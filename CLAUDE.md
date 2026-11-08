# CLAUDE.md

本文件面向在此仓库中工作的 Claude Code / 其他自动化代理，说明项目结构、运行方式和修改约束。用户文档见 `README.md` 与 `Documents/`。

## 项目是什么

《Buddy Simulator 1984》的 Windows 汉化工具链。输入是 UABE/AssetStudio 导出的 Unity MonoBehaviour 文本 dump 与 JSON dump；输出是改好译文的 JSON，再由外部工具回封进 `data.unity3d`。仓库只含工具和过程资料，不含游戏资源、`Projects/` 工作数据或 API 密钥。

## 技术栈

- **Windows CMD 批处理**：`开始.bat` + `Functions/*.bat`（28 个），UTF-8 无 BOM、CRLF，启动时 `CHCP 65001`。
- **Python 3**：`PythonExpansion/*.py`（15 个），标准库 + `requests`；无 requirements、构建系统或测试。
- **外部工具**：UABE / AssetStudio（资源 dump/import）、百度翻译 API、Notepad++、Edge、`certutil`。
- **数据**：UTF-8 文本/JSON；`文本们.txt` 是 GBK 日志。

## 运行方式

必须在**仓库根目录**运行；脚本大量使用相对路径（`Temp\`、`PythonExpansion\`、`Projects\`）。

- **交互入口**：`开始.bat`（cmd 下双击或 `cmd /c 开始.bat`）。
  - 读取 `当前项目.txt` 第一行作为 `PROJECT_DIR`，默认 `Projects\New`。
  - 显示 `备忘录.txt`。
  - 输入按空格拆成最多 4 个 token；若 `Functions\<token>.bat` 存在，`call` 它并传入后 3 个参数；否则 `call %INPUT%` 直接执行原始命令。
  - 因此参数不能含空格；未识别命令会交给 CMD，可能有破坏性，执行前确认。
- **单步批处理**（非交互）：

  ```bat
  cmd /c "set PROJECT_DIR=Projects\Steam324 && call Functions\save.bat level3"
  ```

- **单步 Python**（推荐）：

  ```bat
  python PythonExpansion\SAVE.py "Projects\Steam324" level3
  ```

  `sys.argv[1]` 恒为 `PROJECT_DIR`，`sys.argv[2]` 为资源子目录名（如 `level3`、`sharedassets0.assets`），部分脚本有 `argv[3]`。

- **`-py <脚本> [参数]`**：`Functions\-py.bat` 提示输入一个参数，然后执行：

  ```bat
  python PythonExpansion\<脚本>.py "%PROJECT_DIR%" "<参数>"
  ```

  多参数场景用 `-py CODING`，例如 `SAVE(level3);FILTER(level3,1)`。

## 目录与职责

| 路径 | 职责 |
| --- | --- |
| `开始.bat` | 启动器、项目选择、备忘录、命令分发 |
| `Functions/` | 每个 `.bat` 一个命令；`h.bat` 帮助；`-py.bat` Python 桥 |
| `PythonExpansion/` | 新版步骤、百度翻译、修订、TextMesh、配置生成 |
| `Projects/` | 工作区数据（不在仓库内） |
| `Temp/` | 共享临时目录；脚本会写入并清空，不能并发运行 |
| `Documents/` | 用户/开发文档 |
| `PythonExpansion/Documents/` | 运行时配置与修订数据，和根 `Documents/` 不同 |

### 批处理层

- `clearmono`、`filter`、`collect`、`save`、`load`、`wordlib`、`usewordlib`、`examine`、`rename-a`、`textlib`、`usetextlib`、`auto`、`auto-t` 等各一个文件。
- `h.bat` 中的帮助文本是命令契约的一部分；新增/修改命令时同步更新。
- `save.bat` / `filter.bat` 是早期实现；`PythonExpansion/` 中有对应 Python 重写（`SAVE.py`、`FILTER.py` 等）。中间文本格式兼容、可混用，但 Python 版依赖 `Textsign.txt` / `Banlist.txt`，且 TextMesh 输出目录与批处理版不同。

### Python 层

| 脚本 | 参数 | 作用 |
| --- | --- | --- |
| `CODING.py` | 忽略 `argv[2]` | 交互式多命令解释器 |
| `COLLECT.py` | `dir` | 按 pathID 收集 JSON |
| `FILTER.py` | `dir [,1]` | 过滤 MonoBehaviour；第三参为 `1` 时处理全部子目录（需直接调用） |
| `LOAD.py` | `dir [file]` | 将译文写回 JSON |
| `PREFIX_CATCH.py` | 忽略 | 扫描 `MonoBehaviour_All`，生成 `Textsign_catch.txt` |
| `RENAME.py` | `dir [1/2]` | 将 JSON 改名为 `unnamed asset-...` |
| `REVISE.py` | `dir` | 逐行修订并记录修订记忆 |
| `SAVE.py` | `dir` | 导出 `文本.txt` 与 `行数` |
| `T.py` | `text` | 单句百度翻译，打印到 stdout |
| `TEXTLIB.py` | `dir` | 构建 TextMesh 文本库 |
| `TL.py` | `dir` | 批量百度翻译，输出 `文本翻译_baidu.txt` |
| `UPDATE.py` | 忽略 | 将游戏目录中的 `*-mod` 更新为正式文件 |
| `USETEXTLIB.py` | `dir` | 应用 TextMesh 文本库 |
| `USEWORDLIB.py` | `dir [file]` | 应用翻译记忆库 |
| `WORDLIB.py` | `dir` | 从人工译文构建翻译记忆库 |

## 数据流

1. `clearmono` 按 `清除名单.txt` 删除 `MonoBehaviour_All/<resource>/` 中的无关资源。
2. `filter` 保留含可翻译字段的资源到 `MonoBehaviour/<resource>/`。
3. `collect` 按 `<pathID>` 前缀把 `MonoBehaviour` 与 `Json` 配对到 `Json_Collected/<resource>/`。
4. `save` 从 JSON 提取可翻译行，写 `Workspace/<resource>文本.txt` 与 `Workspace/行数/<resource>`。
5. `open` 生成 `Workspace/<resource>文本翻译.txt`，人工翻译；`TL.py` 生成 `文本翻译_baidu.txt`。
6. `wordlib` 从「原文/译文」构建 `Projects/<project>/WordLib/<md5>`；`usewordlib` 用词库生成译文。
7. `load` 按行号把译文写回 `Workspace/<resource>/<pathID>-<name>.json`。
8. `examine` 对比生成 JSON 与 `Json_Collected`；`rename-a` 恢复 `unnamed asset-<resource>-<pathID>.json` 命名。
9. 用 UABE/AssetStudio 回封 `data.unity3d`，再由 `update.bat` 或 `UPDATE.py` 更新游戏目录。

## 关键数据契约

工作区位于 `Projects/<project>/`：

```text
MonoBehaviour_All/<resource>/<pathID>-<name>.txt
MonoBehaviour/<resource>/<pathID>-<name>.txt
Json/<resource>/unnamed asset-<resource>-<pathID>.json
Json_Collected/<resource>/<pathID>-<name>.json
Workspace/<resource>文本.txt
Workspace/<resource>文本翻译.txt
Workspace/<resource>文本翻译_baidu.txt
Workspace/<resource>_Translated.txt
Workspace/行数/<resource>
Workspace/<resource>/<pathID>-<name>.json
WordLib/<md5>
TextLib/<md5>
TextMesh/<resource>/*.txt
TextMesh/Translated/<resource>_T/*.txt      # Python 版
TextMesh/<resource>_T/*.txt                # 批处理版
TextMesh/地址.txt
Renamed/<resource>_renamed/unnamed asset-<resource>-<pathID>.json
```

`Workspace/` 根目录必须预先存在；`save` 只创建 `Workspace/行数/` 子目录。

运行时配置/缓存：

```text
PythonExpansion/Documents/Textsign.txt       # 字段白名单，格式 string <字段>=样例
PythonExpansion/Documents/Banlist.txt        # 首词黑名单，每行小写
PythonExpansion/Documents/Revision/<resource>/0|1|2/   # REVISE 生成的原文/人工/百度
PythonExpansion/Documents/Revision/<resource>/Process.txt
PythonExpansion/Documents/WordLib/<md5>      # REVISE 的修订记忆（独立于项目 WordLib）
PythonExpansion/Translated/<md5>             # 百度翻译缓存
PythonExpansion/Translated/地址.txt
Temp/*.tmp                                   # 共享临时文件
```

## 关键不变量与易错点

1. **MD5 含行尾换行**：WordLib/TextLib/修订库的键是「行内容 + 换行」在 Windows 文本模式下写入后的 MD5（实际为 UTF-8 + CRLF）。不要用 `strip()` 后的字符串重算，也不要统一换行符。
2. **行号公式**：`save` 对 JSON 的每一行递增 3，首行为 3；`load` 用 `(零基行号 + 1) * 3` 查表。不要改变这个偏移。
3. **文本格式的哨兵**：`当前文件:<path>` 和 `备注:` 不是翻译单元；可翻译行以制表符开头；含反斜杠的行按整行翻译/整行替换。
4. **JSON 回写**：普通行按 `line.split('"')` 后第 4 个片段（索引 3）替换字符串值；含 `\` 的行直接写译文整行。改动格式会导致 JSON 损坏。
5. **Textsign/Banlist**：`Textsign.txt` 每行形如 `string text=样例`，只取 `=` 左侧；`SAVE.py` 会加 `1 ` 前缀匹配 JSON 键。`Banlist.txt` 每行小写，匹配文本值的第一个词。
6. **TL.py 保护规则**：`[占位符]` 替换为 `§`、人物名替换为 `√`、`...`/`:)`/`:(` 替换为 `■` 后送百度，再按顺序还原；新增人物名要同时改 `TL.py` 里的 `banlist`/`banlist2`。
7. **Temp 是全局共享的**：多个脚本会 `del Temp\*` 或复用 `Temp\TEXT.tmp`；不要并行运行两个命令。
8. **编码**：批处理、Python、工作数据均为 UTF-8（无 BOM）；`.bat` 用 CRLF，Python 用 LF；`文本们.txt` 是 GBK 日志。
9. **硬编码路径**：`Functions/change.bat`、`open.bat`（Notepad++）、`web.bat`（Edge）、`update.bat`，以及 `PythonExpansion/UPDATE.py`（游戏目录）含作者本机路径，换机需修改。
10. **仓库缺失的运行时文件**：`Projects/`、`Temp/`、`PythonExpansion/Documents/{Textsign,Banlist}.txt`、`APIs/BaiduAPI.txt` 的真实密钥都不在仓库中；不要假设它们存在。
11. **参数不能带空格**：启动器按空格分词；路径/项目名请用无空格名称。
12. **输出命名**：`usewordlib` 在存在 `X文本翻译.txt` 时输出 `X_Translated.txt`，否则输出 `X文本翻译.txt`；`RENAME.py` 输出到 `Renamed/<resource>_renamed`，重名时追加 `(1)`、`(2)`。
13. **`PROJECT_DIR` 保持相对路径**：`manage` 写入的是 `Projects\<name>`；`LOAD.py` 里 `os.getcwd() + "\\" + WORKSPACE_DIR` 假设其为相对路径，改成绝对路径会生成错误目录。

## 修改代码时的注意事项

- 保持命令行契约：Python 脚本 `argv[1]=PROJECT_DIR`、`argv[2]=dir_name`，不要随意调整参数顺序；`-py` 只能传一个参数。
- 新增批处理命令时，在 `Functions/` 放一个同名 `.bat`，启动器会自动发现；同时更新 `Functions/h.bat` 和 `Documents/02-命令参考.md`。
- 新增 Python 命令时，放在 `PythonExpansion/`，并在 `README.md`/`CLAUDE.md` 的脚本表中登记。
- 不要重命名中文后缀（`文本`、`文本翻译`、`文本翻译_baidu`、`_Translated`、`行数`）或 `PythonExpansion/Documents` 下的配置名。
- 修改哈希/行号/替换逻辑前，先用一份已知正确的 JSON 做端到端对比；保存原始文件用于回滚。
- 生成物（`Projects/`、`Temp/`、`PythonExpansion/Translated/`、`PythonExpansion/Documents/Revision/`）不应提交到仓库。
- 不要并行运行会使用 `Temp/` 的脚本；不要对用户数据执行 `remove`、`clearmono`、`update` 等破坏性命令，除非用户明确要求并已备份。

## 验证方式

无自动化测试。提交前至少做：

```bat
python -m compileall -q PythonExpansion
```

并用手工/小型 fixture 走一遍 `SAVE -> WORDLIB -> USEWORDLIB -> LOAD -> RENAME`，用 `fc` 或 `examine` 检查 JSON 只改动了目标字符串。涉及批处理时，在 `cmd` 中运行 `h` 和对应命令，确认没有语法错误。

## 文档

- `README.md` — 项目简介、快速开始、命令速查
- `Documents/README.md` — 文档索引
- `Documents/01-快速开始.md` — 环境与端到端流程
- `Documents/02-命令参考.md` — 命令/脚本参数与输出
- `Documents/03-工作流与数据结构.md` — 文件格式、行号、哈希、TextMesh
- `Documents/04-常见问题.md` — 故障排查与路径修改
