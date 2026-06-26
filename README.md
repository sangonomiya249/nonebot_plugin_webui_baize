# nonebot_plugin_webui_baize

NoneBot2 Web UI 管理面板插件，基于 FastAPI 提供 Web 管理界面。

## 📸 预览

<p align="center">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/dashboard.png" width="400" alt="仪表盘">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/plugins.png" width="400" alt="插件管理">
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/commands.png" width="400" alt="指令列表">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/logs.png" width="400" alt="实时日志">
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/persona.png" width="400" alt="AI人设">
  <img src="https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/botinfo.png" width="400" alt="Bot信息">
</p>

## 🚀 快速开始

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

> ⚠️ 首次登录后建议立即修改密码。

## 🎯 功能

### 系统仪表盘

首页概览 Bot 运行状态，包括 CPU / 内存 / 磁盘使用率、运行时间、消息收发统计、管理员列表、Token 用量趋势图（需安装 AI 对话插件）。

**QQ 指令：** 打开 Web UI 后自动刷新

![仪表盘](https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/dashboard.png)

---

### 插件管理

列出所有已加载插件及加载状态。支持：

- ✅ 启用 / 禁用插件（重启生效）
- ✅ 一键启用 / 禁用全部
- 👆 卸载外部插件（pip 安装的）
- 👆 编辑插件配置（见下方「插件配置编辑器」）

**QQ 指令：** 无（Web 端操作）

![插件管理](https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/plugins.png)

---

### 插件配置编辑器

在插件管理页点击 ⚙ 图标进入。自动解析插件源码，提取可编辑项：

- **Python 常量**：大写模块级变量、`CONFIG` 字典（含 `_env` 包装）
- **dataclass / 构造函数参数**：`config.py` 中的配置类
- **JSON 配置文件**：插件引用的 `.json` 文件，即时生效
- **指令触发词**：修改后重启生效

修改后点击 💾 保存，自动备份原文件（`.bak`）。

![插件编辑器](https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/config-editor.png)

---

### 指令列表

自动扫描所有已加载插件（含 `src/plugins/` 本地插件和 pip 安装的外部插件），按类型分类展示全部指令触发词。

支持识别的指令格式见底部「支持的格式」章节。

**QQ 指令：** 无（Web 端查看）

![指令列表](https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/commands.png)

---

### 实时日志

WebSocket 推送 Bot 运行日志，支持暂停/继续、自动滚动、错误高亮。

**QQ 指令：** `日志` / `查看日志` / `bot日志` — 以合并转发消息发送最近 30 条日志

![实时日志](https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/logs.png)

---

### Bot 连接信息

展示已连接 Bot 的账号信息（昵称、QQ号、头像），以及好友列表、群聊列表、私聊活跃排行。

支持删除好友、退出群聊操作。

![Bot信息](https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/botinfo.png)

---

### AI 人设管理

编辑 AI 对话插件的人设提示词（需安装 [nonebot_plugin_aichat_baize](https://github.com/sangonomiya249/nonebot_plugin_aichat_baize)）。支持：

- 📂 公开人设 & 🔒 隐藏人设 双栏切换
- ➕ 新建 / 编辑 / 删除人设
- 🔑 隐藏人设白名单管理
- 💾 保存到 `persona_prompts.json`（即时生效）

![AI人设](https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/persona.png)

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

从 NoneBot 官方注册表浏览和安装插件（需要 `httpx`）。

**QQ 指令：** 无（Web 端操作）

---

### Web UI 控制

**QQ 指令：**

| 命令 | 功能 |
| ---- | ---- |
| `webui` / `webui start` | 启动 Web 服务器 |
| `webui stop` | 停止 Web 服务器 |
| `webui status` | 查看服务器状态 |

## ⚙️ 配置项

| 变量 | 默认值 | 说明 |
| ---- | ---- | ---- |
| `WEB_PORT` | `8899` | Web 服务器监听端口 |
| `WEB_HOST` | `0.0.0.0` | Web 服务器监听地址 |

可在 `__init__.py` 中修改。

## 📦 依赖

- Python >= 3.10
- nonebot2 >= 2.2.0
- fastapi >= 0.100
- uvicorn >= 0.22
- psutil >= 5.0

## 📁 项目结构

```
nonebot_plugin_webui_baize/
├── __init__.py          # 插件入口、NoneBot 指令、启动钩子
├── auth.py              # 登录认证系统
├── templates.py         # HTML 模板（登录页 + 管理面板）
├── app.py               # FastAPI 应用与路由
├── config_editor.py     # 插件配置解析/编辑器
├── pyproject.toml       # 项目构建配置
├── README.md            # 本文档
└── https://raw.githubusercontent.com/sangonomiya249/nonebot_plugin_webui_baize/main/screenshots/         # 参考截图
```

## 📖 插件编辑器 — 支持的格式

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

> ⚠️ Python 常量和指令触发词修改后需**重启 Bot** 生效；JSON 配置即时生效。

## 📄 许可证

MIT License
