#!/usr/bin/env python3
"""Check explicit storyboard data; never claim visual or physical correctness."""
import argparse
import json
import math
from pathlib import Path


def check(data):
    errors, warnings = [], []
    if not isinstance(data, dict):
        return {'ok': False, 'errors': ['顶层必须是对象'], 'warnings': [], 'total_seconds': None}
    assets = data.get('assets', {})
    if not isinstance(assets, dict):
        errors.append('assets必须是对象'); assets = {}
    for name, asset in assets.items():
        if not isinstance(asset, dict):
            errors.append(f'资产{name}必须是对象'); continue
        status = asset.get('status')
        if status not in ('missing', 'available', 'approved'):
            errors.append(f'资产{name}状态应为missing/available/approved')
        if status in ('available', 'approved') and not asset.get('source'):
            errors.append(f'资产{name}声称已有但缺少来源')
        if status == 'approved' and not asset.get('approval_evidence'):
            errors.append(f'资产{name}声称验收但没有验收依据')
    shots = data.get('shots', [])
    if not isinstance(shots, list) or not shots:
        errors.append('shots应为非空列表'); shots = []
    total, ids, previous_end = 0.0, set(), None
    for number, shot in enumerate(shots, 1):
        if not isinstance(shot, dict):
            errors.append(f'第{number}镜必须是对象'); continue
        sid = shot.get('id')
        label = sid if isinstance(sid, str) and sid else f'第{number}镜'
        if not isinstance(sid, str) or not sid:
            errors.append(f'{label}缺少字符串id')
        elif sid in ids:
            errors.append(f'重复镜号{sid}')
        else:
            ids.add(sid)
        duration = shot.get('duration_seconds')
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
            errors.append(f'{label}时长必须为有限正数')
        else:
            total += duration
        required = shot.get('required_assets', [])
        if not isinstance(required, list):
            errors.append(f'{label}required_assets必须是列表'); required = []
        for name in required:
            if not isinstance(name, str) or name not in assets:
                errors.append(f'{label}引用未登记资产{name}')
            elif isinstance(assets[name], dict) and assets[name].get('status') == 'missing':
                warnings.append(f'{label}所需资产{name}缺失，仅可作文字方案，生成前待绑定')
        bindings = shot.get('reference_bindings', {})
        if not isinstance(bindings, dict):
            errors.append(f'{label}reference_bindings必须是对象'); bindings = {}
        for slot, name in bindings.items():
            asset = assets.get(name) if isinstance(name, str) else None
            if not isinstance(asset, dict) or asset.get('status') not in ('available', 'approved') or not asset.get('source'):
                errors.append(f'{label}参考位{slot}绑定了缺失或无来源资产{name}')
        start, end = shot.get('state_start'), shot.get('state_end')
        if not isinstance(start, dict) or not start:
            warnings.append(f'{label}未完整声明起始状态，无法充分比对'); start = {}
        if not isinstance(end, dict) or not end:
            warnings.append(f'{label}未完整声明结束状态，无法充分比对'); end = {}
        transition = shot.get('transition', {})
        if not isinstance(transition, dict):
            errors.append(f'{label}transition必须是对象'); transition = {}
        changes = transition.get('changes', {})
        if not isinstance(changes, dict):
            errors.append(f'{label}transition.changes必须是对象'); changes = {}
        if transition.get('type') in ('ellipsis', 'scene_change') and not transition.get('explanation'):
            errors.append(f'{label}省略/换场缺少观众可理解的说明')
        if previous_end is not None:
            for key in previous_end.keys() & start.keys():
                if previous_end[key] != start[key] and not (isinstance(changes.get(key), str) and changes[key].strip()):
                    errors.append(f'{label}状态跳变未交代：{key}，{previous_end[key]!r} → {start[key]!r}')
            omitted = previous_end.keys() - start.keys()
            if omitted:
                warnings.append(f'{label}缺少前镜状态键：'+', '.join(sorted(omitted)))
        previous_end = end
    target = data.get('target_duration_seconds')
    if target is not None:
        if isinstance(target, bool) or not isinstance(target, (int, float)) or not math.isfinite(target) or target <= 0:
            errors.append('target_duration_seconds必须为有限正数')
        elif not math.isclose(total, target, rel_tol=0, abs_tol=0.05):
            errors.append(f'总时长{total:g}秒与目标{target:g}秒不符')
    return {'ok': not errors, 'total_seconds': round(total, 3), 'shot_count': len(shots),
            'errors': errors, 'warnings': warnings,
            'scope': '只验证声明的结构与状态；视觉、物理、台词语速及声明真实性仍须检查。'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='UTF-8 storyboard JSON')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8-sig'))
        report = check(data)
    except (OSError, ValueError) as exc:
        report = {'ok': False, 'errors': [str(exc)], 'warnings': []}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
