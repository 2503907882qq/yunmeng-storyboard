#!/usr/bin/env python3
"""Search the bundled user-supplied descriptor catalog. Python standard library only."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "references" / "lexicon.json"


def positive_limit(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("limit must be an integer from 1 to 100") from exc
    if not 1 <= number <= 100:
        raise argparse.ArgumentTypeError("limit must be from 1 to 100")
    return number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="在本地用户词表中检索候选描述词；词表不等于事实、指令或赛事规则。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python scripts/lookup_terms.py 焦虑 --category emotion --limit 5
  python scripts/lookup_terms.py 环绕 --category 镜头
  python scripts/lookup_terms.py '篮球 运球' --category sports --json
  python scripts/lookup_terms.py --list-categories

多个空格分隔的词使用 AND 子串匹配。排序依次为词面精确匹配、
词面全部包含、来源分类/说明匹配，再按类别和词面排序；不联网、不改写词库。
镜头和风格词也分布在 vivid、美学类别，跨来源查词可省略 --category。""",
    )
    parser.add_argument("query", nargs="?", help="检索词，或用引号包住多个检索词")
    parser.add_argument("-c", "--category", help="类别代码或中文名称；省略时查全部类别")
    parser.add_argument("-n", "--limit", type=positive_limit, default=8, help="返回条数，1–100，默认 8")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出匹配词及完整来源用途")
    parser.add_argument("--list-categories", action="store_true", help="显示类别和词数后退出")
    args = parser.parse_args()
    if not args.list_categories and (not args.query or not args.query.strip()):
        parser.error("请提供非空 query，或使用 --list-categories")
    return args


def search(catalog: dict, query: str, category: str | None) -> list[dict]:
    needles = query.casefold().split()
    results = []
    for key, group in catalog["categories"].items():
        if category is not None and key != category:
            continue
        for entry in group["entries"]:
            term = entry["term"].casefold()
            haystack = " ".join(
                [term] + [
                    " ".join(usage["path"]) + " " + usage.get("source_description", "")
                    for usage in entry["usages"]
                ]
            ).casefold()
            if not all(needle in haystack for needle in needles):
                continue
            if term == query.casefold().strip():
                rank = 0
            elif all(needle in term for needle in needles):
                rank = 1
            else:
                rank = 2
            results.append({"category": key, "category_label": group["label"],
                            "match_rank": rank, **entry})
    return sorted(results, key=lambda item: (item["match_rank"], item["category"], item["term"]))


def main() -> int:
    args = parse_args()
    try:
        with CATALOG.open(encoding="utf-8") as handle:
            catalog = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"无法读取本地词库 {CATALOG}: {exc}", file=sys.stderr)
        return 2
    if args.list_categories:
        for key, category in catalog["categories"].items():
            print(f"{key}\t{category['label']}\t{category['count']}")
        return 0
    aliases = {key.casefold(): key for key in catalog["categories"]}
    aliases.update({group["label"]: key for key, group in catalog["categories"].items()})
    category_key = None
    if args.category:
        category_key = aliases.get(args.category.casefold())
        if category_key is None:
            print("未知类别。使用 --list-categories 查看可用类别。", file=sys.stderr)
            return 2
    results = search(catalog, args.query, category_key)
    selected = results[:args.limit]
    if args.json:
        json.dump({"query": args.query, "category": category_key,
                   "notice": catalog["purpose"], "total_matches": len(results),
                   "returned": len(selected), "results": selected},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print("用户词表候选：按场景改写为可见表达；来源分组、标签及阶段不作事实依据。")
        print(f"匹配 {len(results)} 条，显示 {len(selected)} 条。")
        for entry in selected:
            print(f"\n[{entry['category']}/{entry['category_label']}] {entry['term']}")
            paths = list(dict.fromkeys(" > ".join(usage["path"]) for usage in entry["usages"]))
            print("  语境：" + "；".join(paths))
            sources = list(dict.fromkeys(
                f"{usage['source']['file']} / {usage['source']['sheet']} / "
                f"R{usage['source']['row']}C{usage['source']['column']}"
                for usage in entry["usages"]
            ))
            print("  来源：" + "；".join(sources))
            notes = list(dict.fromkeys(
                note for usage in entry["usages"] for note in usage.get("caveats", [])
            ))
            for note in notes:
                print("  提醒：" + note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
