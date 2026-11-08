# 工具使用说明

本目录是《Buddy Simulator 1984》汉化工具的配套文档。

> 根目录的 `Documents/` 只放**说明文档**；工具运行时读取的 `Textsign.txt`、`Banlist.txt`、修订记录等在 **`PythonExpansion/Documents/`**，两者不要混淆。

## 阅读顺序

| 你的情况 | 建议阅读 |
| --- | --- |
| 第一次使用，想从零跑通一章 | [01-快速开始.md](01-快速开始.md) |
| 已经跑通，查某条命令的参数/输出 | [02-命令参考.md](02-命令参考.md) |
| 想理解中间文件、行号映射、翻译记忆原理 | [03-工作流与数据结构.md](03-工作流与数据结构.md) |
| 遇到报错、路径问题、结果不对 | [04-常见问题.md](04-常见问题.md) |
| 想修改工具代码 | 本目录 + 根目录 [CLAUDE.md](../CLAUDE.md) |

## 文档约定

- `<项目名>`：`Projects/` 下的工作区目录名，例如 `Steam324`。
- `<资源>`：资源子目录名，例如 `level3`、`sharedassets0.assets`。
- 未特别说明时，路径相对仓库根目录。
- 在 `开始.bat` 的 `指令:` 提示符下输入的命令，用普通代码块表示；以 `python ...` 开头的命令在 `cmd` 中直接运行。
- 方括号 `[可选]` 表示可选参数，尖括号 `<必填>` 表示必填参数。

### 版本标记

同一功能可能有两套实现：

| 标记 | 含义 |
| --- | --- |
| **BAT** | 早期批处理实现，位于 `Functions/` |
| **PY** | 后续 Python 实现，位于 `PythonExpansion/` |
| **BAT/PY** | 两者都有，中间格式兼容，可混用 |
| ⚠️ | 含作者本机绝对路径或破坏性操作，使用前确认 |
| 🗑️ | 会删除文件，先备份 |

## 一分钟看懂流程

```text
导出资源
  └─ MonoBehaviour_All/ + Json/ (+ TextMesh/)
        │
        ├─ clearmono → filter        # 筛选含可翻译文本的资源
        ├─ collect                   # 按 pathID 配对 JSON
        └─ save                      # 生成可编辑文本 + 行号表
              │
              ├─ open / 人工翻译      # 文本翻译.txt
              ├─ TL.py                # 百度初稿 文本翻译_baidu.txt
              └─ wordlib/usewordlib   # 翻译记忆复用
                    │
                    └─ load           # 按行号写回 JSON
                          │
                          ├─ examine  # 对比原始 JSON
                          └─ rename-a # 恢复 unnamed asset-... 命名
                                │
                                └─ UABE/AssetStudio 回封 → update
```

## 最重要的五条提醒

1. **先备份**：整个 `Projects/<项目名>/` 和游戏的 `data.unity3d` 在操作前复制一份。
2. **在仓库根目录运行**：脚本依赖相对路径 `Temp\`、`PythonExpansion\`、`Projects\`；不要在 `Functions\` 里双击运行。
3. **第一次先建目录**：`Temp/`、`PythonExpansion/Documents/` 不在仓库中，需要手动创建。
4. **参数不要带空格**：`开始.bat` 按空格拆分命令；`Projects` 下的项目名和资源名用无空格名称。
5. **`remove` / `clearmono` / `update` 会删除文件**：确认路径、做好备份后再执行。

## 文档索引

- [01-快速开始.md](01-快速开始.md) — 环境准备、UABE 导出结构、从 `collect` 到 `rename-a` 的完整单章流程
- [02-命令参考.md](02-命令参考.md) — `Functions/` 全部命令与 `PythonExpansion/` 全部脚本的参数、前置条件、输出
- [03-工作流与数据结构.md](03-工作流与数据结构.md) — 目录契约、`文本.txt`/`行数` 格式、MD5 翻译记忆、百度机翻保护规则、TextMesh
- [04-常见问题.md](04-常见问题.md) — 常见报错、编码问题、路径修改、`fc` 本地化、JSON 校验
