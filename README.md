# nonebot_plugin_webui_baize

NoneBot2 Web UI 管理面板插件，基于 FastAPI 提供浏览器端管理界面。
当前界面使用「崩坏：星穹铁道」流萤印象主题，加入薄荷青绿配色、动态登录横幅、玻璃卡片、光粒气泡和随机图片图标，并拥有插件管理、配置编辑、实时日志、指令列表、Bot 信息、AI 人设、帮助模块、插件商店和 GitHub 插件下载等主要功能。

<p align="center">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/1.png" width="34" alt="">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/2.png" width="34" alt="">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/3.png" width="34" alt="">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/4.png" width="34" alt="">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/5.png" width="34" alt="">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/6.png" width="34" alt="">
</p>

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/7.png" width="24" alt=""> 快速开始

### 安装

```bash
pip install git+https://github.com/sangonomiya249/nonebot_plugin_webui_baize.git
```

### NoneBot 配置

在 `pyproject.toml` 中添加插件：

```toml
[tool.nonebot]
plugins = ["nonebot_plugin_webui_baize"]
```

### 访问

默认地址：`http://127.0.0.1:8899`

| 用户名 | 密码 |
| ---- | ---- |
| `admin` | `admin` |

> 首次登录后建议立即修改密码。

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/8.png" width="24" alt=""> 功能

### 登录界面

使用流萤印象主题登录页，顶部动态横幅参考 Firefly 风格，首次登录修改默认密码、Token 认证与会话刷新逻辑。

**QQ 指令：** `webui` / `webui start` 启动后访问 Web UI

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/admin.png" width="600" alt="登录界面">

---

### 系统仪表盘

首页概览 Bot 运行状态，包括 CPU / 内存 / 磁盘使用率、运行时间、消息收发统计、管理员列表、Token 用量趋势图（需安装 AI 对话插件）。

**QQ 指令：** 打开 Web UI 后自动刷新

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/dashboard.png" width="600" alt="仪表盘">

---

### 插件管理

列出所有已加载插件及加载状态。支持：

- ✅ 启用 / 禁用插件（重启生效）
- ✅ 一键启用 / 禁用全部
- 👆 卸载外部插件（pip 安装的）
- 👆 编辑插件配置（见下方「插件配置编辑器」）

**QQ 指令：** 无（Web 端操作）

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/plugins.png" width="600" alt="插件管理">

---

### 插件配置编辑器

在插件管理页点击 ⚙ 图标进入。自动解析插件源码，提取可编辑项：

- **Python 常量**：大写模块级变量、`CONFIG` 字典（含 `_env` 包装）
- **dataclass / 构造函数参数**：`config.py` 中的配置类
- **JSON 配置文件**：插件引用的 `.json` 文件，即时生效
- **指令触发词**：修改后重启生效

修改后点击 💾 保存，自动备份原文件（`.bak`）。

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/config-editor.png" width="280" alt="插件编辑器">

---

### 指令列表

自动扫描所有已加载插件（含 `src/plugins/` 本地插件和 pip 安装的外部插件），按类型分类展示全部指令触发词。

支持识别的指令格式见底部「支持的格式」章节。

**QQ 指令：** 无（Web 端查看）

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/commands.png" width="600" alt="指令列表">

---

### 实时日志

WebSocket 推送 Bot 运行日志，支持暂停/继续、自动滚动、错误高亮。

**QQ 指令：** `日志` / `查看日志` / `bot日志` — 以合并转发消息发送最近 30 条日志

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/logs.png" width="600" alt="实时日志">

---

### Bot 连接信息

展示已连接 Bot 的账号信息（昵称、QQ号、头像），以及好友列表、群聊列表、私聊活跃排行。

支持删除好友、退出群聊操作。

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/botinfo.png" width="600" alt="Bot信息">

---

### AI 人设管理

编辑 AI 对话插件的人设提示词（需安装 [nonebot_plugin_aichat_baize](https://github.com/sangonomiya249/nonebot_plugin_aichat_baize)）。支持：

- 📂 公开人设 & 🔒 隐藏人设 双栏切换
- ➕ 新建 / 编辑 / 删除人设
- 🔑 隐藏人设白名单管理
- 💾 保存到 `persona_prompts.json`（即时生效）

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/persona.png" width="600" alt="AI人设">

---

### 帮助模块管理

管理 `/帮助` 图片中各功能模块的展示内容。支持修改帮助图标题、副标题、模块名称、模块颜色、启用状态、插件展示名、插件描述、触发词说明和排序。

> 注意：该功能需要安装配套的 help 插件：[nonebot_plugin_help_baize](https://github.com/sangonomiya249/nonebot_plugin_help_baize)。

- 自动分类 / 单插件模式切换
- 模块排序自动保存
- 帮助图标题与副标题在线编辑
- 保存后用于 `/帮助` 命令渲染

**QQ 指令：** `/帮助` 查看最终渲染效果

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/help.png" width="600" alt="帮助模块">

---

### 指令使用统计

追踪各插件的指令使用频率，支持历史统计和今日统计。

**QQ 指令：**

| 命令 | 功能 |
| ---- | ---- |
| `指令使用统计` / `指令统计` | 历史指令使用统计 |
| `今日指令使用统计` / `今日统计` | 今日指令统计 |

---

### 插件商店

从 NoneBot 官方注册表浏览和安装插件（需要 `httpx`）。支持按名称搜索、按标签筛选，一键安装 pip 包并自动写入 `pyproject.toml`，安装完成后自动热重载。

**QQ 指令：** 无（Web 端操作）

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/store.png" width="600" alt="插件商店">

---

### 下载插件（GitHub 仓库）

从 [webui作者](https://github.com/sangonomiya249) 的 GitHub 仓库直接下载插件到 `src/plugins/` 目录。支持：

- 按名称搜索仓库
- 一键下载/更新插件到本地 plugins 目录
- 更新时只覆盖 `.py` 文件，保留 JSON 配置和数据文件
- 自动清理 `.github`、`tests` 等无关文件

> 通过此方式安装的插件由 `plugin_dirs` 自动加载，不会写入 `pyproject.toml`。

**QQ 指令：** 无（Web 端操作）

<img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/github-plugins.png" width="600" alt="下载插件">

---

### Web UI 控制

**QQ 指令：**

| 命令 | 功能 |
| ---- | ---- |
| `webui` / `webui start` | 启动 Web 服务器 |
| `webui stop` | 停止 Web 服务器 |
| `webui status` | 查看服务器状态 |

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/9.png" width="24" alt=""> 配置项

| 变量 | 默认值 | 说明 |
| ---- | ---- | ---- |
| `WEB_PORT` | `8899` | Web 服务器监听端口 |
| `WEB_HOST` | `0.0.0.0` | Web 服务器监听地址 |

可在 `__init__.py` 中修改。

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/10.png" width="24" alt=""> 依赖

- Python >= 3.10
- nonebot2 >= 2.2.0
- fastapi >= 0.100
- uvicorn >= 0.22
- psutil >= 5.0

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/11.png" width="24" alt=""> 项目结构

```
nonebot_plugin_webui_baize/
├── __init__.py          # 插件入口、NoneBot 指令、启动钩子
├── auth.py              # 登录认证系统
├── templates.py         # HTML 模板（登录页 + 管理面板）
├── app.py               # FastAPI 应用与路由
├── config_editor.py     # 插件配置解析/编辑器
├── pyproject.toml       # 项目构建配置
├── README.md            # 本文档
└── screenshots/         # WebUI 主题资源
```

> GitHub README 预览图位于仓库根目录 `screenshots/`；WebUI 主题资源位于 `nonebot_plugin_webui_baize/screenshots/`。

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/12.png" width="24" alt=""> 插件编辑器 — 支持的格式

插件配置编辑器能够自动识别并编辑以下代码模式：

### 配置常量

| 格式 | 示例 | 说明 |
| ---- | ---- | ---- |
| 模块级常量 | `API_KEY = "sk-xxx"` | 大写常量，自动识别 |
| 字典式配置 | `CONFIG = {"MAX_LEN": 100}` | 支持 `_env("KEY", default)` 包装 |
| dataclass 参数 | 构造函数 `ClassName(key=value)` | `config.py` 中的配置类 |

### 指令触发词

| 格式 | 示例 | 说明 |
| ---- | ---- | ---- |
| on_command | `cmd = on_command("签到")` | 标准斜杠指令 |
| on_fullmatch | `m = on_fullmatch("捞漂流瓶")` | 完全匹配 |
| on_startswith | `m = on_startswith("#")` | 前缀匹配 |
| on_regex | `m = on_regex(r"正则")` | 正则匹配 |
| on_endswith | `m = on_endswith("后缀")` | 后缀匹配 |
| on_alconna | `cmd = on_alconna(Alconna("词云"))` | Alconna 匹配器 |
| 元组触发词 | `on_command(("词1", "词2"))` | 多触发词 |
| 内嵌命令元组 | `("/gif倒放", "action"),` | 函数体内手动解析（on_message 模式） |

### JSON 配置文件

插件源码中通过 `XXX_FILE = "data/xxx.json"` 引用的 JSON 文件会被自动检测并支持在线编辑（即时生效）。

> Python 常量和指令触发词修改后需**重启 Bot** 生效；JSON 配置即时生效。

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/13.png" width="24" alt=""> 鸣谢

登录页动态视觉和部分流萤主题元素参考并使用了 [CuteLeaf/Firefly](https://github.com/CuteLeaf/Firefly) 项目的内容。

## <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/nonebot_plugin_webui_baize/screenshots/14.png" width="24" alt=""> 许可证

MIT License
