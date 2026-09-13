# 模型适配：通用内容与平台参数分离

来源与核验：用户提供的《Midjourney V8.2 参数大全（AI短剧分镜专用）》署期为2026年8月，已完整读取第一至九节。它提供风格、画幅、复用与批量创作的思路，但不是官方能力依据。下表“原文”保留争议来源，“核验”依据所链官方页面；核验日期为 **2026-09-13**。这是有日期的记录，不能替代后续使用时的版本检查，也不能将该日期的默认版本写成技能永久默认。

## 通用适配规则

用户常用入口按原话记录为 **LibTV、sd2.5**；此处尚未核实准确产品、模型全名及接口能力。不得擅自展开为 Stable Diffusion、Seedance 或其他模型，也不得从简称推定它支持参考图、首尾帧、原生音频或某种参数。写普通分镜时直接交付可用的中文自然语言；只有确实需要填写平台专属字段时，才核对用户界面、官方链接或已有设置。

提示词分两层：第一层写主体身份、场景、动作、景别、构图、光线、材质与风格；视频另写动作先后、主体与镜头各自的运动、结束状态。第二层单列平台、模型版本、任务类型、参考素材槽位、画幅及已核实设置。平台未指定或不是 Midjourney 时，不自动拼接 `--v`、`--p`、`--sref` 等 MJ 标记。真人、3渲2、赛璐璐等风格保留为正文描述，不能冒充官方预设。

参考素材清单应写明文件名、角色或场景编号、用途与镜头关联。角色身份参考、视觉风格参考、构图参考、视频首帧和尾帧分别标注；同一张图承担多种用途时也要明确，不能把本地路径伪装成可访问网址。缺少平台要求的素材时保留素材需求，已有分镜照常完成。负面要求先用自然语言单列，只有目标平台确认支持负面提示字段时才映射过去；否则把必需的人物数量、服装完整性和动作关系写进正向描述，并通过结果检查修正。

可迁移的动作示例：“她先看向门口，停顿后握紧钥匙；镜头缓慢向前推进，结束时停在胸像景别。”此句描述叙事目标，不暗示任何平台具有精确时间线控制；若实际出片动作拥挤，拆成两个镜头。

镜头时长是创作计划；模型单次生成时长、分辨率和续接方式是执行条件。两者分别记录，能力未知标“待核实”，不编造最大秒数或1080p限制。画幅、成片分辨率和原生生成尺寸也分别记录。若执行条件不足，先拆分动作与交付分镜，不能把补帧、放大或剪辑建议宣称为模型原生支持。不因编写提示词自动要求注册、申请密钥或购买服务。

## Midjourney 条件核验表

仅在明确采用 MJ 时使用本节；版本、模式与账户条件需匹配。

| 原文位置及说法 | 官方核验与处理 |
| --- | --- |
| 第一、九节：V8.2 最新，8.0/8.1/8.2均可选，固定8.2 | V8.2确有[2026-07-24发布公告](https://updates.midjourney.com/version-8-2/)。[Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)已列V8.0停止提供；按项目实际版本填写，不盲用旧表。 |
| 第一、八节：`--p cinematic/photoreal/anime/editorial/sketch/3d` 为官方预设 | [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization)规定 `--p` 使用默认个人化配置或真实配置ID/code；这些风格词不能据此作为官方配置值。无有效配置就省略。 |
| 第一节：V8.2的 `--q` 可用0.25、0.5、1、high、ultra | [Version兼容表](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)标明V8.1/8.2不支持 `--q`；[Quality](https://docs.midjourney.com/hc/en-us/articles/32176522101773-Quality)的V7数值为1、2、4。不能跨版本搬用，high/ultra未获这些文档支持。 |
| 第三节：`--sw` 为0–2、默认1 | [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)写0–1000、默认100；风格参考可用图片或有效代码，不能拿它锁定角色身份。 |
| 第四、九节：任意整数seed，同seed可保持角色与场景、多角度复用 | [Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds)限定整数0–4294967295；它控制初始噪声，用于对照实验，不保证跨提示词身份、布局或风格。 |
| 第九节：移除 `--cref/--oref`，以seed+p+sref替代 | [Edit Model](https://docs.midjourney.com/hc/en-us/articles/48495453462797-Edit-Model)在V8.1/8.2承接角色与物体参考能力；网页附加参考图或Discord `--edit` 使用须按文档。原文“替代配方”不成立；仍需逐镜检查角色。 |
| 第七节：`--motion 1–4`、默认2 | [Video](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video)使用 `--motion low` 或 `--motion high`。视频只接收其支持的参数，不能继承整套图片后缀。 |
| 第六节：`--r 2–40` 通用；`--stealth` 直接保密 | [Repeat](https://docs.midjourney.com/hc/en-us/articles/32757107922061-Repeat)范围受套餐及速度模式约束；[Stealth](https://docs.midjourney.com/hc/en-us/articles/32019750070669-Stealth-Mode)受账户资格约束，公开Discord频道中的作品仍可见。不能作为无条件模板。 |

## 其余参数的使用边界

原文第一节的 `--hd/--sd` 在[Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)中有依据，兼容表确认V8.1/8.2高清图片能力；不要把图片HD标记解释为视频分辨率开关。第二节 `--ar` 表达宽高比，不等于像素尺寸，范围还随版本及HD模式变化，见[Aspect Ratio](https://docs.midjourney.com/hc/en-us/articles/31894244298125-Aspect-Ratio)。

第三、四节的数值范围与官方相符：[Stylize](https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize)为0–1000，[Chaos](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety)为0–100，[Weird](https://docs.midjourney.com/hc/en-us/articles/32390120435085-Weird)为0–3000。但“低s必写实、高s必二次元”“低chaos得到同角色不同镜头”均非保证；weird是实验特性，与seed也不完全兼容。[Raw](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw)减少模型自动风格加工，不承诺去掉滤镜或保证摄影真实感。

第五、九节的 `--no` 用来表达排除倾向，不是修手、去水印或清除缺陷的保证。按[No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No)可用英文逗号分隔排除项；逐项检查是否误伤剧情必需内容，不机械追加“文字、模糊”等。按[Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)，正文与参数之间必须留空格，参数放末尾，`--`与名称之间无空格。原文“参数前不能带空格”应纠正为“参数名称内部不能插入空格”。

## 交付与复核

原文第八节三套配方仅保留风格描写，不原样复制其参数串或“统一参数保证一致”的承诺。先固定角色卡、服装道具、场景关系与参考素材；获选图再用于后续镜头的实际参考流程，seed只作实验记录。每次输出专属参数时检查平台、版本、图像/视频模式、实际素材与支持范围；用户问“最新”、指定新版本或平台报错时重新查官方文档。页面矛盾时标明冲突，无法核验则省略争议标记并交付自然语言稿；不靠猜测补齐。记录使用版本与核验日期，避免保存会过期的价格或默认版本判断。
