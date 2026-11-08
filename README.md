# Buddy Simulator 1984 汉化工具

> 一套面向《Buddy Simulator 1984》的 Windows 文本汉化流水线：从 Unity 资源导出、可翻译文本筛选、人工/机器翻译、翻译记忆复用，到 JSON 回写、资源回封与游戏更新。

## 项目简介

本仓库是作者在汉化《Buddy Simulator 1984》过程中使用的完整工具链（示例工作区名为 `Steam324`）。仓库**不包含**游戏本体、`data.unity3d`、导出的资源或成品补丁；使用前需要自备游戏文件，并用 UABE / AssetStudio 等工具导出资源。

工具的核心思路是：

1. 把 Unity 资源中的 MonoBehaviour 文本 dump 与 JSON dump 按 pathID 配对；
2. 只保留真正包含可翻译字符串的资源；
3. 将英文原文与 JSON 行号分离，输出成便于编辑的文本；
4. 用 MD5 翻译记忆库复用已有译文，用百度翻译生成初稿；
5. 将译文按行号写回 JSON，检查差异后恢复资源命名并回封。

## 主要功能

- **资源筛选**：按 `清除名单.txt` 删除无关组件，按 `黑名单.txt` / `Banlist.txt` 排除非文本字段。
- **JSON 配对**：根据 pathID 把 MonoBehaviour dump 与 JSON dump 一一对应。
- **可编辑文本导出**：生成 `X文本.txt` 与 `行数\X`，保留 `当前文件`、`备注` 等定位信息。
- **翻译记忆库（WordLib）**：以整行英文的 MD5 为键，复用人工译文；支持查询和编辑单条记录。
- **百度翻译辅助**：`TL.py` 批量机翻，`T.py` 单句查询；带本地缓存、占位符和人物名保护。
- **修订工作流**：`REVISE.py` 对比原文、人工译文和百度译文，逐行记录修订决策。
- **TextMesh 文本库**：单独处理 TextMesh 资源中的 `m_Text` 行。
- **批处理自动化**：`auto` / `auto-t` 按 `level` 与 `sharedassets` 编号区间批量执行。
- **回写与校验**：`load` 生成 JSON，`examine` 对比差异，`rename-a` 恢复资源命名，`update` 更新游戏文件。
- **命令面板**：`开始.bat` 自动发现 `Functions\*.bat`，也允许直接执行 CMD 内建命令。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 启动器 / 命令层 | Windows CMD 批处理（`CHCP 65001`，28 个 `.bat`） |
| 扩展层 | Python 3（`requests`、`hashlib`、`shutil`、`json`） |
| 资源处理 | UABE（Unity Asset Bundle Extractor）/ AssetStudio 等外部工具 |
| 机器翻译 | 百度翻译开放平台 API |
| 辅助工具 | Notepad++、Microsoft Edge、Windows `certutil` |
| 数据格式 | Unity `data.unity3d`、MonoBehaviour 文本/JSON dump、UTF-8 纯文本 |

项目没有构建系统、依赖清单或自动化测试；所有步骤通过命令和中间文件驱动。

## 工作流总览

```text
UABE / AssetStudio
   ├─ MonoBehaviour_All/<资源>/*.txt ──clearmono/filter──▶ MonoBehaviour/<资源>/*.txt
   ├─ Json/<资源>/*.json ──────────────collect───────────▶ Json_Collected/<资源>/*.json
   └─ TextMesh/<资源>/*.txt ───────────textlib───────────▶ TextLib/
                                          │
MonoBehaviour + Json_Collected ──save──▶ Workspace/<资源>文本.txt + 行数/<资源>
                                          │
                              open（人工翻译）+ TL.py（百度初稿）
                                          │
                              wordlib / usewordlib（翻译记忆）
                                          │
                                       load ──▶ Workspace/<资源>/*.json
                                          │
                              examine ──▶ rename-a ──▶ Renamed/<资源>_renamed
                                          │
                              UABE 回封 ──▶ data.unity3d ──▶ update
```

## 目录结构

```text
1984Translation/
├─ 开始.bat                 # 主入口：读取当前项目、显示备忘录、分发命令
├─ 当前项目.txt             # 当前工作区，例如 Projects\Steam324
├─ 备忘录.txt               # 翻译约定/提醒，启动时显示，可用 edit 编辑
├─ 黑名单.txt               # 批处理版过滤器使用的首词黑名单
├─ 清除名单.txt             # clearmono 要删除的 MonoBehaviour 类型
├─ 文本们.txt               # 历史机翻输出日志（GBK），不是工具输入
├─ Functions/               # 28 个 CMD 命令实现
├─ PythonExpansion/         # Python 扩展与新版实现
│  ├─ APIs/BaiduAPI.txt     # 百度翻译 APPID/APPKEY（当前为占位符）
│  ├─ Documents/            # 运行时配置：Textsign.txt、Banlist.txt、Revision、WordLib（需自建）
│  ├─ Translated/           # 百度翻译缓存（运行时生成）
│  └─ *.py                  # 15 个 Python 脚本
├─ Projects/                # 各版本工作区（不随仓库提供）
├─ Temp/                    # 临时文件（需自建；脚本会清空）
└─ Documents/               # 本工具的使用说明
```

> 注意：根目录的 `Documents/` 是**文档**；`PythonExpansion/Documents/` 是**运行时配置与修订数据**，两者不是同一个目录。

## 环境要求

- Windows 10/11，使用 `cmd.exe`（不要用 PowerShell 直接运行 `.bat`）。
- Python 3.x（建议 3.8+），并安装 `requests`：

  ```bat
  pip install requests
  ```

- UABE / AssetStudio：用于导出 MonoBehaviour、JSON、TextMesh，并在最后回封 `data.unity3d`。
- 可选：Notepad++（`open`、`change` 默认调用）和 Microsoft Edge（`web` 命令）。
- 可选：百度翻译开放平台账号（仅 `TL.py` / `T.py` 需要）。

## 快速开始

更完整的步骤见 [Documents/01-快速开始.md](Documents/01-快速开始.md)。

1. **准备 Python**：安装 Python 3 和 `requests`。
2. **准备资源**：用 UABE/AssetStudio 导出到 `Projects/<项目名>/`，至少包含 `MonoBehaviour_All/`、`Json/`；TextMesh 视需要导出。
3. **创建目录**：在仓库根目录创建 `Temp/` 和 `PythonExpansion/Documents/`；在项目下创建 `Workspace/`（`save` 只创建 `Workspace/行数/`，不会创建 `Workspace/` 根目录）。
4. **生成配置（Python 版需要）**：运行 `-py PREFIX_CATCH`，将 `Textsign_catch.txt` 审阅后保存为 `Textsign.txt`；按 `黑名单.txt` 建立 `Banlist.txt`。
5. **选择项目**：双击 `开始.bat`，执行 `manage <项目名>`。
6. **跑通单章（批处理版）**：

   ```text
   clearmono level3
   filter level3
   collect level3
   save level3
   open level3
   ```

7. **翻译与复用**：编辑 `Projects/<项目名>/Workspace/level3文本翻译.txt`；然后用 `wordlib level3`、`usewordlib level3` 或 `-py TL level3`。
8. **回写与回封**：

   ```text
   load level3
   examine level3
   rename-a Workspace level3
   ```

   批处理版 `rename-a` 需要两个参数；如果使用 Python 版，则对应 `-py RENAME level3`（提示选择 `1` 表示 `Workspace`）。用 UABE 导入 `Renamed/level3_renamed/` 或 `Workspace/level3_renamed/` 中的 JSON，重新打包 `data.unity3d`，再按需修改 `update.bat` 或 `UPDATE.py` 的路径并更新游戏。

## 命令速查

| 命令 | 说明 |
| --- | --- |
| `h` | 显示帮助 |
| `manage <项目名>` | 切换 `Projects/<项目名>` 工作区 |
| `collect <资源>` | 按 pathID 收集 JSON 到 `Json_Collected` |
| `filter <资源>` | 过滤 `MonoBehaviour_All`，保留含可翻译文本的资源 |
| `clearmono <资源>` | 按 `清除名单.txt` 删除无关 MonoBehaviour |
| `save <资源>` | 导出 `X文本.txt` 与 `行数/X` |
| `open <资源>` | 创建/打开 `X文本翻译.txt` |
| `wordlib <资源>` | 从人工译文构建翻译记忆库 |
| `usewordlib <资源> [文件]` | 用翻译记忆库生成译文 |
| `load <资源> [文件]` | 将译文按行号写回 JSON |
| `examine <资源>` | 对比 `Workspace` 与 `Json_Collected` |
| `rename-a <顶层目录> <子目录>` / `-py RENAME <资源>` | 恢复 `unnamed asset-<资源>-<pathID>.json` 命名 |
| `remove <资源>` | 删除 `Workspace/<资源>` 下生成的 JSON |
| `textlib <资源>` / `usetextlib <资源>` | TextMesh 文本库的建立/应用 |
| `auto <m>-<n> <o>-<p>` | 批量 `clearmono` + `filter` |
| `auto-t <m>-<n> <o>-<p>` | 批量调用 `TL.py` 机翻 |
| `-py <脚本> [参数]` | 运行 Python 扩展 |
| `view` / `web <词>` / `edit` / `change <命令>` / `update` | 辅助命令 |

完整参数、前置条件和输出说明见 [Documents/02-命令参考.md](Documents/02-命令参考.md)。

## 翻译记忆与机器翻译

- **WordLib 的键**是整行英文（去掉制表符后补一个换行）的 MD5；值是中文译文。改写英文、增删空格或换行都会导致命中失败。
- **人工译文优先**：`usewordlib` 只做精确匹配，不会覆盖已有 `文本翻译.txt`；必要时输出 `_Translated.txt`。
- **百度机翻是初稿**：`TL.py` 只翻译以句末标点结尾的行，并保护 `[PLAYER]` 这类占位符和硬编码的人物名；结果写入 `文本翻译_baidu.txt`，不会直接覆盖人工译文。
- **修订记忆独立**：`REVISE.py` 把修订记录保存在 `PythonExpansion/Documents/WordLib/`，与项目内的 `WordLib/` 不是同一套；它用于辅助审校，不会自动改写 `Workspace` 文件。

## 已知限制与注意事项

- 仓库不含游戏资源、`Projects/` 数据和成品补丁；需要自行准备并遵守游戏许可。
- 多个脚本里有作者本机的绝对路径（Notepad++、Edge、游戏目录），换机器后必须修改，详见常见问题。
- `开始.bat` 只按空格拆分前 4 个参数，**参数中不能带空格**；未匹配到 `Functions\*.bat` 的输入会原样交给 CMD 执行，请避免误执行危险命令。
- 批处理版是早期实现，处理大文件较慢且对特殊字符敏感；Python 版是后续重写，建议在大量文本时优先使用。
- 翻译前请备份 `Projects/`；`remove`、`update` 会删除文件，确认路径后再执行。
- `文本们.txt` 是历史 `auto-t` 输出日志，编码为 GBK，不是工具读取的数据。
- 仓库未附开源许可证；如需复用或分发，请先联系作者确认。

## 文档

- [Documents/README.md](Documents/README.md) — 文档索引与阅读顺序
- [Documents/01-快速开始.md](Documents/01-快速开始.md) — 从零搭建并跑通一章
- [Documents/02-命令参考.md](Documents/02-命令参考.md) — 全部命令与 Python 脚本
- [Documents/03-工作流与数据结构.md](Documents/03-工作流与数据结构.md) — 中间文件格式、行号映射、翻译记忆、TextMesh
- [Documents/04-常见问题.md](Documents/04-常见问题.md) — 故障排查与路径修改

---

本项目仅用于学习和交流；《Buddy Simulator 1984》及其资源版权归原开发者所有。
