# python3
# -*- coding: utf-8 -*-
"""
Web UI HTML 模板
包含登录页面和管理仪表板的 HTML/CSS/JS 模板
"""

# ==================== HTML 模板 ====================

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baize Bot - 登录</title>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --border: #334155; --text: #f1f5f9; --muted: #94a3b8; --accent: #3b82f6; --danger: #ef4444; --success: #22c55e; --radius: 12px; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .login-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 40px; width: 380px; max-width: 95vw; box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
        .login-card h1 { font-size: 22px; text-align: center; margin-bottom: 4px; }
        .login-card .sub { text-align: center; color: var(--muted); font-size: 13px; margin-bottom: 24px; }
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 13px; color: var(--muted); margin-bottom: 4px; }
        .form-group input { width: 100%; padding: 10px 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 14px; }
        .form-group input:focus { border-color: var(--accent); outline: none; }
        .btn { width: 100%; padding: 10px; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; font-weight: 600; }
        .btn-primary { background: var(--accent); color: #fff; }
        .btn-primary:hover { opacity: 0.9; }
        .btn-danger { background: var(--danger); color: #fff; }
        .toast { position: fixed; top: 20px; right: 20px; padding: 10px 18px; border-radius: 6px; color: #fff; font-size: 13px; z-index: 9999; display: none; }
        .toast-error { background: var(--danger); }
        .toast-success { background: var(--success); }
        .toast-info { background: var(--accent); }
        .modal { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: none; align-items: center; justify-content: center; z-index: 10000; }
        .modal-card { background: var(--card); border-radius: var(--radius); padding: 28px; width: 360px; max-width: 95vw; }
        .modal-card h3 { margin-bottom: 12px; font-size: 16px; }
        .modal-card .btn { margin-top: 8px; }
        .skip-link { text-align: center; margin-top: 10px; font-size: 12px; color: var(--muted); cursor: pointer; }
        .skip-link:hover { color: var(--text); }
    </style>
</head>
<body>
    <div class="login-card">
        <h1>🤖 Baize Bot</h1>
        <div class="sub">Web UI 管理面板</div>
        <div class="form-group">
            <label>用户名</label>
            <input type="text" id="username" value="admin" placeholder="admin">
        </div>
        <div class="form-group">
            <label>密码</label>
            <input type="password" id="password" placeholder="请输入密码" onkeydown="if(event.key==='Enter')doLogin()">
        </div>
        <button class="btn btn-primary" onclick="doLogin()">登 录</button>
        <div style="text-align:center;margin-top:12px;font-size:11px;color:var(--muted);">默认账号: admin / 密码: admin</div>
    </div>

    <div class="modal" id="pw-modal">
        <div class="modal-card">
            <h3>🔐 修改默认密码</h3>
            <p style="font-size:13px;color:var(--muted);margin-bottom:12px;">检测到首次登录，建议修改默认密码</p>
            <div class="form-group">
                <label>新密码（至少 6 位）</label>
                <input type="password" id="new-pw" placeholder="新密码" onkeydown="if(event.key==='Enter')doChangePw()">
            </div>
            <button class="btn btn-primary" onclick="doChangePw()">确认修改</button>
            <div class="skip-link" onclick="skipChangePw()">暂不修改，直接进入</div>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let authToken = '';
        function showToast(msg, type) { const t = document.getElementById('toast'); t.textContent = msg; t.className = 'toast toast-' + type; t.style.display = 'block'; setTimeout(function(){ t.style.display = 'none'; }, 3000); }
        async function doLogin() {
            const u = document.getElementById('username').value, p = document.getElementById('password').value;
            try {
                const r = await fetch('/api/login', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username: u, password: p}) });
                const d = await r.json();
                if (r.ok && d.success) {
                    authToken = d.token;
                    sessionStorage.setItem('lhc_token', authToken);
                    if (d.first_login) {
                        document.getElementById('pw-modal').style.display = 'flex';
                    } else {
                        location.reload();
                    }
                } else { showToast(d.error || '登录失败', 'error'); }
            } catch(e) { showToast('请求失败: ' + e.message, 'error'); }
        }
        async function doChangePw() {
            const pw = document.getElementById('new-pw').value;
            if (pw.length < 6) { showToast('密码至少 6 位', 'error'); return; }
            try {
                const r = await fetch('/api/change-password', { method: 'POST', headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}, body: JSON.stringify({new_password: pw}) });
                const d = await r.json();
                if (r.ok && d.success) { showToast('密码已修改', 'success'); document.getElementById('pw-modal').style.display = 'none'; location.reload(); }
                else { showToast(d.error || '修改失败', 'error'); }
            } catch(e) { showToast('请求失败', 'error'); }
        }
        function skipChangePw() { document.getElementById('pw-modal').style.display = 'none'; location.reload(); }
    </script>
</body>
</html>"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baize Bot - 管理面板</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>">
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --border: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --cyan: #06b6d4;
            --purple: #a855f7;
            --radius: 12px;
            --radius-sm: 8px;
            --shadow: 0 4px 6px -1px rgba(0,0,0,0.3), 0 2px 4px -2px rgba(0,0,0,0.3);
            --transition: all 0.2s ease;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }
        /* 侧边栏 */
        .sidebar {
            position: fixed;
            left: 0; top: 0; bottom: 0;
            width: 240px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            padding: 20px 0;
            overflow-y: auto;
            z-index: 100;
        }
        .sidebar-logo {
            padding: 0 20px 20px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .sidebar-logo .logo-icon {
            width: 40px; height: 40px;
            background: linear-gradient(135deg, var(--accent), var(--purple));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
        }
        .sidebar-logo h1 { font-size: 16px; font-weight: 600; }
        .sidebar-logo .ver { font-size: 11px; color: var(--text-muted); }
        .nav-item {
            display: flex; align-items: center; gap: 10px;
            padding: 10px 20px; margin: 2px 10px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            color: var(--text-secondary);
            transition: var(--transition);
            font-size: 14px;
            user-select: none;
        }
        .nav-item:hover { background: var(--bg-hover); color: var(--text-primary); }
        .nav-item.active {
            background: var(--accent);
            color: #fff;
        }
        .nav-item .nav-icon { font-size: 18px; width: 24px; text-align: center; }
        .nav-divider {
            border-top: 1px solid var(--border);
            margin: 8px 20px;
        }
        .nav-label {
            padding: 8px 20px 4px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
        }
        /* 主内容 */
        .main {
            margin-left: 240px;
            padding: 28px 32px;
            min-height: 100vh;
        }
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        .page-header {
            margin-bottom: 24px;
        }
        .page-header h2 { font-size: 24px; font-weight: 700; }
        .page-header p { color: var(--text-secondary); font-size: 14px; margin-top: 4px; }
        /* 卡片网格 */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            transition: var(--transition);
        }
        .stat-card:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: var(--shadow); }
        .stat-card-header {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 12px;
        }
        .stat-card-title {
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 500;
        }
        .stat-card-icon {
            width: 32px; height: 32px;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 16px;
        }
        .stat-card-value {
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .stat-card-sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }
        /* 进度条 */
        .progress-bar {
            height: 6px;
            background: var(--bg-primary);
            border-radius: 3px;
            margin-top: 8px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.6s ease;
        }
        .progress-fill.green { background: var(--success); }
        .progress-fill.blue { background: var(--accent); }
        .progress-fill.yellow { background: var(--warning); }
        .progress-fill.red { background: var(--danger); }
        .progress-fill.purple { background: var(--purple); }
        /* 表格 */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
            margin-bottom: 20px;
        }
        .card-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card-header h3 { font-size: 15px; font-weight: 600; }
        .card-body { padding: 0; overflow-x: auto; }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px 16px;
            text-align: left;
            font-size: 13px;
        }
        th {
            background: var(--bg-primary);
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }
        td { border-top: 1px solid var(--border); }
        tr:hover td { background: var(--bg-hover); }
        tr.disabled-row td { opacity: 0.5; }
        tr.disabled-row:hover td { opacity: 0.75; background: var(--bg-hover); }
        /* 标签 */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 100px;
            font-size: 11px;
            font-weight: 600;
        }
        .badge-success { background: rgba(34,197,94,0.15); color: var(--success); }
        .badge-warning { background: rgba(245,158,11,0.15); color: var(--warning); }
        .badge-danger { background: rgba(239,68,68,0.15); color: var(--danger); }
        .badge-info { background: rgba(59,130,246,0.15); color: var(--accent); }
        .badge-purple { background: rgba(168,85,247,0.15); color: var(--purple); }
        /* 按钮 */
        .btn {
            padding: 7px 16px;
            border: 1px solid var(--border);
            background: var(--bg-secondary);
            color: var(--text-primary);
            border-radius: var(--radius-sm);
            cursor: pointer;
            font-size: 13px;
            transition: var(--transition);
            white-space: nowrap;
        }
        .btn:hover { background: var(--bg-hover); }
        .btn-primary { background: var(--accent); border-color: var(--accent); color: #fff; }
        .btn-primary:hover { background: var(--accent-hover); }
        .btn-sm { padding: 4px 10px; font-size: 12px; }
        /* 日志区 */
        .log-container {
            background: #0a0e1a;
            border-radius: var(--radius-sm);
            padding: 16px;
            height: 450px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
            font-size: 12px;
            line-height: 1.8;
        }
        .log-line { white-space: pre-wrap; word-break: break-all; }
        .log-line.info { color: #e2e8f0; }
        .log-line.warning { color: #fbbf24; }
        .log-line.error { color: #f87171; }
        .log-line.debug { color: #818cf8; }
        .log-line.success { color: #4ade80; }
        /* 响应式 */
        /* 浅色主题 */
        body.light-theme {
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --bg-hover: #f1f5f9;
            --border: #e2e8f0;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
        }
        body.light-theme .log-container { background: #f1f5f9; }
        body.light-theme .config-item-input input, body.light-theme .config-item-input select { background: #f8fafc; }
        /* 主题切换按钮 */
        .theme-toggle {
            position: fixed; bottom: 20px; left: 20px; z-index: 200;
            width: 36px; height: 36px; border-radius: 50%;
            background: var(--bg-card); border: 1px solid var(--border);
            color: var(--text-primary); cursor: pointer; font-size: 16px;
            display: flex; align-items: center; justify-content: center;
            transition: var(--transition);
        }
        .theme-toggle:hover { border-color: var(--accent); }
        /* 汉堡菜单按钮 */
        .hamburger {
            display: none; position: fixed; top: 12px; left: 12px; z-index: 300;
            width: 36px; height: 36px; border-radius: 8px;
            background: var(--accent); border: none; color: #fff;
            font-size: 18px; cursor: pointer;
        }
        /* 移动端适配 */
        @media (max-width: 768px) {
            .hamburger { display: flex; align-items: center; justify-content: center; }
            .sidebar {
                transform: translateX(-100%);
                width: 220px; padding: 12px 0;
                transition: transform 0.25s ease;
            }
            .sidebar.open { transform: translateX(0); }
            .sidebar-logo { padding: 0 16px 12px; }
            .sidebar-logo h1, .sidebar-logo .ver, .nav-item span:not(.nav-icon), .nav-label { display: block; }
            .nav-item { justify-content: flex-start; padding: 10px 16px; margin: 2px 8px; }
            .main { margin-left: 0 !important; padding: 56px 12px 16px !important; }
            .stat-grid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }
            .stat-card { padding: 14px; }
            .stat-card-value { font-size: 22px; }
            table { font-size: 11px; }
            th, td { padding: 6px 8px; }
            .config-modal { width: 95vw !important; }
            .page-header { flex-direction: column; align-items: flex-start; gap: 8px; }
            .page-header .btn, .page-header > div { width: 100%; }
            .theme-toggle { bottom: 16px; left: auto; right: 16px; }
        }
        /* 侧边栏遮罩 */
        .sidebar-overlay {
            display: none; position: fixed; inset: 0; z-index: 99;
            background: rgba(0,0,0,0.3);
        }
        @media (max-width: 768px) {
            .sidebar-overlay.show { display: block; }
        }
        /* 脉冲动画 */
        .pulse {
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--success);
            display: inline-block;
            animation: pulse 2s infinite;
            margin-right: 6px;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        .status-dot { display: flex; align-items: center; gap: 6px; }
        /* Toast */
        .toast {
            position: fixed;
            top: 20px; right: 20px;
            padding: 12px 20px;
            border-radius: var(--radius-sm);
            color: #fff;
            font-size: 14px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
            box-shadow: var(--shadow);
        }
        @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        .toast-success { background: var(--success); }
        .toast-error { background: var(--danger); }
        .toast-info { background: var(--accent); }
        /* 配置编辑弹窗 */
        .config-overlay {
            position: fixed; inset: 0;
            background: rgba(0,0,0,0.6);
            display: flex; align-items: center; justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(2px);
        }
        .config-modal {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            width: 560px; max-width: 95vw; max-height: 80vh;
            display: flex; flex-direction: column;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: fadeIn 0.2s ease;
        }
        .config-modal-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between;
        }
        .config-modal-header h3 { font-size: 16px; }
        .config-modal-body {
            padding: 16px 20px;
            overflow-y: auto;
            flex: 1;
        }
        .config-modal-footer {
            padding: 12px 20px;
            border-top: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between;
        }
        .config-item {
            display: flex; align-items: flex-start; gap: 12px;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
        }
        .config-item:last-child { border-bottom: none; }
        .config-item-label {
            min-width: 140px;
            font-size: 13px; font-weight: 600;
            color: var(--text-primary);
            word-break: break-all;
        }
        .config-item-input {
            flex: 1;
            display: flex; flex-direction: column; gap: 4px;
        }
        .config-item-input input, .config-item-input select {
            background: var(--bg-primary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
            font-family: inherit;
            width: 100%;
            box-sizing: border-box;
        }
        .config-item-input input:focus { border-color: var(--accent); outline: none; }
        .config-item-comment {
            font-size: 11px;
            color: var(--text-muted);
        }
        .config-item-type {
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            background: var(--bg-primary);
            color: var(--text-muted);
            white-space: nowrap;
        }
        /* 刷新按钮 */
        .refresh-indicator {
            display: inline-block;
            transition: transform 0.5s ease;
            cursor: pointer;
        }
        .refresh-indicator.spinning { transform: rotate(360deg); }
        .flex-between { display: flex; align-items: center; justify-content: space-between; }
        .gap-8 { gap: 8px; }
        /* AI人设管理 */
        .persona-tab {
            padding: 10px 20px;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
        }
        .persona-tab:hover { color: var(--text-primary); border-bottom-color: var(--border); }
        .persona-tab.active {
            color: var(--accent);
            border-bottom-color: var(--accent);
        }
        .persona-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
        }
        .persona-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            user-select: none;
        }
        .persona-card-header:hover { background: var(--bg-hover); }
        .persona-card-header .collapse-icon {
            transition: transform 0.2s;
            font-size: 12px;
        }
        .persona-card.collapsed .collapse-icon { transform: rotate(-90deg); }
        .persona-card.collapsed .persona-card-body { display: none; }
        .persona-card-body {
            padding: 16px;
        }
        .persona-field {
            margin-bottom: 12px;
        }
        .persona-field:last-child { margin-bottom: 0; }
        .persona-field label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .persona-field input,
        .persona-field textarea {
            width: 100%;
            padding: 8px 12px;
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 13px;
            font-family: inherit;
            transition: border-color 0.2s;
            box-sizing: border-box;
        }
        .persona-field input:focus,
        .persona-field textarea:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
        }
        .persona-field textarea {
            min-height: 120px;
            max-height: 400px;
            resize: vertical;
            line-height: 1.6;
            font-size: 13px;
        }
        .persona-field .field-hint {
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 2px;
        }
        .whitelist-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        .whitelist-row input {
            flex: 1;
            padding: 6px 10px;
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 13px;
        }
        .whitelist-row input:focus {
            outline: none;
            border-color: var(--accent);
        }
        .whitelist-tag {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 8px;
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: 12px;
            margin: 2px 4px 2px 0;
        }
        .whitelist-tag .remove-tag {
            cursor: pointer;
            color: var(--danger);
            font-weight: bold;
            margin-left: 2px;
        }
    </style>
</head>
<body>
    <!-- 汉堡菜单 + 侧边栏遮罩 -->
    <button class="hamburger" onclick="toggleSidebar()" title="菜单">☰</button>
    <div class="sidebar-overlay" id="sidebar-overlay" onclick="toggleSidebar()"></div>
    <!-- 主题切换 -->
    <button class="theme-toggle" onclick="toggleTheme()" title="切换主题" id="theme-btn">🌙</button>
    <!-- 侧边栏 -->
    <aside class="sidebar">
        <div class="sidebar-logo">
            <div class="logo-icon">🤖</div>
            <div>
                <h1>Baize Bot</h1>
                <div class="ver">v2.4.4 · Web UI</div>
            </div>
        </div>
        <div class="nav-label">主菜单</div>
        <div class="nav-item active" data-page="dashboard">
            <span class="nav-icon">📊</span> 仪表盘
        </div>
        <div class="nav-item" data-page="plugins">
            <span class="nav-icon">🧩</span> 插件管理
        </div>
        <div class="nav-item" data-page="bots">
            <span class="nav-icon">🔗</span> Bot 连接
        </div>
        <div class="nav-divider"></div>
        <div class="nav-label">工具</div>
        <div class="nav-item" data-page="logs">
            <span class="nav-icon">📜</span> 实时日志
        </div>
        <div class="nav-item" data-page="commands">
            <span class="nav-icon">📋</span> 指令列表
        </div>
        <div class="nav-item" data-page="bot-info">
            <span class="nav-icon">👤</span> 用户配置
        </div>
        <div class="nav-item" data-page="persona" id="nav-persona" style="display:none;">
            <span class="nav-icon">🎭</span> AI人设
        </div>
        <div class="nav-item" data-page="help-page">
            <span class="nav-icon">📖</span> 使用帮助
        </div>
        <div class="nav-item" data-page="store">
            <span class="nav-icon">🛒</span> 插件商店
        </div>
        <div class="nav-item" data-page="about">
            <span class="nav-icon">ℹ️</span> 关于
        </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main">
        <!-- 仪表盘 -->
        <div class="page active" id="page-dashboard">
            <div class="page-header flex-between">
                <div>
                    <h2>📊 仪表盘</h2>
                    <p>系统状态总览</p>
                </div>
                <div style="display:flex;gap:6px;">
                    <button class="btn" onclick="refreshAll()" title="刷新数据">🔄 刷新</button>
                    <button class="btn" onclick="restartBot()" title="重启机器人" style="color:var(--danger);border-color:var(--danger);">⏻ 重启</button>
                </div>
            </div>
            <div class="stat-grid" id="stat-grid">
                <div class="stat-card"><div class="stat-card-header"><span class="stat-card-title">加载中...</span></div></div>
            </div>
            <div class="card" style="margin-bottom:20px;">
                <div class="card-header flex-between">
                    <h3>👑 管理员</h3>
                    <span style="font-size:12px;color:var(--text-muted);">仅管理员可使用 Web UI 指令</span>
                </div>
                <div class="card-body" style="padding:12px 16px;">
                    <div style="display:flex;gap:8px;margin-bottom:8px;">
                        <input type="text" id="admin-qq-input" placeholder="输入 QQ 号" style="background:var(--bg-primary);border:1px solid var(--border);color:var(--text-primary);padding:5px 10px;border-radius:6px;font-size:13px;width:160px;">
                        <button class="btn btn-sm btn-primary" onclick="addAdmin()">➕ 添加</button>
                    </div>
                    <div id="admin-list" style="display:flex;flex-wrap:wrap;gap:6px;">
                        <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                    </div>
                </div>
            </div>
            <!-- Token 用量统计 -->
            <div class="card" style="margin-bottom:20px;display:none;" id="token-card">
                <div class="card-header flex-between">
                    <h3>📈 Token 用量统计</h3>
                    <span style="font-size:12px;color:var(--text-muted);">近 14 天</span>
                </div>
                <div class="card-body" style="padding:16px;">
                    <!-- 统计卡片 -->
                    <div class="stat-grid" style="grid-template-columns:repeat(6,1fr);margin-bottom:16px;" id="token-summary-cards">
                        <div class="stat-card"><div class="stat-card-title">累计 Token</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title">今日 Token</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title">累计调用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title">今日调用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title">累计费用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title">今日费用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                    </div>
                    <!-- 柱状图 -->
                    <div id="token-chart" style="display:flex;align-items:flex-end;gap:6px;height:160px;padding:0 4px;position:relative;overflow-x:auto;">
                        <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                    </div>
                    <!-- 图例 -->
                    <div style="display:flex;gap:20px;margin-top:8px;justify-content:center;font-size:12px;">
                        <span>🟦 输入 Token</span>
                        <span>🟧 输出 Token</span>
                        <span style="color:var(--success);">×N 调用次数</span>
                    </div>
                </div>
            </div>
            <div class="card" style="margin-bottom:20px;">
                <div class="card-header flex-between">
                    <h3>📊 指令使用统计</h3>
                    <span style="font-size:12px;color:var(--text-muted);" id="cmd-stats-total">--</span>
                </div>
                <div class="card-body" id="cmd-stats-table">
                    <div style="padding:20px;text-align:center;color:var(--text-muted);">加载中...</div>
                </div>
            </div>
            <div class="card">
                <div class="card-header"><h3>📋 系统信息</h3></div>
                <div class="card-body" id="sysinfo-table"></div>
            </div>
        </div>

        <!-- 插件管理 -->
        <div class="page" id="page-plugins">
            <div class="page-header flex-between">
                <div>
                    <h2>🧩 插件管理</h2>
                    <p>查看已加载插件信息</p>
                </div>
                <div style="display:flex;gap:6px;">
                    <button class="btn btn-sm" onclick="toggleAllPlugins(true)" title="启用所有已禁用的插件">▶ 一键启用</button>
                    <button class="btn btn-sm" onclick="toggleAllPlugins(false)" title="禁用所有已启用的插件" style="color:var(--danger);">⏸ 一键禁用</button>
                    <button class="btn" onclick="loadPlugins()">🔄 刷新</button>
                </div>
            </div>
            <div class="card">
                <div class="card-header flex-between">
                    <h3>已加载插件列表</h3>
                    <span style="font-size:13px;color:var(--text-muted)" id="plugin-count">--</span>
                </div>
                <div class="card-body" id="plugin-table"></div>
            </div>
        </div>

        <!-- Bot 连接 -->
        <div class="page" id="page-bots">
            <div class="page-header flex-between">
                <div>
                    <h2>🔗 Bot 连接</h2>
                    <p>查看已连接的机器人实例</p>
                </div>
                <button class="btn" onclick="loadBots()">🔄 刷新</button>
            </div>
            <div class="card">
                <div class="card-header"><h3>在线 Bot 列表</h3></div>
                <div class="card-body" id="bot-table"></div>
            </div>
        </div>

        <!-- 日志 -->
        <div class="page" id="page-logs">
            <div class="page-header flex-between">
                <div>
                    <h2>📜 实时日志</h2>
                    <p>最近 200 条系统日志（每 3 秒自动刷新）</p>
                </div>
                <div style="display:flex;gap:8px;">
                    <button class="btn btn-sm" onclick="toggleAutoRefresh()" id="btn-auto-refresh">⏸ 暂停</button>
                    <button class="btn btn-sm" onclick="clearLogs()">🗑 清屏</button>
                    <button class="btn btn-sm" onclick="loadLogs()">🔄 刷新</button>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <div class="log-container" id="log-container">
                        <div class="log-line info">正在加载日志...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 指令列表 -->
        <div class="page" id="page-commands">
            <div class="page-header flex-between">
                <div>
                    <h2>📋 指令列表</h2>
                    <p>自动扫描所有本地插件，按类型分类展示全部指令触发词</p>
                </div>
                <button class="btn" onclick="loadCommands()">🔄 刷新</button>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3>⌨️ on_command（指令）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_command">--</span></div>
                <div class="card-body" id="cmd-table-on_command"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3>🎯 on_fullmatch（全匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_fullmatch">--</span></div>
                <div class="card-body" id="cmd-table-on_fullmatch"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3>✨ on_alconna（Alconna）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_alconna">--</span></div>
                <div class="card-body" id="cmd-table-on_alconna"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3>🔤 on_startswith（前缀匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_startswith">--</span></div>
                <div class="card-body" id="cmd-table-on_startswith"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3>🔍 on_regex（正则匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_regex">--</span></div>
                <div class="card-body" id="cmd-table-on_regex"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3>🔤 on_endswith（后缀匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_endswith">--</span></div>
                <div class="card-body" id="cmd-table-on_endswith"></div>
            </div>
            <div class="card">
                <div class="card-header"><h3>💬 on_message（消息触发）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_message">--</span></div>
                <div class="card-body" id="cmd-table-on_message"></div>
            </div>
        </div>

        <!-- 插件商店 -->
        <div class="page" id="page-store">
            <div class="page-header flex-between">
                <div>
                    <h2>🛒 插件商店</h2>
                    <p>浏览并安装 NoneBot 插件商店的插件（数据来源：registry.nonebot.dev）</p>
                </div>
                <div style="display:flex;gap:8px;">
                    <input type="text" id="store-search" placeholder="搜索插件..." style="background:var(--bg-primary);border:1px solid var(--border);color:var(--text-primary);padding:6px 12px;border-radius:6px;font-size:13px;width:180px;" oninput="searchStore()">
                    <button class="btn btn-sm" onclick="loadStore()">🔄 刷新</button>
                </div>
            </div>
            <div id="store-status" style="margin-bottom:12px;font-size:13px;color:var(--text-muted);">加载中...</div>
            <div id="store-list"></div>
        </div>

        <!-- Bot 用户信息 -->
        <div class="page" id="page-bot-info">
            <div class="page-header flex-between">
                <div>
                    <h2>👤 用户配置</h2>
                    <p>Bot 账号信息总览</p>
                </div>
                <button class="btn" onclick="loadBotInfo()">🔄 刷新</button>
            </div>
            <div id="bot-info-content" style="display:flex;gap:24px;flex-wrap:wrap;">
                <div class="stat-card" style="flex:1;min-width:280px;text-align:center;">
                    <img id="bot-avatar" src="" style="width:100px;height:100px;border-radius:50%;margin-bottom:12px;background:var(--bg-primary);" onerror="this.style.display='none'">
                    <div style="font-size:20px;font-weight:700;" id="bot-nickname">--</div>
                    <div style="font-size:13px;color:var(--text-muted);" id="bot-qq">QQ: --</div>
                </div>
                <div style="flex:2;min-width:300px;display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                    <div class="stat-card" style="cursor:pointer;" onclick="showDetailModal('friends')">
                        <div class="stat-card-title">👥 好友数量（点击查看）</div>
                        <div class="stat-card-value" id="bot-friends">--</div>
                    </div>
                    <div class="stat-card" style="cursor:pointer;" onclick="showDetailModal('groups')">
                        <div class="stat-card-title">💬 群聊数量（点击查看）</div>
                        <div class="stat-card-value" id="bot-groups">--</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-title">📥 接收消息</div>
                        <div class="stat-card-value" id="bot-msg-recv">--</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-title">📤 发送消息</div>
                        <div class="stat-card-value" id="bot-msg-sent">--</div>
                    </div>
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <div class="card-header"><h3>📩 私聊排行 Top 10</h3></div>
                <div class="card-body" style="padding:12px 16px;" id="top-users-list">
                    <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                </div>
            </div>
        </div>

        <!-- AI人设管理 -->
        <div class="page" id="page-persona">
            <div class="page-header flex-between">
                <div>
                    <h2>🎭 AI人设管理</h2>
                    <p>管理对话机器人的人设提示词（persona_prompts.json）</p>
                </div>
                <div style="display:flex;gap:6px;">
                    <button class="btn" onclick="loadPersona()" title="重新加载">🔄 刷新</button>
                    <button class="btn btn-primary" onclick="savePersona()" title="保存修改">💾 保存</button>
                </div>
            </div>
            <!-- 栏目切换 Tab -->
            <div style="display:flex;gap:8px;margin-bottom:16px;border-bottom:2px solid var(--border);padding-bottom:0;align-items:flex-end;justify-content:space-between;">
                <div style="display:flex;gap:8px;">
                    <button class="persona-tab active" onclick="switchPersonaTab('public')" id="tab-public">
                        📂 公开人设 (persona_catalog)
                    </button>
                    <button class="persona-tab" onclick="switchPersonaTab('hidden')" id="tab-hidden">
                        🔒 隐藏人设 (hidden_persona_catalog)
                    </button>
                </div>
                <div style="display:flex;gap:6px;padding-bottom:8px;">
                    <button class="btn btn-sm btn-primary" onclick="showCreatePersonaModal('public')" id="btn-create-public">➕ 新建公开人设</button>
                    <button class="btn btn-sm" onclick="showCreatePersonaModal('hidden')" id="btn-create-hidden" style="display:none;">➕ 新建隐藏人设</button>
                </div>
            </div>
            <!-- 人设编辑区域 -->
            <div id="persona-editor" style="display:flex;flex-direction:column;gap:16px;">
                <span style="color:var(--text-muted);font-size:13px;">加载中...</span>
            </div>
            <!-- 隐藏人设白名单区域 -->
            <div id="persona-whitelist-section" style="display:none;margin-top:24px;">
                <div class="card">
                    <div class="card-header"><h3>🔑 隐藏人设专属白名单</h3></div>
                    <div class="card-body" style="padding:12px 16px;" id="persona-whitelist-editor">
                        <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                    </div>
                </div>
            </div>
            <!-- 新建人设弹窗 -->
            <div id="create-persona-overlay" class="config-overlay" style="display:none;" onclick="if(event.target===this)closeCreatePersonaModal()">
                <div class="config-modal" style="max-width:600px;">
                    <div class="config-modal-header">
                        <h3 id="create-persona-title">➕ 新建人设</h3>
                        <button class="btn btn-sm" onclick="closeCreatePersonaModal()" style="color:var(--text-muted);">✕</button>
                    </div>
                    <div class="config-modal-body">
                        <div class="persona-field">
                            <label>人设 ID (key) <span id="create-key-hint" class="field-hint"></span></label>
                            <input type="text" id="create-persona-key" placeholder="">
                        </div>
                        <div class="persona-field">
                            <label>名称 (name)</label>
                            <input type="text" id="create-persona-name" placeholder="例如：白钰袖温柔版">
                        </div>
                        <div class="persona-field">
                            <label>显示名称 (display_model)</label>
                            <input type="text" id="create-persona-display" placeholder="例如：白钰袖">
                        </div>
                        <div class="persona-field">
                            <label>描述 (description)</label>
                            <input type="text" id="create-persona-desc" placeholder="例如：风灵玉秀-白钰袖人设">
                        </div>
                        <div class="persona-field">
                            <label>系统提示词 (system_prompt)</label>
                            <textarea id="create-persona-prompt" placeholder="例如：你是白钰袖，来自风灵玉秀世界。你性格温柔善良...&#10;请始终保持角色设定，用中文回复。"></textarea>
                        </div>
                    </div>
                    <div class="config-modal-footer">
                        <button class="btn" onclick="closeCreatePersonaModal()">取消</button>
                        <button class="btn btn-primary" onclick="confirmCreatePersona()">✅ 确认创建</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 使用帮助 -->
        <div class="page" id="page-help-page">
            <div class="page-header">
                <h2>📖 使用帮助</h2>
                <p>Web UI 管理面板功能说明</p>
            </div>
            <div class="stat-grid" style="margin-bottom:20px;">
                <div class="stat-card">
                    <div class="stat-card-title">📊 仪表盘</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看 CPU/内存/磁盘/运行时间<br>消息收发统计<br>指令使用排行（今日+历史）</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">🧩 插件管理</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看所有插件及加载状态<br>启用/禁用插件（重启生效）<br>编辑插件配置（常量+JSON）<br>修改指令触发词<br>安装/卸载插件（插件商店）<br>一键启用/禁用全部插件</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">📜 实时日志</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看最近 200 条系统日志<br>3 秒自动刷新<br>等级颜色区分</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">📋 指令列表</div>
                    <div class="stat-card-sub" style="line-height:1.8;">自动扫描所有插件的指令<br>按类型分类展示<br>支持 on_command / fullmatch / alconna / startswith 等</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">👤 用户配置</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看 Bot QQ 号/头像<br>好友列表（可删除好友）<br>群聊列表（可退出群聊）</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">🛒 插件商店</div>
                    <div class="stat-card-sub" style="line-height:1.8;">浏览 NoneBot 注册表插件<br>搜索 + 一键安装<br>安装后自动写入 pyproject.toml</div>
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <div class="card-header"><h3>⌨️ 快捷指令</h3></div>
                <div class="card-body">
                    <table>
                        <tr><td style="font-weight:600;width:200px;">webui / webui start</td><td>启动/查看 Web UI 状态</td></tr>
                        <tr><td style="font-weight:600;">webui stop</td><td>停止 Web UI 服务器</td></tr>
                        <tr><td style="font-weight:600;">/日志 / 查看日志</td><td>查看最近 Bot 日志（合并转发）</td></tr>
                        <tr><td style="font-weight:600;">/指令使用统计</td><td>查看历史指令使用排行（合并转发）</td></tr>
                        <tr><td style="font-weight:600;">/今日指令使用统计</td><td>查看今日指令使用排行（合并转发）</td></tr>
                    </table>
                </div>
            </div>
        </div>

        <!-- 关于 -->
        <div class="page" id="page-about">
            <div class="page-header">
                <h2>ℹ️ 关于</h2>
                <p>关于 Baize Bot & Web UI 管理面板</p>
            </div>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title">🤖 机器人框架</span></div>
                    <div style="font-size:18px;font-weight:600;">NoneBot v2</div>
                    <div class="stat-card-sub">异步 Python 机器人框架</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title">🔌 适配器</span></div>
                    <div style="font-size:18px;font-weight:600;">OneBot V11</div>
                    <div class="stat-card-sub">go-cqhttp / LLOneBot</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title">🌐 Web 框架</span></div>
                    <div style="font-size:18px;font-weight:600;">FastAPI</div>
                    <div class="stat-card-sub">高性能异步 Web 框架</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title">📝 作者</span></div>
                    <div style="font-size:18px;font-weight:600;">lhc</div>
                    <div class="stat-card-sub">2491434931@qq.com</div>
                </div>
            </div>
            <div class="card" style="margin-top:20px;">
                <div class="card-header"><h3>📋 API 接口列表</h3></div>
                <div class="card-body">
                    <table>
                        <thead><tr><th>接口</th><th>方法</th><th>描述</th></tr></thead>
                        <tbody>
                            <tr><td>/api/status</td><td>GET</td><td>获取系统状态信息</td></tr>
                            <tr><td>/api/plugins</td><td>GET</td><td>获取插件列表</td></tr>
                            <tr><td>/api/bots</td><td>GET</td><td>获取在线 Bot 列表</td></tr>
                            <tr><td>/api/logs</td><td>GET</td><td>获取最近日志</td></tr>
                            <tr><td>/api/ping</td><td>GET</td><td>健康检查</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </main>

    <!-- 配置编辑弹窗 -->
    <div class="config-overlay" id="config-overlay" style="display:none;" onclick="if(event.target===this)hideConfigEditor()">
        <div class="config-modal">
            <div class="config-modal-header">
                <h3 id="config-modal-title">⚙ 插件配置</h3>
                <button class="btn btn-sm" onclick="hideConfigEditor()">✕ 关闭</button>
            </div>
            <div class="config-modal-body" id="config-modal-body">
                <div style="text-align:center;padding:40px;color:var(--text-muted);">加载中...</div>
            </div>
            <div class="config-modal-footer">
                <span style="font-size:11px;color:var(--text-muted);">⚠ 修改后需重启 Bot 生效</span>
                <div style="display:flex;gap:8px;">
                    <button class="btn" onclick="hideConfigEditor()">取消</button>
                    <button class="btn btn-primary" id="btn-save-config" onclick="saveConfig()">💾 保存配置</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 好友/群聊详情弹窗 -->
    <div class="config-overlay" id="detail-overlay" style="display:none;" onclick="if(event.target===this)hideDetailModal()">
        <div class="config-modal" style="max-height:70vh;">
            <div class="config-modal-header">
                <h3 id="detail-modal-title">详情</h3>
                <button class="btn btn-sm" onclick="hideDetailModal()">✕ 关闭</button>
            </div>
            <div class="config-modal-body" id="detail-modal-body" style="max-height:55vh;"></div>
        </div>
    </div>

    <!-- Toast -->
    <div id="toast" class="toast" style="display:none;"></div>

    <script>
        let autoRefresh = true;
        let autoRefreshTimer = null;
        let tokenRefreshTimer = null;

        // ====== 主题切换 ======
        (function() {
            const saved = localStorage.getItem('lhc_theme');
            if (saved === 'light') {
                document.body.classList.add('light-theme');
                document.getElementById('theme-btn').textContent = '☀️';
            }
        })();
        function toggleTheme() {
            const body = document.body;
            const btn = document.getElementById('theme-btn');
            body.classList.toggle('light-theme');
            const isLight = body.classList.contains('light-theme');
            btn.textContent = isLight ? '☀️' : '🌙';
            localStorage.setItem('lhc_theme', isLight ? 'light' : 'dark');
        }

        // ====== 移动端侧边栏 ======
        function toggleSidebar() {
            document.querySelector('.sidebar').classList.toggle('open');
            document.getElementById('sidebar-overlay').classList.toggle('show');
        }
        // 点击导航项后自动关闭侧边栏（移动端）
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.nav-item').forEach(function(item) {
                item.addEventListener('click', function() {
                    if (window.innerWidth <= 768) {
                        toggleSidebar();
                    }
                });
            });
        });

        // ====== 导航 ======
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                const page = item.dataset.page;
                document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
                document.getElementById('page-' + page).classList.add('active');
                if (page === 'dashboard') { refreshAll(); startTokenRefresh(); }
                else if (page === 'plugins') { loadPlugins(); stopTokenRefresh(); }
                else if (page === 'bots') { loadBots(); stopTokenRefresh(); }
                else if (page === 'logs') { loadLogs(); startAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'commands') { loadCommands(); stopAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'bot-info') { loadBotInfo(); stopAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'persona') {
                    if (!_aichatAvailable) {
                        document.getElementById('page-persona').innerHTML = '<div style="text-align:center;padding:60px;color:var(--text-muted);"><h3>📦 未检测到 AI 对话插件</h3><p style="margin-top:12px;">需要安装 nonebot_plugin_aichat_baize 才能使用 AI 人设管理功能</p></div>';
                    } else {
                        loadPersona();
                    }
                    stopAutoRefresh(); stopTokenRefresh();
                }
                else if (page === 'help-page') { stopAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'store') { loadStore(); stopAutoRefresh(); stopTokenRefresh(); }
                else { stopAutoRefresh(); stopTokenRefresh(); }
            });
        });

        async function restartBot() {
            if (!confirm('确定要重启机器人吗？\n\nBot 进程将退出并由进程管理器自动拉起。')) return;
            showToast('⏳ Bot 即将重启...', 'info');
            try {
                await postApi('/api/restart', {});
            } catch (e) {
                // 进程退出时 fetch 会失败，这是正常的
            }
        }

        // ====== Toast ======
        function showToast(msg, type = 'info') {
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.className = 'toast toast-' + type;
            t.style.display = 'block';
            setTimeout(() => { t.style.display = 'none'; }, 2500);
        }

        // ====== API 调用 ======
        function getToken() {
            return sessionStorage.getItem('lhc_token') || '';
        }
        async function api(path, options = {}) {
            const token = getToken();
            const headers = options.headers || {};
            if (token) headers['Authorization'] = 'Bearer ' + token;
            try {
                const res = await fetch(path, { ...options, headers });
                if (res.status === 401) { sessionStorage.removeItem('lhc_token'); location.reload(); return null; }
                if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
                return await res.json();
            } catch (e) {
                showToast('请求失败: ' + e.message, 'error');
                return null;
            }
        }
        async function postApi(path, body) {
            const token = getToken();
            const headers = {'Content-Type': 'application/json'};
            if (token) headers['Authorization'] = 'Bearer ' + token;
            try {
                const res = await fetch(path, {method: 'POST', headers, body: JSON.stringify(body)});
                if (res.status === 401) { sessionStorage.removeItem('lhc_token'); location.reload(); return null; }
                const data = await res.json();
                return {ok: res.ok, ...data};
            } catch (e) {
                showToast('❌ 请求失败: ' + e.message, 'error');
                return null;
            }
        }

        // ====== 仪表盘 ======
        let _aichatAvailable = false;  // 全局标志，由 refreshAll 设置

        async function refreshAll() {
            const data = await api('/api/status');
            if (!data) return;
            renderStats(data);
            renderSysInfo(data);
            loadCmdStats();
            loadAdmins();

            // 检测 AI 对话插件是否可用
            _aichatAvailable = data.aichat_available === true;
            document.getElementById('nav-persona').style.display = _aichatAvailable ? '' : 'none';
            document.getElementById('token-card').style.display = _aichatAvailable ? '' : 'none';
            if (_aichatAvailable) {
                loadTokenStats();
            } else {
                document.getElementById('token-summary-cards').innerHTML =
                    '<div class="stat-card" style="grid-column:1/-1;"><div class="stat-card-title" style="color:var(--text-muted);">📦 未检测到 AI 对话插件 (nonebot_plugin_aichat_baize)，Token 统计不可用</div></div>';
                document.getElementById('token-chart').innerHTML = '';
            }
        }

        function renderStats(data) {
            const grid = document.getElementById('stat-grid');
            const cpuPct = data.cpu_percent || 0;
            const cpuColor = cpuPct > 80 ? 'red' : cpuPct > 50 ? 'yellow' : 'green';
            const memPct = data.memory_percent || 0;
            const memColor = memPct > 80 ? 'red' : memPct > 50 ? 'yellow' : 'green';
            const uptime = formatUptime(data.uptime_seconds || 0);

            grid.innerHTML = `
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">CPU 使用率</span>
                        <span class="stat-card-icon" style="background:rgba(59,130,246,0.15)">💻</span>
                    </div>
                    <div class="stat-card-value">${cpuPct.toFixed(1)}<span style="font-size:16px;color:var(--text-secondary)">%</span></div>
                    <div class="progress-bar"><div class="progress-fill ${cpuColor}" style="width:${cpuPct}%"></div></div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">内存使用率</span>
                        <span class="stat-card-icon" style="background:rgba(168,85,247,0.15)">🧠</span>
                    </div>
                    <div class="stat-card-value">${memPct.toFixed(1)}<span style="font-size:16px;color:var(--text-secondary)">%</span></div>
                    <div class="progress-bar"><div class="progress-fill ${memColor}" style="width:${memPct}%"></div></div>
                    <div class="stat-card-sub">已用 ${formatBytes(data.memory_used || 0)} / 总计 ${formatBytes(data.memory_total || 0)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">运行时间</span>
                        <span class="stat-card-icon" style="background:rgba(34,197,94,0.15)">⏱</span>
                    </div>
                    <div class="stat-card-value" style="font-size:22px;">${uptime}</div>
                    <div class="stat-card-sub">自 ${data.start_time || '--'} 起</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">消息统计</span>
                        <span class="stat-card-icon" style="background:rgba(6,182,212,0.15)">💬</span>
                    </div>
                    <div style="display:flex;gap:24px;margin-top:4px;">
                        <div><div style="font-size:22px;font-weight:700;">${(data.recv_msg_count || 0).toLocaleString()}</div><div style="font-size:11px;color:var(--text-muted);">接收</div></div>
                        <div><div style="font-size:22px;font-weight:700;">${(data.send_msg_count || 0).toLocaleString()}</div><div style="font-size:11px;color:var(--text-muted);">发送</div></div>
                    </div>
                </div>
            `;
        }

        function renderSysInfo(data) {
            document.getElementById('sysinfo-table').innerHTML = `
                <table>
                    <tbody>
                        <tr><td style="width:160px;font-weight:600;color:var(--text-secondary)">操作系统</td><td>${esc(data.os || '--')}</td></tr>
                        <tr><td style="font-weight:600;color:var(--text-secondary)">Python 版本</td><td>${esc(data.python_version || '--')}</td></tr>
                        <tr><td style="font-weight:600;color:var(--text-secondary)">NoneBot 版本</td><td>${esc(data.nonebot_version || '--')}</td></tr>
                        <tr><td style="font-weight:600;color:var(--text-secondary)">CPU 核心数</td><td>${data.cpu_count || '--'}</td></tr>
                        <tr><td style="font-weight:600;color:var(--text-secondary)">磁盘使用</td><td>${formatBytes(data.disk_used || 0)} / ${formatBytes(data.disk_total || 0)} (${(data.disk_percent || 0).toFixed(1)}%)</td></tr>
                        <tr><td style="font-weight:600;color:var(--text-secondary)">启动时间</td><td>${data.start_time || '--'}</td></tr>
                        <tr><td style="font-weight:600;color:var(--text-secondary)">Bot 数量</td><td><span class="badge badge-success">${data.bot_count || 0} 个在线</span></td></tr>
                        <tr><td style="font-weight:600;color:var(--text-secondary)">已加载插件</td><td><span class="badge badge-info">${data.plugin_count || 0} 个</span></td></tr>
                    </tbody>
                </table>`;
        }

        // ====== 管理员管理 ======
        async function loadAdmins() {
            const data = await api('/api/admins');
            if (!data) return;
            const admins = data.admins || [];
            const container = document.getElementById('admin-list');
            if (!admins.length) {
                container.innerHTML = '<span style="color:var(--text-muted);font-size:12px;">暂无额外管理员（使用 config.yml 的 superusers）</span>';
                return;
            }
            container.innerHTML = admins.map(qq => `
                <span style="background:var(--accent);color:#fff;padding:3px 10px;border-radius:100px;font-size:12px;display:inline-flex;align-items:center;gap:4px;">
                    👑 ${esc(qq)}
                    <span style="cursor:pointer;opacity:0.7;" onclick="removeAdmin('${esc(qq)}')" title="移除">✕</span>
                </span>`).join('');
        }

        async function addAdmin() {
            const inp = document.getElementById('admin-qq-input');
            const qq = inp.value.trim();
            if (!qq) { showToast('请输入 QQ 号', 'error'); return; }
            const data = await postApi('/api/admins/add', {qq: qq});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                inp.value = '';
                loadAdmins();
            } else {
                showToast('❌ ' + ((data && data.error) || '添加失败'), 'error');
            }
        }

        async function removeAdmin(qq) {
            if (!confirm('确定移除管理员 ' + qq + ' 吗？')) return;
            const data = await postApi('/api/admins/remove', {qq: qq});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                loadAdmins();
            } else {
                showToast('❌ ' + ((data && data.error) || '移除失败'), 'error');
            }
        }

        // ====== 指令统计 ======
        async function loadCmdStats() {
            const data = await api('/api/cmd-stats');
            if (!data) return;

            document.getElementById('cmd-stats-total').textContent =
                '📅 今日 ' + (data.today || 0) + ' 次 · 📊 累计 ' + (data.total || 0) + ' 次';

            const typeLabels = {on_command: '指令', on_fullmatch: '全匹配', on_message: '消息'};
            const typeBadges = {on_command: 'badge-info', on_fullmatch: 'badge-purple', on_message: 'badge-success'};

            // 今日排行
            const todayDetails = data.today_details || [];
            const todayRows = todayDetails.length ? todayDetails.map((d, i) => `
                <tr>
                    <td>${i + 1}</td>
                    <td><strong>${esc(d.trigger)}</strong></td>
                    <td><span class="badge ${typeBadges[d.type] || 'badge-info'}">${typeLabels[d.type] || d.type}</span></td>
                    <td>${esc(d.plugin)}</td>
                    <td><span style="font-weight:700;color:var(--success);">${d.count}</span> 次</td>
                </tr>`).join('') : '<tr><td colspan="5" style="text-align:center;color:var(--text-muted);">暂无今日记录</td></tr>';

            // 历史排行
            const allDetails = data.details || [];
            const allRows = allDetails.length ? allDetails.map((d, i) => `
                <tr>
                    <td>${i + 1}</td>
                    <td><strong>${esc(d.trigger)}</strong></td>
                    <td><span class="badge ${typeBadges[d.type] || 'badge-info'}">${typeLabels[d.type] || d.type}</span></td>
                    <td>${esc(d.plugin)}</td>
                    <td><span style="font-weight:700;color:var(--accent);">${d.count}</span> 次</td>
                </tr>`).join('') : '<tr><td colspan="5" style="text-align:center;color:var(--text-muted);">暂无使用记录</td></tr>';

            const tblStyle = 'style="table-layout:fixed;width:100%;"';
            const tblHead = '<thead><tr><th style="width:6%;">#</th><th style="width:28%;">触发词</th><th style="width:16%;">类型</th><th style="width:28%;">所属插件</th><th style="width:22%;">次数</th></tr></thead>';

            document.getElementById('cmd-stats-table').innerHTML =
                '<div style="font-size:12px;font-weight:600;color:var(--text-secondary);margin-bottom:4px;">🕐 今日排行</div>' +
                '<table ' + tblStyle + ' style="margin-bottom:12px;">' + tblHead + '<tbody>' + todayRows + '</tbody></table>' +
                '<div style="font-size:12px;font-weight:600;color:var(--text-secondary);margin-bottom:4px;">📚 历史排行</div>' +
                '<table ' + tblStyle + '>' + tblHead + '<tbody>' + allRows + '</tbody></table>';
        }

        // ====== Token 用量图表 ======
        async function loadTokenStats() {
            const data = await api('/api/token-stats');
            if (!data) return;

            // 更新统计卡片
            const summary = data.summary;
            const cards = document.querySelectorAll('#token-summary-cards .stat-card-value');
            cards[0].textContent = formatNumber(summary.total_tokens);
            cards[1].textContent = formatNumber(summary.today_tokens);
            cards[2].textContent = formatNumber(summary.total_calls);
            cards[3].textContent = formatNumber(summary.today_calls);
            cards[4].textContent = '¥' + summary.total_cost.toFixed(2);
            cards[5].textContent = '¥' + summary.today_cost.toFixed(4);

            // 渲染柱状图
            const chart = document.getElementById('token-chart');
            const daily = data.daily || [];
            if (daily.length === 0) {
                chart.innerHTML = '<span style="color:var(--text-muted);font-size:12px;">暂无数据</span>';
                return;
            }

            const maxVal = Math.max(1, ...daily.map(d => d.input + d.output));
            chart.innerHTML = daily.map(d => {
                const inputH = Math.max(2, (d.input / maxVal) * 120);
                const outputH = Math.max(2, (d.output / maxVal) * 120);
                const total = d.input + d.output;
                const calls = d.calls || 0;
                return `<div style="flex:1;display:flex;flex-direction:column;align-items:center;min-width:30px;">
                    <span style="font-size:10px;color:var(--text-muted);margin-bottom:2px;" title="Token: ${formatNumber(total)} | 调用: ${calls}次">${formatNumber(total)}</span>
                    <span style="font-size:9px;color:var(--success);margin-bottom:1px;" title="调用次数">${calls > 0 ? '×'+calls : ''}</span>
                    <div style="display:flex;flex-direction:column;align-items:center;width:100%;max-width:36px;">
                        <div style="width:50%;background:var(--accent);border-radius:3px 3px 0 0;height:${outputH}px;min-height:${d.output > 0 ? 2 : 0}px;" title="输出: ${formatNumber(d.output)}"></div>
                        <div style="width:50%;background:rgba(59,130,246,0.4);border-radius:0 0 3px 3px;height:${inputH}px;min-height:${d.input > 0 ? 2 : 0}px;" title="输入: ${formatNumber(d.input)}"></div>
                    </div>
                    <span style="font-size:9px;color:var(--text-muted);margin-top:3px;white-space:nowrap;">${d.date}</span>
                </div>`;
            }).join('');
        }

        function formatNumber(n) {
            if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
            if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
            return String(n);
        }

        // ====== 指令列表 ======
        async function loadCommands() {
            const data = await api('/api/commands');
            if (!data) return;

            const sections = [
                {key: 'on_command', title: '⌨️ on_command', prefix: '/'},
                {key: 'on_fullmatch', title: '🎯 on_fullmatch', prefix: ''},
                {key: 'on_alconna', title: '✨ on_alconna', prefix: ''},
                {key: 'on_startswith', title: '🔤 on_startswith', prefix: ''},
                {key: 'on_regex', title: '🔍 on_regex', prefix: ''},
                {key: 'on_endswith', title: '🔤 on_endswith', prefix: ''},
                {key: 'on_message', title: '💬 on_message', prefix: ''},
            ];

            sections.forEach(sec => {
                const items = data[sec.key] || [];
                document.getElementById('cmd-count-' + sec.key).textContent = items.length + ' 个';

                if (!items.length) {
                    document.getElementById('cmd-table-' + sec.key).innerHTML =
                        '<div style="padding:16px;text-align:center;color:var(--text-muted);">暂无</div>';
                    return;
                }

                // 按插件分组
                const grouped = {};
                items.forEach(item => {
                    const mod = item.module;
                    if (!grouped[mod]) grouped[mod] = [];
                    grouped[mod].push(sec.prefix + item.trigger);
                });

                const rows = Object.entries(grouped).map(([mod, triggers]) => `
                    <tr>
                        <td style="font-weight:600;color:var(--accent);white-space:nowrap;">${esc(mod)}</td>
                        <td style="color:var(--text-secondary);">${triggers.map(t => '<code style="background:var(--bg-primary);padding:2px 6px;border-radius:4px;margin:2px;display:inline-block;font-size:12px;">' + esc(t) + '</code>').join(' ')}</td>
                    </tr>`).join('');

                document.getElementById('cmd-table-' + sec.key).innerHTML =
                    '<table><thead><tr><th style="width:140px;">插件</th><th>触发词</th></tr></thead><tbody>' + rows + '</tbody></table>';
            });
        }

        // ====== Bot 用户信息 ======
        async function loadBotInfo() {
            const data = await api('/api/bot-info');
            if (!data) return;
            document.getElementById('bot-nickname').textContent = data.nickname || '--';
            document.getElementById('bot-qq').textContent = 'QQ: ' + (data.qq || '--');
            if (data.avatar) {
                const av = document.getElementById('bot-avatar');
                av.src = data.avatar;
                av.style.display = '';
            }
            document.getElementById('bot-friends').textContent = (data.friends || 0).toLocaleString();
            document.getElementById('bot-groups').textContent = (data.groups || 0).toLocaleString();
            document.getElementById('bot-msg-recv').textContent = (data.msg_recv || 0).toLocaleString();
            document.getElementById('bot-msg-sent').textContent = (data.msg_sent || 0).toLocaleString();
            // 私聊排行
            const topData = await api('/api/bot-info/top-users');
            const users = (topData && topData.users) ? topData.users : [];
            const listEl = document.getElementById('top-users-list');
            if (!users.length) {
                listEl.innerHTML = '<div style="padding:16px;text-align:center;color:var(--text-muted);">暂无数据</div>';
            } else {
                const max = users[0].count;
                listEl.innerHTML = users.map((u, i) => {
                    const av = 'https://q1.qlogo.cn/g?b=qq&nk=' + u.qq + '&s=100';
                    return `<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);">
                        <span style="font-weight:700;color:var(--accent);width:24px;text-align:center;">#${i + 1}</span>
                        <img src="${av}" style="width:32px;height:32px;border-radius:50%;background:var(--bg-primary);" onerror="this.style.display='none'">
                        <span style="flex:1;min-width:0;">${esc(u.qq)}</span>
                        <span style="font-weight:600;white-space:nowrap;">${u.count} 条</span>
                        <div style="width:80px;height:4px;background:var(--bg-primary);border-radius:2px;flex-shrink:0;">
                            <div style="height:100%;width:${Math.min(100, u.count / max * 100)}%;background:var(--accent);border-radius:2px;"></div>
                        </div>
                    </div>`;
                }).join('');
            }
        }

        async function showDetailModal(type) {
            const titles = {friends: '👥 好友列表', groups: '💬 群聊列表'};
            document.getElementById('detail-modal-title').textContent = titles[type] || '详情';
            document.getElementById('detail-modal-body').innerHTML = '<div style="text-align:center;padding:30px;color:var(--text-muted);">加载中...</div>';
            document.getElementById('detail-overlay').style.display = 'flex';

            const data = await api('/api/bot-info/' + type);
            if (!data) return;

            if (type === 'friends') {
                const friends = data.friends || [];
                if (!friends.length) {
                    document.getElementById('detail-modal-body').innerHTML = '<div style="text-align:center;padding:30px;color:var(--text-muted);">暂无好友</div>';
                    return;
                }
                document.getElementById('detail-modal-body').innerHTML = friends.map(f => `
                    <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);">
                        <img src="${esc(f.avatar)}" style="width:40px;height:40px;border-radius:50%;background:var(--bg-primary);" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 40 40%22><rect fill=%22%23334155%22 width=%2240%22 height=%2240%22/><text x=%2220%22 y=%2226%22 text-anchor=%22middle%22 fill=%22%2394a3b8%22 font-size=%2216%22>?</text></svg>'">
                        <div style="flex:1;">
                            <div style="font-size:13px;font-weight:600;">${esc(f.nickname || f.qq)}</div>
                            <div style="font-size:11px;color:var(--text-muted);">${esc(f.qq)}${f.remark ? ' · ' + esc(f.remark) : ''}</div>
                        </div>
                        <button class="btn btn-sm" style="color:var(--danger);" onclick="deleteFriend('${esc(f.qq)}', this)" title="删除好友">🗑</button>
                    </div>`).join('');
            } else if (type === 'groups') {
                const groups = data.groups || [];
                if (!groups.length) {
                    document.getElementById('detail-modal-body').innerHTML = '<div style="text-align:center;padding:30px;color:var(--text-muted);">暂无群聊</div>';
                    return;
                }
                document.getElementById('detail-modal-body').innerHTML = groups.map(g => `
                    <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);">
                        <img src="${esc(g.avatar || '')}" style="width:40px;height:40px;border-radius:50%;background:var(--bg-primary);" onerror="this.style.display='none'">
                        <div style="flex:1;">
                            <div style="font-size:13px;font-weight:600;">${esc(g.name || g.id)}</div>
                            <div style="font-size:11px;color:var(--text-muted);">${esc(g.id)} · ${g.member_count || 0}/${g.max_member_count || 0} 人</div>
                        </div>
                        <button class="btn btn-sm" style="color:var(--danger);" onclick="leaveGroup('${esc(g.id)}', this)" title="退出群聊">🚪</button>
                    </div>`).join('');
            }
        }

        async function deleteFriend(qq, btn) {
            if (!confirm('确定要删除好友 ' + qq + ' 吗？')) return;
            btn.textContent = '⏳'; btn.disabled = true;
            const data = await postApi('/api/bot-info/friends/delete', {qq: qq});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                showDetailModal('friends');
            } else {
                showToast('❌ ' + ((data && data.error) || '删除失败'), 'error');
                btn.textContent = '🗑'; btn.disabled = false;
            }
        }

        async function leaveGroup(gid, btn) {
            if (!confirm('确定要退出群聊 ' + gid + ' 吗？')) return;
            btn.textContent = '⏳'; btn.disabled = true;
            const data = await postApi('/api/bot-info/groups/leave', {group_id: gid});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                showDetailModal('groups');
            } else {
                showToast('❌ ' + ((data && data.error) || '退群失败'), 'error');
                btn.textContent = '🚪'; btn.disabled = false;
            }
        }

        function hideDetailModal() {
            document.getElementById('detail-overlay').style.display = 'none';
        }

        // ====== 插件商店 ======
        let storeData = [];

        async function loadStore() {
            document.getElementById('store-status').textContent = '加载中...';
            document.getElementById('store-list').innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted);">加载中...</div>';

            const search = document.getElementById('store-search').value;
            const url = '/api/store' + (search ? '?search=' + encodeURIComponent(search) : '');
            const data = await api(url);
            if (!data) return;

            storeData = data.plugins || [];
            document.getElementById('store-status').textContent = '共 ' + data.total + ' 个插件' + (search ? '（搜索: ' + esc(search) + '）' : '');

            if (!storeData.length) {
                document.getElementById('store-list').innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted);">没有找到匹配的插件</div>';
                return;
            }

            document.getElementById('store-list').innerHTML = storeData.map(p => {
                const tags = (p.tags || []).map(t => '<span style="background:' + (t.color || '#64748b') + '22;color:' + (t.color || '#94a3b8') + ';padding:1px 6px;border-radius:4px;font-size:10px;margin:2px;">' + esc(t.label) + '</span>').join('');
                const badge = p.is_official ? '<span class="badge badge-success" style="font-size:10px;">官方</span> ' : '';
                const installed = p.installed ? '<span class="badge badge-info" style="font-size:10px;">✓ 已安装</span> ' : '';
                const actionBtn = p.installed
                    ? '<button class="btn btn-sm" style="color:var(--danger);" onclick="uninstallStorePlugin(\'' + esc(p.module_name) + '\', this)">🗑 卸载</button>'
                    : '<button class="btn btn-sm btn-primary" onclick="installStorePlugin(\'' + esc(p.project_link || p.module_name) + '\', this)">📥 安装</button>';
                return '<div class="stat-card" style="padding:14px 18px;">' +
                    '<div style="display:flex;justify-content:space-between;align-items:flex-start;">' +
                    '<div style="flex:1;">' +
                    '<div style="font-size:14px;font-weight:600;">' + badge + installed + esc(p.name || p.module_name) + '</div>' +
                    '<div style="font-size:11px;color:var(--text-muted);margin:2px 0;">' + esc(p.module_name) + ' · v' + esc(p.version || '?') + ' · ' + esc(p.author || '未知') + '</div>' +
                    '<div style="font-size:12px;color:var(--text-secondary);margin:4px 0;">' + esc(p.desc || '') + '</div>' +
                    '<div style="margin-top:4px;">' + tags + '</div>' +
                    '</div>' +
                    '<div style="margin-left:12px;">' + actionBtn + '</div>' +
                    '</div></div>';
            }).join('');
        }

        function searchStore() {
            clearTimeout(window._storeTimer);
            window._storeTimer = setTimeout(() => loadStore(), 400);
        }

        async function installStorePlugin(project, btn) {
            if (!confirm('确定要安装插件「' + project + '」吗？\n\n安装后需在 pyproject.toml 中添加并重启 Bot。')) return;
            btn.textContent = '⏳ 安装中...';
            btn.disabled = true;
            const data = await postApi('/api/store/install', {project: project});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                loadStore();
            } else {
                showToast('❌ ' + ((data && data.error) || '安装失败'), 'error');
                btn.textContent = '📥 安装';
                btn.disabled = false;
            }
        }

        async function uninstallStorePlugin(module, btn) {
            if (!confirm('确定要卸载插件「' + module + '」吗？\n\n将执行 pip uninstall 并从 pyproject.toml 移除。')) return;
            btn.textContent = '⏳ 卸载中...';
            btn.disabled = true;
            const data = await postApi('/api/plugins/uninstall', {module: module});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                loadStore();
            } else {
                showToast('❌ ' + ((data && data.error) || '卸载失败'), 'error');
                btn.textContent = '🗑 卸载';
                btn.disabled = false;
            }
        }

        // ====== 插件 ======
        async function loadPlugins() {
            const data = await api('/api/plugins');
            if (!data) return;
            document.getElementById('plugin-count').textContent = '共 ' + data.length + ' 个插件';
            const rows = data.map((p, i) => {
                const isDisabled = p.disabled === true;
                const isExternal = p.external === true;
                const statusBadge = isExternal ? '<span class="badge badge-info">📦 外部</span>'
                    : isDisabled ? '<span class="badge badge-warning">⏸ 已禁用</span>'
                    : p.loaded ? '<span class="badge badge-success">✓ 已加载</span>'
                    : '<span class="badge badge-danger">✗ 加载失败</span>';
                const toggleLabel = isDisabled ? '▶ 启用' : '⏸ 禁用';
                const toggleTitle = isExternal
                    ? (isDisabled ? '启用（添加回 pyproject.toml）' : '禁用（从 pyproject.toml 移除）')
                    : (isDisabled ? '启用此插件（重启后生效）' : '禁用此插件（重启后生效）');
                const toggleBtn = `<button class="btn btn-sm" onclick="togglePlugin('${esc(p.module)}', ${isDisabled})" title="${toggleTitle}">${toggleLabel}</button>`;
                const rowClass = isDisabled ? ' class="disabled-row"' : '';
                return `<tr${rowClass}>
                    <td>${i + 1}</td>
                    <td><strong>${esc(p.name)}</strong></td>
                    <td style="color:var(--text-secondary);max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${esc(p.description || '')}">${esc(p.description || '无描述')}</td>
                    <td><span class="badge badge-purple">${esc(p.module || '--')}</span></td>
                    <td>${statusBadge}</td>
                    <td style="white-space:nowrap;">
                        ${toggleBtn}
                        <button class="btn btn-sm" onclick="showConfigEditor('${esc(p.module)}')" title="编辑配置">⚙</button>
                        <button class="btn btn-sm" style="color:var(--danger);" onclick="uninstallPlugin('${esc(p.module)}', ${isExternal})" title="卸载插件">🗑</button>
                    </td>
                </tr>`;
            }).join('');
            document.getElementById('plugin-table').innerHTML = `<table><thead><tr><th>#</th><th>名称</th><th>描述</th><th>模块</th><th>状态</th><th>操作</th></tr></thead><tbody>${rows}</tbody></table>`;
        }

        async function uninstallPlugin(module, isExternal) {
            const warn = isExternal
                ? '确定要卸载 pip 插件「' + module + '」吗？\n\n这将执行 pip uninstall 并从 pyproject.toml 移除。'
                : '确定要删除插件「' + module + '」吗？\n\n这将永久删除插件文件，不可恢复！';
            if (!confirm(warn)) return;
            const data = await postApi('/api/plugins/uninstall', {module: module});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                setTimeout(() => loadPlugins(), 300);
            } else {
                showToast('❌ ' + ((data && data.error) || '卸载失败'), 'error');
            }
        }

        async function toggleAllPlugins(enable) {
            const action = enable ? '启用' : '禁用';
            if (!confirm('确定要一键' + action + '所有本地插件吗？\n\n这将' + action + ' src/plugins/ 下的所有插件并触发热重载。')) return;
            const data = await postApi('/api/plugins/toggle-all', {enabled: enable});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                setTimeout(() => loadPlugins(), 500);
            } else {
                showToast('❌ ' + ((data && data.error) || '操作失败'), 'error');
            }
        }

        async function togglePlugin(module, enable) {
            const action = enable ? '启用' : '禁用';
            if (!confirm('确定要' + action + '插件「' + module + '」吗？\n\n重启 Bot 后生效。')) return;
            const data = await postApi('/api/plugins/toggle', {module: module, enabled: enable});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                setTimeout(() => loadPlugins(), 300);
            } else {
                showToast('❌ ' + ((data && data.error) || '操作失败'), 'error');
            }
        }

        // ====== Bot 列表 ======
        async function loadBots() {
            const data = await api('/api/bots');
            if (!data) return;
            if (!data.length) {
                document.getElementById('bot-table').innerHTML = '<div style="padding:40px;text-align:center;color:var(--text-muted);">暂无在线 Bot</div>';
                return;
            }
            const rows = data.map(b => `
                <tr>
                    <td><span class="status-dot"><span class="pulse"></span> 在线</span></td>
                    <td><strong>${esc(b.self_id)}</strong></td>
                    <td>${esc(b.nickname || '--')}</td>
                    <td><span class="badge badge-info">${esc(b.adapter || '--')}</span></td>
                </tr>`).join('');
            document.getElementById('bot-table').innerHTML = `<table><thead><tr><th>状态</th><th>Bot ID</th><th>昵称</th><th>适配器</th></tr></thead><tbody>${rows}</tbody></table>`;
        }

        // ====== 日志 ======
        async function loadLogs() {
            const data = await api('/api/logs?limit=200');
            if (!data) return;
            const container = document.getElementById('log-container');
            if (!data.length) {
                container.innerHTML = '<div class="log-line info">暂无日志记录</div>';
                return;
            }
            container.innerHTML = data.map(l => {
                let cls = 'info';
                if (l.level === 'WARNING') cls = 'warning';
                else if (l.level === 'ERROR' || l.level === 'CRITICAL') cls = 'error';
                else if (l.level === 'DEBUG' || l.level === 'TRACE') cls = 'debug';
                else if (l.level === 'SUCCESS') cls = 'success';
                return `<div class="log-line ${cls}">[${esc(l.time)}] [${esc(l.level)}] ${esc(l.message)}</div>`;
            }).join('');
            container.scrollTop = container.scrollHeight;
        }

        function clearLogs() {
            document.getElementById('log-container').innerHTML = '<div class="log-line info">日志已清屏（不影响实际日志文件）</div>';
        }

        function toggleAutoRefresh() {
            autoRefresh = !autoRefresh;
            const btn = document.getElementById('btn-auto-refresh');
            btn.textContent = autoRefresh ? '⏸ 暂停' : '▶ 继续';
            if (autoRefresh) startAutoRefresh(); else stopAutoRefresh();
        }

        function startAutoRefresh() {
            stopAutoRefresh();
            autoRefreshTimer = setInterval(loadLogs, 3000);
        }

        function stopAutoRefresh() {
            if (autoRefreshTimer) { clearInterval(autoRefreshTimer); autoRefreshTimer = null; }
        }

        function startTokenRefresh() {
            stopTokenRefresh();
            tokenRefreshTimer = setInterval(loadTokenStats, 15000);  // 每15秒刷新Token统计
        }

        function stopTokenRefresh() {
            if (tokenRefreshTimer) { clearInterval(tokenRefreshTimer); tokenRefreshTimer = null; }
        }

        // ====== 插件配置编辑器 ======
        let currentConfigModule = null;

        async function showConfigEditor(module) {
            currentConfigModule = module;
            document.getElementById('config-modal-title').textContent = '⚙ ' + esc(module) + ' — 配置';
            document.getElementById('config-modal-body').innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted);">加载中...</div>';
            document.getElementById('config-overlay').style.display = 'flex';

            const data = await api('/api/plugins/config?module=' + encodeURIComponent(module));
            if (!data) {
                document.getElementById('config-modal-body').innerHTML = '<div style="text-align:center;padding:40px;color:var(--danger);">加载配置失败</div>';
                return;
            }
            const hasConfigs = data.configs && data.configs.length > 0;
            const hasJsonFiles = data.json_files && data.json_files.length > 0;
            const hasMatchers = data.matchers && data.matchers.length > 0;
            const hasConfigPy = data.config_py && data.config_py.items && data.config_py.items.length > 0;
            if (!hasConfigs && !hasJsonFiles && !hasMatchers && !hasConfigPy) {
                document.getElementById('config-modal-body').innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted);">此插件无可编辑的配置</div>';
                return;
            }
            document.getElementById('config-modal-body').innerHTML =
                renderConfigPy(data.config_py) +
                renderConfigForm(data.configs || []) +
                renderJsonEditors(data.json_files || []) +
                renderMatchers(data.matchers || []) +
                renderFormatHelp();
        }

        function renderFormatHelp() {
            return `<details style="margin-top:20px;font-size:12px;color:var(--text-muted);border-top:1px solid var(--border);padding-top:12px;">
                <summary style="cursor:pointer;font-weight:600;color:var(--text-secondary);user-select:none;">📖 支持识别的配置项与指令格式</summary>
                <div style="margin-top:10px;line-height:1.8;">
                    <div style="font-weight:600;color:var(--accent);margin-bottom:4px;">📝 配置常量</div>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">API_KEY = "sk-xxx"</code> &nbsp;模块级大写常量<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">CONFIG = {"KEY": value}</code> &nbsp;字典式配置（支持 _env 包装）<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">config.py</code> &nbsp;dataclass / 构造函数参数<br>

                    <div style="font-weight:600;color:var(--accent);margin-top:10px;margin-bottom:4px;">📋 指令触发词</div>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">cmd = on_command("触发词")</code> &nbsp;标准指令<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">matcher = on_fullmatch("完全匹配")</code> &nbsp;全匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">rule = on_startswith("前缀")</code> &nbsp;前缀匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">rule = on_regex(r"正则")</code> &nbsp;正则匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">rule = on_endswith("后缀")</code> &nbsp;后缀匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">cmd = on_alconna(Alconna("..."))</code> &nbsp;Alconna 匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">("/gif倒放", "action")</code> &nbsp;函数体内嵌命令元组（on_message 手动解析模式）<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">on_command(("词1", "词2"))</code> &nbsp;元组触发词<br>

                    <div style="font-weight:600;color:var(--accent);margin-top:10px;margin-bottom:4px;">📁 JSON 配置文件</div>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">XXX_FILE = "data/xxx.json"</code> &nbsp;插件源码中引用的 JSON 文件（自动检测）<br>

                    <div style="margin-top:10px;color:var(--warning);">⚠ 注意：内嵌命令元组编辑后需保留缩进，Python 常量修改后需重启 Bot</div>
                </div>
            </details>`;
        }

        function hideConfigEditor() {
            document.getElementById('config-overlay').style.display = 'none';
            currentConfigModule = null;
        }

        function renderConfigPy(configPy) {
            if (!configPy || !configPy.items || !configPy.items.length) return '';
            return '<div style="font-size:12px;color:var(--text-muted);margin-bottom:8px;font-weight:600;">📝 config.py 配置 (' + esc(configPy.path || '') + ')</div>' +
                configPy.items.map(c => {
                let input;
                if (c.type === 'bool') {
                    input = `<select data-configpy-key="${esc(c.name)}" data-configpy-type="bool">
                        <option value="True" ${c.value ? 'selected' : ''}>True（开启）</option>
                        <option value="False" ${!c.value ? 'selected' : ''}>False（关闭）</option>
                    </select>`;
                } else if (c.type === 'int') {
                    input = `<input type="number" data-configpy-key="${esc(c.name)}" data-configpy-type="int" value="${c.value}" step="1">`;
                } else if (c.type === 'float') {
                    input = `<input type="number" data-configpy-key="${esc(c.name)}" data-configpy-type="float" value="${c.value}" step="any">`;
                } else {
                    input = `<input type="text" data-configpy-key="${esc(c.name)}" data-configpy-type="str" value="${esc(String(c.value))}">`;
                }
                return `<div class="config-item">
                    <div class="config-item-label" title="${esc(c.name)}">${esc(c.name)}</div>
                    <div class="config-item-input">
                        ${input}
                        ${c.comment ? '<div class="config-item-comment">' + esc(c.comment) + '</div>' : ''}
                    </div>
                    <div class="config-item-type">${esc(c.type)}</div>
                </div>`;
            }).join('');
        }

        function renderConfigForm(configs) {
            if (!configs.length) return '';
            return '<div style="font-size:12px;color:var(--text-muted);margin-bottom:8px;font-weight:600;">📝 Python 常量</div>' +
                configs.map(c => {
                let input;
                if (c.type === 'bool') {
                    input = `<select data-key="${esc(c.name)}" data-type="bool">
                        <option value="True" ${c.value ? 'selected' : ''}>True（开启）</option>
                        <option value="False" ${!c.value ? 'selected' : ''}>False（关闭）</option>
                    </select>`;
                } else if (c.type === 'int') {
                    input = `<input type="number" data-key="${esc(c.name)}" data-type="int" value="${c.value}" step="1">`;
                } else if (c.type === 'float') {
                    input = `<input type="number" data-key="${esc(c.name)}" data-type="float" value="${c.value}" step="any">`;
                } else {
                    input = `<input type="text" data-key="${esc(c.name)}" data-type="str" value="${esc(String(c.value))}">`;
                }
                return `<div class="config-item">
                    <div class="config-item-label" title="${esc(c.name)}">${esc(c.name)}</div>
                    <div class="config-item-input">
                        ${input}
                        ${c.comment ? '<div class="config-item-comment">' + esc(c.comment) + '</div>' : ''}
                    </div>
                    <div class="config-item-type">${esc(c.type)}</div>
                </div>`;
            }).join('');
        }

        function renderJsonEditors(jsonFiles) {
            if (!jsonFiles.length) return '';
            return '<div style="font-size:12px;color:var(--text-muted);margin:16px 0 8px;font-weight:600;">📁 JSON 配置文件</div>' +
                jsonFiles.map(jf => {
                    const parsed = jf.parsed || {};
                    const hasError = !!parsed.error;
                    const statusIcon = hasError ? '⚠' : '✓';
                    const statusColor = hasError ? 'var(--warning)' : 'var(--success)';
                    const keyCount = parsed.data ? Object.keys(parsed.data).length : 0;
                    return `<div class="config-item" style="flex-direction:column;align-items:stretch;">
                        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                            <div>
                                <span style="font-weight:600;font-size:13px;">${esc(jf.name)}</span>
                                <span style="font-size:11px;color:var(--text-muted);margin-left:8px;">→ ${esc(jf.path)}</span>
                            </div>
                            <span style="font-size:11px;color:${statusColor};">
                                ${statusIcon} ${hasError ? esc(parsed.error) : '已解析 · ' + keyCount + ' 个顶级键'}
                            </span>
                        </div>
                        <textarea data-json-name="${esc(jf.name)}" data-json-path="${esc(jf.path)}"
                            style="width:100%;height:200px;background:var(--bg-primary);color:var(--text-primary);
                            border:1px solid var(--border);border-radius:6px;padding:10px;font-family:'JetBrains Mono','Consolas',monospace;
                            font-size:12px;line-height:1.5;resize:vertical;tab-size:2;"
                            spellcheck="false"
                        >${esc(jf.content || '')}</textarea>
                    </div>`;
                }).join('');
        }

        function renderMatchers(matchers) {
            if (!matchers.length) return '';
            const typeLabel = {on_command: '指令', on_fullmatch: '全匹配', on_message: '消息触发', on_regex: '正则', on_startswith: '前缀', on_endswith: '后缀', on_alconna: 'Alconna'};
            return '<div style="font-size:12px;color:var(--text-muted);margin:16px 0 8px;font-weight:600;">📋 指令触发词（修改后需重启）</div>' +
                matchers.map(m => {
                    const isInline = m.variable && m.variable.startsWith('_inline:');
                    const displayVar = isInline ? '📦 内嵌命令' : m.variable;
                    const displayTitle = isInline ? '函数体内嵌命令元组 (行 ' + m.line + ')' : m.variable;
                    return `<div class="config-item">
                        <div class="config-item-label" title="${esc(displayTitle)}">${esc(displayVar)}</div>
                        <div class="config-item-input">
                            <input type="text" data-matcher-var="${esc(m.variable)}" value="${esc(m.trigger)}">
                            <div class="config-item-comment">${typeLabel[m.type] || m.type} — 修改此触发词后重启生效</div>
                        </div>
                        <div class="config-item-type">${esc(m.type)}</div>
                    </div>`;
                }).join('');
        }

        async function saveConfig() {
            if (!currentConfigModule) return;
            const inputs = document.querySelectorAll('#config-modal-body [data-key]');
            const changes = {};
            inputs.forEach(el => {
                const key = el.dataset.key;
                const type = el.dataset.type;
                let val = el.value;
                if (type === 'bool') {
                    val = val === 'True';
                } else if (type === 'int') {
                    val = parseInt(val, 10);
                    if (isNaN(val)) { showToast(key + ' 需为整数', 'error'); return; }
                } else if (type === 'float') {
                    val = parseFloat(val);
                    if (isNaN(val)) { showToast(key + ' 需为数字', 'error'); return; }
                }
                changes[key] = val;
            });

            // 收集 JSON 文件变更
            const jsonAreas = document.querySelectorAll('#config-modal-body [data-json-name]');
            const jsonChanges = [];
            jsonAreas.forEach(el => {
                jsonChanges.push({
                    name: el.dataset.jsonName,
                    path: el.dataset.jsonPath,
                    content: el.value,
                });
            });

            // 收集指令触发词变更
            const matcherInputs = document.querySelectorAll('#config-modal-body [data-matcher-var]');
            const matcherChanges = [];
            matcherInputs.forEach(el => {
                matcherChanges.push({
                    variable: el.dataset.matcherVar,
                    trigger: el.value,
                });
            });

            // 收集 config.py 变更
            const configPyInputs = document.querySelectorAll('#config-modal-body [data-configpy-key]');
            const configPyChanges = {};
            configPyInputs.forEach(el => {
                const key = el.dataset.configpyKey;
                const type = el.dataset.configpyType;
                let val = el.value;
                if (type === 'bool') {
                    val = val === 'True';
                } else if (type === 'int') {
                    val = parseInt(val, 10);
                    if (isNaN(val)) { showToast(key + ' 需为整数', 'error'); return; }
                } else if (type === 'float') {
                    val = parseFloat(val);
                    if (isNaN(val)) { showToast(key + ' 需为数字', 'error'); return; }
                }
                configPyChanges[key] = val;
            });

            const btn = document.getElementById('btn-save-config');
            btn.textContent = '⏳ 保存中...';
            btn.disabled = true;

            const data = await postApi('/api/plugins/config', {module: currentConfigModule, changes, json_changes: jsonChanges, matcher_changes: matcherChanges, config_py_changes: configPyChanges});
            if (data && data.ok) {
                showToast('✅ ' + data.message, 'success');
                hideConfigEditor();
            } else {
                showToast('❌ ' + ((data && data.error) || '未知错误'), 'error');
            }
            btn.textContent = '💾 保存配置';
            btn.disabled = false;
        }

        // ====== 工具函数 ======
        function formatUptime(seconds) {
            const d = Math.floor(seconds / 86400);
            const h = Math.floor((seconds % 86400) / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            const s = Math.floor(seconds % 60);
            const parts = [];
            if (d > 0) parts.push(d + '天');
            if (h > 0) parts.push(h + '时');
            if (m > 0) parts.push(m + '分');
            parts.push(s + '秒');
            return parts.join(' ');
        }

        function formatBytes(bytes) {
            if (!bytes || bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        function esc(s) {
            if (!s) return '';
            return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        }

        // ====== AI人设管理 ======
        let _personaData = null;
        let _currentPersonaTab = 'public';

        function switchPersonaTab(tab) {
            _currentPersonaTab = tab;
            document.querySelectorAll('.persona-tab').forEach(t => t.classList.remove('active'));
            document.getElementById('tab-' + tab).classList.add('active');
            // 显示/隐藏白名单区域
            const whitelistSection = document.getElementById('persona-whitelist-section');
            whitelistSection.style.display = (tab === 'hidden') ? 'block' : 'none';
            // 切换新建按钮显示
            document.getElementById('btn-create-public').style.display = (tab === 'public') ? '' : 'none';
            document.getElementById('btn-create-hidden').style.display = (tab === 'hidden') ? '' : 'none';
            renderPersonaEditor();
        }

        async function loadPersona() {
            const data = await api('/api/persona');
            if (!data) {
                document.getElementById('persona-editor').innerHTML =
                    '<span style="color:var(--danger);">加载人设数据失败</span>';
                return;
            }
            _personaData = data;
            renderPersonaEditor();
        }

        function renderPersonaEditor() {
            if (!_personaData) { loadPersona(); return; }
            const catalogKey = _currentPersonaTab === 'public' ? 'persona_catalog' : 'hidden_persona_catalog';
            const catalog = _personaData[catalogKey] || {};
            const entries = Object.entries(catalog);
            const container = document.getElementById('persona-editor');

            if (entries.length === 0) {
                container.innerHTML = '<div class="stat-card" style="text-align:center;padding:40px;"><span style="color:var(--text-muted);">暂无' + (_currentPersonaTab === 'public' ? '公开' : '隐藏') + '人设</span></div>';
            } else {
                container.innerHTML = entries.map(([key, item]) => {
                    const name = esc(item.name || '');
                    const sp = esc(item.system_prompt || '');
                    const dm = esc(item.display_model || '');
                    const desc = esc(item.description || '');
                    const keyEsc = esc(key);
                    const spLines = (item.system_prompt || '').split('\n').length;
                    return `<div class="persona-card">
                        <div class="persona-card-header" onclick="togglePersonaCard(this)">
                            <div>
                                <strong>#${keyEsc} ${name}</strong>
                                <span style="color:var(--text-muted);font-size:12px;margin-left:8px;">${esc(item.display_model || '')}</span>
                            </div>
                            <div style="display:flex;align-items:center;gap:8px;">
                                <button class="btn btn-sm" style="color:var(--danger);border-color:var(--danger);padding:2px 8px;font-size:11px;"
                                    onclick="event.stopPropagation();deletePersona('${keyEsc}')" title="删除此人格">🗑 删除</button>
                                <span class="collapse-icon">▼</span>
                            </div>
                        </div>
                        <div class="persona-card-body">
                            <div class="persona-field">
                                <label>名称 (name)</label>
                                <input type="text" value="${name}" data-key="${keyEsc}" data-field="name" onchange="onFieldChange(this)" placeholder="人设名称">
                            </div>
                            <div class="persona-field">
                                <label>显示名称 (display_model)</label>
                                <input type="text" value="${dm}" data-key="${keyEsc}" data-field="display_model" onchange="onFieldChange(this)" placeholder="在前端显示的名称">
                            </div>
                            <div class="persona-field">
                                <label>描述 (description)</label>
                                <input type="text" value="${desc}" data-key="${keyEsc}" data-field="description" onchange="onFieldChange(this)" placeholder="人设的简短描述">
                            </div>
                            <div class="persona-field">
                                <label>系统提示词 (system_prompt) <span class="field-hint">— 共 ${(item.system_prompt||'').length} 字，约 ${spLines} 行</span></label>
                                <textarea data-key="${keyEsc}" data-field="system_prompt" onchange="onFieldChange(this)" placeholder="在此编辑系统提示词...&#10;每行一条角色设定，AI将严格按照此提示词扮演角色。">${sp}</textarea>
                            </div>
                        </div>
                    </div>`;
                }).join('');
            }

            // 渲染隐藏人设白名单
            if (_currentPersonaTab === 'hidden') {
                renderWhitelistEditor();
            }
        }

        function togglePersonaCard(header) {
            header.parentElement.classList.toggle('collapsed');
        }

        function onFieldChange(el) {
            // 将修改实时写入 _personaData
            const key = el.dataset.key;
            const field = el.dataset.field;
            const value = el.value;
            const catalogKey = _currentPersonaTab === 'public' ? 'persona_catalog' : 'hidden_persona_catalog';
            if (!_personaData[catalogKey]) _personaData[catalogKey] = {};
            if (!_personaData[catalogKey][key]) _personaData[catalogKey][key] = {};
            _personaData[catalogKey][key][field] = value;
        }

        function renderWhitelistEditor() {
            const container = document.getElementById('persona-whitelist-editor');
            const whitelists = _personaData.hidden_persona_whitelists || {};
            const catalog = _personaData.hidden_persona_catalog || {};
            const entries = Object.keys(catalog);

            if (entries.length === 0) {
                container.innerHTML = '<span style="color:var(--text-muted);font-size:12px;">无隐藏人设</span>';
                return;
            }

            // 存索引→key映射，避免中文key作为HTML ID的问题
            window._hiddenKeys = entries;

            container.innerHTML = entries.map((key, idx) => {
                const tags = (whitelists[key] || []).map(qq =>
                    `<span class="whitelist-tag">${esc(qq)}<span class="remove-tag" onclick="removeWhitelistQQ(${idx},'${esc(qq)}')">×</span></span>`
                ).join('');
                return `<div class="persona-field" style="margin-bottom:14px;">
                    <label>${esc(key)} — 专属白名单 QQ</label>
                    <div style="display:flex;gap:6px;align-items:center;">
                        <input type="text" id="wl-input-${idx}" placeholder="输入QQ号，回车添加" style="flex:1;"
                            onkeydown="if(event.key==='Enter'){addWhitelistQQ(${idx});event.preventDefault();}">
                        <button class="btn btn-sm btn-primary" onclick="addWhitelistQQ(${idx})">添加</button>
                    </div>
                    <div style="margin-top:6px;min-height:24px;">${tags || '<span style="color:var(--text-muted);font-size:11px;">暂无白名单成员</span>'}</div>
                </div>`;
            }).join('');
        }

        function addWhitelistQQ(idx) {
            const keys = window._hiddenKeys || [];
            const personaKey = keys[idx];
            if (!personaKey) return;
            const input = document.getElementById('wl-input-' + idx);
            if (!input) return;
            const qq = input.value.trim();
            if (!qq || !/^\d+$/.test(qq)) { showToast('QQ号需为纯数字', 'error'); return; }
            if (!_personaData.hidden_persona_whitelists) _personaData.hidden_persona_whitelists = {};
            if (!_personaData.hidden_persona_whitelists[personaKey]) _personaData.hidden_persona_whitelists[personaKey] = [];
            const list = _personaData.hidden_persona_whitelists[personaKey];
            if (list.includes(qq)) { showToast('该QQ已存在', 'info'); input.value = ''; return; }
            list.push(qq);
            input.value = '';
            renderWhitelistEditor();
        }

        function removeWhitelistQQ(idx, qq) {
            const keys = window._hiddenKeys || [];
            const personaKey = keys[idx];
            if (!personaKey) return;
            if (!_personaData.hidden_persona_whitelists || !_personaData.hidden_persona_whitelists[personaKey]) return;
            const list = _personaData.hidden_persona_whitelists[personaKey];
            const i = list.indexOf(qq);
            if (i > -1) list.splice(i, 1);
            renderWhitelistEditor();
        }

        let _createPersonaType = 'public';

        function showCreatePersonaModal(type) {
            _createPersonaType = type;
            const title = document.getElementById('create-persona-title');
            const keyHint = document.getElementById('create-key-hint');
            const keyInput = document.getElementById('create-persona-key');
            // 清空表单
            document.getElementById('create-persona-key').value = '';
            document.getElementById('create-persona-name').value = '';
            document.getElementById('create-persona-display').value = '';
            document.getElementById('create-persona-desc').value = '';
            document.getElementById('create-persona-prompt').value = '';

            if (type === 'public') {
                title.textContent = '➕ 新建公开人设';
                keyHint.textContent = '— 输入数字ID，如 6';
                keyInput.placeholder = '输入数字ID（如 6）';
            } else {
                title.textContent = '➕ 新建隐藏人设';
                keyHint.textContent = '— 输入唯一字符串ID，如 明月定制3';
                keyInput.placeholder = '输入唯一字符串ID（如 明月定制3）';
            }
            document.getElementById('create-persona-overlay').style.display = 'flex';
        }

        function closeCreatePersonaModal() {
            document.getElementById('create-persona-overlay').style.display = 'none';
        }

        async function confirmCreatePersona() {
            const key = document.getElementById('create-persona-key').value.trim();
            const name = document.getElementById('create-persona-name').value.trim();
            const display = document.getElementById('create-persona-display').value.trim();
            const desc = document.getElementById('create-persona-desc').value.trim();
            const prompt = document.getElementById('create-persona-prompt').value.trim();

            if (!key) { showToast('请输入人设 ID', 'error'); return; }
            if (_createPersonaType === 'public' && !/^\d+$/.test(key)) { showToast('公开人设 ID 需为纯数字', 'error'); return; }
            if (!name) { showToast('请输入名称', 'error'); return; }
            if (!prompt) { showToast('请输入系统提示词', 'error'); return; }

            // 检查是否已存在
            const catalogKey = _createPersonaType === 'public' ? 'persona_catalog' : 'hidden_persona_catalog';
            if (!_personaData) _personaData = { persona_catalog: {}, hidden_persona_catalog: {}, hidden_persona_whitelists: {} };
            if (!_personaData[catalogKey]) _personaData[catalogKey] = {};
            if (_personaData[catalogKey][key]) { showToast('该 ID 已存在，请更换', 'error'); return; }

            const newPersona = {
                name: name,
                system_prompt: prompt,
                display_model: display || name,
                description: desc || name
            };
            _personaData[catalogKey][key] = newPersona;

            // 如果是隐藏人设，自动初始化空白名单
            if (_createPersonaType === 'hidden') {
                if (!_personaData.hidden_persona_whitelists) _personaData.hidden_persona_whitelists = {};
                if (!_personaData.hidden_persona_whitelists[key]) _personaData.hidden_persona_whitelists[key] = [];
            }

            // 保存到 JSON 文件
            const result = await postApi('/api/persona/save', _personaData);
            if (result && result.ok) {
                closeCreatePersonaModal();
                showToast('✅ 人设已创建并保存', 'success');
                renderPersonaEditor();
                // 切换到对应 tab
                switchPersonaTab(_createPersonaType);
            } else {
                showToast('❌ 创建失败: ' + (result ? result.error : '网络错误'), 'error');
            }
        }

        async function deletePersona(key) {
            const catalogKey = _currentPersonaTab === 'public' ? 'persona_catalog' : 'hidden_persona_catalog';
            const persona = _personaData[catalogKey] && _personaData[catalogKey][key];
            const personaName = persona ? persona.name : key;
            if (!confirm('确定要删除人设 "#' + key + ' ' + personaName + '" 吗？\n\n此操作不可撤销，删除后需点击保存按钮生效。')) return;

            // 从内存数据中删除
            if (_personaData[catalogKey]) {
                delete _personaData[catalogKey][key];
            }
            // 隐藏人设还需清理白名单
            if (_currentPersonaTab === 'hidden' && _personaData.hidden_persona_whitelists) {
                delete _personaData.hidden_persona_whitelists[key];
            }
            renderPersonaEditor();
            showToast('🗑 已标记删除 "#' + key + ' ' + personaName + '"，请点击保存按钮生效', 'info');
        }

        async function savePersona() {
            if (!_personaData) { showToast('没有可保存的数据', 'error'); return; }
            const result = await postApi('/api/persona/save', _personaData);
            if (result && result.ok) {
                showToast('✅ ' + (result.message || '人设配置已保存'), 'success');
            } else {
                showToast('❌ 保存失败: ' + (result ? result.error : '网络错误'), 'error');
            }
        }

        // ====== 初始加载 ======
        refreshAll();
    </script>
</body>
</html>"""

