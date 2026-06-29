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
    <title>LiuYing - 登录</title>
    <style>
        :root { --bg: #eafff9; --card: rgba(255,255,255,0.78); --border: rgba(92,181,174,0.32); --text: #173b3f; --muted: #5c7e82; --accent: #31bfa7; --accent-2: #8be6ce; --danger: #ef6461; --success: #24b67a; --radius: 18px; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; background: radial-gradient(circle at 18% 20%, rgba(190,255,218,.75), transparent 26%), linear-gradient(135deg, #f4fff8 0%, #cdf8ee 42%, #b9eef1 100%); color: var(--text); min-height: 100vh; overflow-x:hidden; overflow-y:auto; }
        body:before { content:""; position:fixed; inset:0; background: linear-gradient(90deg, rgba(49,191,167,.1) 1px, transparent 1px), linear-gradient(180deg, rgba(49,191,167,.08) 1px, transparent 1px); background-size: 56px 56px; mask-image: linear-gradient(120deg, transparent 0%, #000 18%, #000 82%, transparent 100%); pointer-events:none; z-index:1; }
        body:after { content:"FIREFLY"; position:fixed; right:-26px; top:10vh; writing-mode:vertical-rl; font-size:108px; line-height:.8; font-weight:900; letter-spacing:.08em; color:rgba(37,142,138,.1); pointer-events:none; z-index:3; }
        .login-page { position:relative; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:44vh 20px 34px; }
        .login-hero { position:fixed; left:0; top:0; right:0; height:58vh; min-height:380px; overflow:hidden; z-index:0; background:#123b52; }
        .login-hero:before { content:""; position:absolute; inset:0; z-index:3; background: linear-gradient(180deg, rgba(7,33,48,.14), rgba(7,33,48,.02) 48%, rgba(234,255,249,.2) 78%, rgba(234,255,249,.82) 100%); pointer-events:none; }
        .login-hero:after { content:""; position:absolute; left:-4%; right:-4%; bottom:-1px; height:23%; z-index:4; background: rgba(234,255,249,.72); clip-path: ellipse(62% 48% at 50% 100%); backdrop-filter: blur(3px); pointer-events:none; }
        .wallpaper-track { position:absolute; inset:0; }
        .wallpaper-track img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position: 0% 20%; opacity:0; transform:scale(1.08); animation: loginWallpaper 36s infinite ease-in-out; filter:saturate(1.04); }
        .wallpaper-track img:nth-child(2) { animation-delay:6s; }
        .wallpaper-track img:nth-child(3) { animation-delay:12s; }
        .wallpaper-track img:nth-child(4) { animation-delay:18s; }
        .wallpaper-track img:nth-child(5) { animation-delay:24s; }
        .wallpaper-track img:nth-child(6) { animation-delay:30s; }
        @keyframes loginWallpaper {
            0%, 13% { opacity:0; transform:scale(1.08) translateX(0); }
            18%, 30% { opacity:1; transform:scale(1.02) translateX(-1.2%); }
            35%, 100% { opacity:0; transform:scale(1.08) translateX(-2.2%); }
        }
        .hero-text { position:absolute; left:50%; top:39%; transform:translate(-50%,-50%); z-index:5; text-align:center; color:#fff; text-shadow:0 4px 26px rgba(0,0,0,.36); width:min(90vw, 900px); }
        .hero-title { font-size:clamp(36px, 5vw, 72px); line-height:1.05; font-weight:850; letter-spacing:.02em; }
        .hero-subtitle { margin-top:18px; font-size:clamp(17px, 2.1vw, 28px); font-weight:600; color:rgba(255,255,255,.88); min-height:1.5em; }
        .hero-subtitle:after { content:""; display:inline-block; width:2px; height:.9em; margin-left:4px; background:rgba(255,255,255,.82); vertical-align:-.1em; animation: caretBlink 1s steps(1) infinite; }
        @keyframes caretBlink { 50% { opacity:0; } }
        .hero-shine { position:absolute; inset:-20%; z-index:2; background: radial-gradient(circle at 50% 15%, rgba(255,255,255,.25), transparent 18%), linear-gradient(115deg, transparent 12%, rgba(255,255,255,.18) 30%, transparent 42%); mix-blend-mode:screen; animation: heroShine 10s ease-in-out infinite; pointer-events:none; }
        @keyframes heroShine { 0%,100% { transform:translateX(-4%); opacity:.45; } 50% { transform:translateX(5%); opacity:.85; } }
        .login-card { position:relative; z-index:6; background: var(--card); border: 1px solid rgba(255,255,255,.64); border-radius: var(--radius); padding: 44px 40px 36px; width: 400px; max-width: 92vw; box-shadow: 0 30px 100px rgba(48,151,144,0.26), inset 0 1px 0 rgba(255,255,255,.82); backdrop-filter: blur(22px); overflow:hidden; }
        .login-card:before { content:""; position:absolute; inset:0; background: linear-gradient(135deg, rgba(255,255,255,.88), transparent 36%), radial-gradient(circle at 86% 12%, rgba(139,230,206,.55), transparent 28%); pointer-events:none; }
        .login-card:after { content:""; position:absolute; right:22px; top:22px; width:58px; height:58px; border:2px solid rgba(49,191,167,.32); border-left-color:transparent; border-bottom-color:transparent; transform:rotate(45deg); border-radius:16px 16px 4px 16px; pointer-events:none; }
        .login-card > * { position:relative; z-index:1; }
        .login-card h1 { font-size: 30px; text-align: center; margin-bottom: 2px; color:#124c4f; letter-spacing:.02em; }
        .login-card .sub { text-align: center; color: var(--muted); font-size: 13px; margin-bottom: 24px; }
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 13px; color: var(--muted); margin-bottom: 4px; }
        .form-group input { width: 100%; padding: 11px 13px; background: rgba(255,255,255,.62); border: 1px solid var(--border); border-radius: 10px; color: var(--text); font-size: 14px; box-shadow: inset 0 1px 0 rgba(255,255,255,.7); }
        .form-group input:focus { border-color: var(--accent); outline: none; box-shadow: 0 0 0 4px rgba(49,191,167,.14); }
        .btn { width: 100%; padding: 11px; border: none; border-radius: 10px; font-size: 14px; cursor: pointer; font-weight: 700; }
        .btn-primary { background: linear-gradient(135deg, #29b99f, #8be6ce); color: #083c3e; box-shadow: 0 12px 28px rgba(49,191,167,.32); }
        .btn-primary:hover { transform: translateY(-1px); filter: saturate(1.06); }
        .btn-danger { background: var(--danger); color: #fff; }
        .toast { position: fixed; top: 20px; right: 20px; padding: 10px 18px; border-radius: 10px; color: #fff; font-size: 13px; z-index: 9999; display: none; box-shadow:0 14px 34px rgba(20,86,83,.22); }
        .toast-error { background: var(--danger); }
        .toast-success { background: var(--success); }
        .toast-info { background: var(--accent); }
        .modal { position: fixed; inset: 0; background: rgba(12,63,66,0.34); display: none; align-items: center; justify-content: center; z-index: 10000; backdrop-filter: blur(8px); }
        .modal-card { background: var(--card); border:1px solid var(--border); border-radius: var(--radius); padding: 28px; width: 360px; max-width: 95vw; box-shadow: 0 24px 80px rgba(48,151,144,0.24); }
        .modal-card h3 { margin-bottom: 12px; font-size: 16px; }
        .modal-card .btn { margin-top: 8px; }
        .skip-link { text-align: center; margin-top: 10px; font-size: 12px; color: var(--muted); cursor: pointer; }
        .skip-link:hover { color: var(--text); }
        @media (max-width: 768px) {
            .login-page { padding-top: 36vh; align-items:flex-start; }
            .login-hero { height:44vh; min-height:300px; }
            .hero-text { top:34%; }
            .hero-title { font-size:36px; }
            .hero-subtitle { font-size:16px; margin-top:12px; }
            .login-card { padding:34px 26px 28px; }
        }
    </style>
</head>
<body>
    <div class="login-hero">
        <div class="wallpaper-track">
            <img src="/screenshots/firefly-login-d1.avif" alt="">
            <img src="/screenshots/firefly-login-d2.avif" alt="">
            <img src="/screenshots/firefly-login-d3.avif" alt="">
            <img src="/screenshots/firefly-login-d4.avif" alt="">
            <img src="/screenshots/firefly-login-d5.avif" alt="">
            <img src="/screenshots/firefly-login-d6.avif" alt="">
        </div>
        <div class="hero-shine"></div>
        <div class="hero-text">
            <div class="hero-title">Lovely firefly!</div>
            <div class="hero-subtitle" id="hero-subtitle">From Undreamt Night, I Thence Shine</div>
        </div>
    </div>
    <div class="login-page">
        <div class="login-card">
            <h1><img src="/screenshots/main.jpg" onerror="this.style.display='none'" style="width:40px;height:40px;border-radius:10px;vertical-align:middle;margin-right:8px;object-fit:cover;">LiuYing</h1>
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
        (function initHeroTypewriter() {
            const el = document.getElementById('hero-subtitle');
            if (!el) return;
            const lines = [
                'In Reddened Chrysalis, I Once Rest',
                'From Shattered Sky, I Free Fall',
                'Amidst Silenced Stars, I Deep Sleep',
                'Upon Lighted Fyrefly, I Soon Gaze',
                'From Undreamt Night, I Thence Shine',
                'In Finalized Morrow, I Full Bloom'
            ];
            let line = 4, index = lines[line].length, deleting = true;
            function tick() {
                const text = lines[line];
                el.textContent = text.slice(0, index);
                if (deleting) {
                    index--;
                    if (index <= 0) {
                        deleting = false;
                        line = (line + 1) % lines.length;
                    }
                } else {
                    index++;
                    if (index >= lines[line].length) {
                        deleting = true;
                        setTimeout(tick, 1800);
                        return;
                    }
                }
                setTimeout(tick, deleting ? 45 : 88);
            }
            setTimeout(tick, 1600);
        })();
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
    <title>LiuYing - 管理面板</title>
    <link rel="icon" href="/screenshots/main.jpg">
    <style>
        :root {
            --bg-primary: #eafff9;
            --bg-secondary: rgba(246,255,252,0.78);
            --bg-card: rgba(255,255,255,0.72);
            --bg-hover: rgba(115,222,200,0.18);
            --border: rgba(74,172,165,0.28);
            --text-primary: #123d42;
            --text-secondary: #50777c;
            --text-muted: #7d989b;
            --accent: #27b99f;
            --accent-hover: #1aa58f;
            --success: #22c55e;
            --warning: #d99526;
            --danger: #e85b61;
            --cyan: #36c6d6;
            --purple: #91a7ff;
            --firefly: #b8f7d6;
            --teal-dark: #0d585b;
            --radius: 16px;
            --radius-sm: 8px;
            --shadow: 0 18px 48px rgba(49,145,139,0.18), 0 2px 8px rgba(49,145,139,0.08);
            --transition: all 0.22s ease;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background:
                radial-gradient(circle at 20% 10%, rgba(189,255,219,0.9), transparent 26%),
                radial-gradient(circle at 86% 8%, rgba(93,206,215,0.5), transparent 30%),
                radial-gradient(circle at 70% 92%, rgba(189,255,219,0.48), transparent 28%),
                linear-gradient(135deg, #f7fff9 0%, #d7fbef 45%, #c3eff2 100%);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
        }
        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(39,185,159,0.09) 1px, transparent 1px),
                linear-gradient(180deg, rgba(39,185,159,0.07) 1px, transparent 1px);
            background-size: 64px 64px;
            mask-image: linear-gradient(110deg, rgba(0,0,0,.2), rgba(0,0,0,.75) 42%, transparent 95%);
            pointer-events: none;
            z-index: -2;
        }
        body::after {
            content: "FIREFLY";
            position: fixed;
            right: -18px;
            top: 7vh;
            writing-mode: vertical-rl;
            font-size: clamp(64px, 9vw, 132px);
            line-height: .78;
            font-weight: 900;
            letter-spacing: .08em;
            color: rgba(19,103,103,0.065);
            pointer-events: none;
            z-index: -1;
        }
        ::selection { background: rgba(139,230,206,.45); color: #0b3a3d; }
        /* 侧边栏 */
        .sidebar {
            position: fixed;
            left: 0; top: 0; bottom: 0;
            width: 264px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.86), rgba(230,255,248,0.62)),
                radial-gradient(circle at 0 0, rgba(139,230,206,.42), transparent 32%);
            border-right: 1px solid var(--border);
            padding: 22px 0;
            overflow-y: auto;
            z-index: 100;
            box-shadow: 18px 0 48px rgba(58,154,149,.14);
            backdrop-filter: blur(22px);
        }
        .sidebar-logo {
            padding: 0 22px 22px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
        }
        .sidebar-logo .logo-icon {
            width: 46px; height: 46px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            overflow: hidden;
            border: 1px solid rgba(39,185,159,.32);
            box-shadow: 0 8px 26px rgba(39,185,159,.25);
        }
        .sidebar-logo .logo-icon img {
            width: 100%; height: 100%;
            object-fit: cover;
            border-radius: 14px;
        }
        .sidebar-logo h1 { font-size: 20px; font-weight: 800; color: var(--teal-dark); letter-spacing:.02em; }
        .sidebar-logo .ver { font-size: 11px; color: var(--text-muted); }
        .sidebar-logo::after {
            content: "✦";
            position: absolute;
            right: 20px;
            top: 4px;
            width: 26px;
            height: 26px;
            display: grid;
            place-items: center;
            border-radius: 50%;
            color: #27b99f;
            background: rgba(255,255,255,.48);
            border: 1px solid rgba(39,185,159,.22);
            box-shadow: 0 0 22px rgba(139,230,206,.46);
            animation: emblemPulse 2.8s ease-in-out infinite;
        }
        @keyframes emblemPulse {
            0%,100% { transform: scale(1); opacity:.64; }
            50% { transform: scale(1.12); opacity:1; }
        }
        .nav-item {
            display: flex; align-items: center; gap: 10px;
            padding: 10px 16px; margin: 4px 12px;
            border-radius: 12px;
            cursor: pointer;
            color: var(--text-secondary);
            transition: var(--transition);
            font-size: 14px;
            user-select: none;
            border: 1px solid transparent;
            position: relative;
        }
        .nav-item:hover { background: var(--bg-hover); color: var(--text-primary); border-color: rgba(39,185,159,.18); }
        .nav-item.active {
            background: linear-gradient(135deg, rgba(39,185,159,.95), rgba(155,237,210,.9));
            color: #083f42;
            box-shadow: 0 12px 28px rgba(39,185,159,.24);
            font-weight: 700;
        }
        .nav-item.active::after { content:""; position:absolute; right:10px; width:7px; height:7px; border-radius:50%; background:#eafff9; box-shadow:0 0 14px #eafff9; }
        .nav-item .nav-icon { font-size: 18px; width: 24px; text-align: center; }
        .nav-icon-img { width: 20px; height: 20px; object-fit: contain; flex-shrink: 0; vertical-align: middle; }
        .nav-divider {
            border-top: 1px solid var(--border);
            margin: 10px 22px;
        }
        .nav-label {
            padding: 10px 22px 4px;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            font-weight: 800;
        }
        /* 主内容 */
        .main {
            margin-left: 264px;
            padding: 32px 34px 44px;
            min-height: 100vh;
        }
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        .page-header {
            margin-bottom: 22px;
            padding: 20px 22px;
            border: 1px solid rgba(74,172,165,0.22);
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(255,255,255,.68), rgba(226,255,247,.42));
            box-shadow: 0 12px 34px rgba(49,145,139,.1);
            backdrop-filter: blur(18px);
            overflow: hidden;
            position: relative;
        }
        .page-header::after { content:""; position:absolute; right:18px; top:14px; width:72px; height:72px; border:2px solid rgba(39,185,159,.2); border-left-color:transparent; border-bottom-color:transparent; transform:rotate(45deg); border-radius:18px 18px 4px 18px; pointer-events:none; }
        .page-header::before { content:"FIREFLY OS"; position:absolute; right:116px; bottom:14px; font-size:11px; font-weight:900; letter-spacing:.22em; color:rgba(13,88,91,.16); pointer-events:none; }
        .page-header h2 {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-size: 26px;
            font-weight: 850;
            color: var(--teal-dark);
            padding: 2px 12px 4px 0;
            text-shadow: 0 6px 24px rgba(39,185,159,.18);
        }
        .page-header h2::before {
            content:"";
            width: 12px;
            height: 28px;
            border-radius: 999px;
            background: linear-gradient(180deg, #9befd2, #27b99f);
            box-shadow: 0 0 22px rgba(139,230,206,.72);
        }
        .page-header p {
            display: inline-flex;
            margin-top: 8px;
            padding: 5px 12px;
            border-radius: 999px;
            color: var(--text-secondary);
            font-size: 14px;
            background: rgba(255,255,255,.42);
            border: 1px solid rgba(39,185,159,.14);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.56);
        }
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
            padding: 22px;
            transition: var(--transition);
            box-shadow: 0 8px 24px rgba(49,145,139,.08), inset 0 1px 0 rgba(255,255,255,.72);
            backdrop-filter: blur(18px);
            position: relative;
            overflow: hidden;
        }
        .stat-card::before { content:""; position:absolute; inset:0; background: linear-gradient(135deg, rgba(255,255,255,.52), transparent 36%), radial-gradient(circle at 90% 12%, rgba(184,247,214,.35), transparent 28%); pointer-events:none; }
        .stat-card::after {
            content:"";
            position:absolute;
            right:-20px;
            bottom:-22px;
            width: 108px;
            height: 108px;
            border-radius: 50%;
            background: radial-gradient(circle at 32% 28%, rgba(255,255,255,.74), rgba(139,230,206,.22) 42%, transparent 70%);
            border: 1px solid rgba(255,255,255,.36);
            opacity: .42;
            pointer-events:none;
        }
        .stat-card:hover::after { opacity: .62; transform: translate(-8px, -6px) scale(1.04); transition: var(--transition); }
        .stat-card:hover::before {
            background:
                linear-gradient(115deg, transparent 0%, rgba(255,255,255,.58) 42%, transparent 54%) -140% 0 / 220% 100% no-repeat,
                linear-gradient(135deg, rgba(255,255,255,.52), transparent 36%),
                radial-gradient(circle at 90% 12%, rgba(184,247,214,.35), transparent 28%);
            animation: cardSweep 1.6s ease;
        }
        @keyframes cardSweep {
            from { background-position: -140% 0, 0 0, 0 0; }
            to { background-position: 160% 0, 0 0, 0 0; }
        }
        .stat-card > * { position: relative; z-index: 1; }
        .stat-card:hover { border-color: rgba(39,185,159,.55); transform: translateY(-3px); box-shadow: var(--shadow); }
        .stat-card-header {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 12px;
        }
        .stat-card-title {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            width: fit-content;
            max-width: 100%;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 13px;
            color: var(--teal-dark);
            font-weight: 800;
            background: linear-gradient(135deg, rgba(255,255,255,.66), rgba(226,255,247,.42));
            border: 1px solid rgba(39,185,159,.16);
            box-shadow: 0 8px 18px rgba(39,185,159,.08), inset 0 1px 0 rgba(255,255,255,.62);
        }
        .stat-card-title::before {
            content:"";
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #9befd2;
            box-shadow: 0 0 14px rgba(39,185,159,.72);
            flex: 0 0 auto;
        }
        .stat-card-icon {
            width: 32px; height: 32px;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 16px;
        }
        .stat-card-icon.random-art-icon {
            width: 48px;
            height: 48px;
            border-radius: 14px;
            padding: 7px;
            background: linear-gradient(135deg, rgba(206,246,232,.96), rgba(179,236,236,.72)) !important;
            border: 1px solid rgba(39,185,159,.18);
            box-shadow: 0 12px 28px rgba(39,185,159,.14), inset 0 1px 0 rgba(255,255,255,.65);
        }
        .stat-card-icon.random-art-icon img,
        .inline-random-icon {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
            filter: drop-shadow(0 5px 8px rgba(39,185,159,.2));
        }
        .title-random-icon {
            width: 22px;
            height: 22px;
            object-fit: contain;
            margin-right: 6px;
            vertical-align: -5px;
            filter: drop-shadow(0 4px 7px rgba(39,185,159,.18));
        }
        .ui-action-icon {
            width: 16px;
            height: 16px;
            object-fit: contain;
            margin-right: 5px;
            vertical-align: -3px;
            filter: drop-shadow(0 3px 6px rgba(39,185,159,.18));
        }
        .badge .ui-action-icon,
        .whitelist-tag .ui-action-icon {
            width: 14px;
            height: 14px;
            margin-right: 4px;
        }
        .stat-card-value {
            font-size: 28px;
            font-weight: 850;
            color: var(--teal-dark);
            letter-spacing: 0;
        }
        .stat-card-sub {
            font-size: 13px;
            color: #5f8286;
            margin-top: 12px;
            line-height: 1.9;
        }
        .stat-card-sub:not(:empty) {
            padding: 10px 12px;
            border-radius: 13px;
            background:
                linear-gradient(135deg, rgba(255,255,255,.42), rgba(232,255,249,.22)),
                radial-gradient(circle at 92% 8%, rgba(139,230,206,.28), transparent 24%);
            border: 1px solid rgba(39,185,159,.1);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.46);
        }
        .stat-card-sub br {
            display: block;
            content: "";
            margin: 5px 0;
        }
        /* 进度条 */
        .progress-bar {
            height: 6px;
            background: rgba(255,255,255,.48);
            border-radius: 3px;
            margin-top: 8px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.6s ease;
        }
        .progress-fill.green { background: linear-gradient(90deg, #22c55e, #9befd2); }
        .progress-fill.blue { background: linear-gradient(90deg, #27b99f, #72dbe5); }
        .progress-fill.yellow { background: linear-gradient(90deg, #d99526, #ffe6a3); }
        .progress-fill.red { background: linear-gradient(90deg, #e85b61, #ffb6b1); }
        .progress-fill.purple { background: linear-gradient(90deg, #91a7ff, #c8d6ff); }
        /* 表格 */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
            margin-bottom: 20px;
            box-shadow: 0 10px 28px rgba(49,145,139,.09), inset 0 1px 0 rgba(255,255,255,.7);
            backdrop-filter: blur(18px);
            position: relative;
        }
        .card::after { content:""; position:absolute; right:16px; top:14px; width:34px; height:34px; border:1px solid rgba(39,185,159,.14); border-left-color:transparent; border-bottom-color:transparent; border-radius:10px 10px 2px 10px; transform:rotate(45deg); pointer-events:none; }
        .card-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(90deg, rgba(232,255,249,.72), rgba(255,255,255,.2));
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card-header h3 {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            width: fit-content;
            max-width: calc(100% - 60px);
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 15px;
            font-weight: 800;
            color: var(--teal-dark);
            background: rgba(255,255,255,.48);
            border: 1px solid rgba(39,185,159,.14);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.6);
        }
        .card-header h3::after {
            content:"";
            width: 28px;
            height: 1px;
            background: linear-gradient(90deg, rgba(39,185,159,.42), transparent);
        }
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
            background: rgba(225,255,247,.62);
            color: var(--text-secondary);
            font-weight: 800;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }
        td { border-top: 1px solid var(--border); }
        td:first-child {
            color: var(--teal-dark);
        }
        #page-help-page td:first-child,
        #page-commands td:first-child {
            font-weight: 800;
            position: relative;
        }
        #page-help-page td:first-child:not(:only-child)::before,
        #page-commands td:first-child:not(:only-child)::before {
            content:"";
            display:inline-block;
            width: 7px;
            height: 7px;
            margin-right: 8px;
            border-radius: 50%;
            background: rgba(39,185,159,.52);
            box-shadow: 0 0 12px rgba(139,230,206,.72);
            vertical-align: 1px;
        }
        td code {
            border-radius: 999px !important;
            border: 1px solid rgba(39,185,159,.12);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.46);
        }
        table span[style*="background:var(--bg-primary)"],
        table code[style*="background:var(--bg-primary)"],
        .card-body span[style*="background:var(--bg-primary)"],
        .card-body code[style*="background:var(--bg-primary)"] {
            display: inline-flex !important;
            align-items: center;
            gap: 4px;
            padding: 3px 9px !important;
            margin: 3px 4px 3px 0 !important;
            border-radius: 999px !important;
            background: linear-gradient(135deg, rgba(207,245,232,.96), rgba(231,255,248,.78)) !important;
            color: #09876f !important;
            border: 1px solid rgba(39,185,159,.16) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.72), 0 6px 14px rgba(39,185,159,.08);
            font-weight: 700;
        }
        table span[style*="background:var(--bg-primary)"]::before,
        table code[style*="background:var(--bg-primary)"]::before,
        .card-body span[style*="background:var(--bg-primary)"]::before,
        .card-body code[style*="background:var(--bg-primary)"]::before {
            content: "#";
            color: #27b99f;
            font-weight: 900;
        }
        #store-list span[style*="border-radius:4px"],
        #github-plugins-list span[style*="border-radius:4px"] {
            display: inline-flex !important;
            align-items: center;
            padding: 3px 9px !important;
            border-radius: 999px !important;
            background: rgba(207,245,232,.88) !important;
            border: 1px solid rgba(39,185,159,.16);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.6);
            font-size: 11px !important;
            font-weight: 750;
        }
        #store-list span[style*="border-radius:4px"]::before,
        #github-plugins-list span[style*="border-radius:4px"]::before {
            content:"#";
            margin-right: 2px;
            color: #27b99f;
        }
        #plugin-table td:nth-child(3),
        #store-list div[style*="font-size:12px;color:var(--text-secondary)"],
        #github-plugins-list div[style*="font-size:12px;color:var(--text-secondary)"] {
            position: relative;
            padding: 6px 10px !important;
            border-radius: 12px;
            background: rgba(255,255,255,.34);
            border: 1px solid rgba(39,185,159,.08);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.42);
            line-height: 1.55;
        }
        #plugin-table td:nth-child(3):empty {
            background: transparent;
            border-color: transparent;
            box-shadow: none;
        }
        tr:hover td { background: linear-gradient(90deg, rgba(184,247,214,.2), rgba(115,222,200,.12)); }
        tr.disabled-row td { opacity: 0.5; }
        tr.disabled-row:hover td { opacity: 0.75; background: var(--bg-hover); }
        #page-help-page .stat-grid {
            grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
            align-items: stretch;
        }
        #page-help-page .stat-card {
            min-height: 184px;
            padding: 24px;
            background:
                linear-gradient(145deg, rgba(255,255,255,.82), rgba(232,255,249,.5)),
                radial-gradient(circle at 18% 12%, rgba(255,255,255,.72), transparent 28%),
                radial-gradient(circle at 90% 90%, rgba(139,230,206,.28), transparent 30%);
        }
        #page-help-page .stat-card::after {
            right: 16px;
            bottom: 14px;
            width: 54px;
            height: 54px;
            opacity: .32;
        }
        #page-help-page .stat-card::before {
            background:
                linear-gradient(90deg, rgba(39,185,159,.4), transparent 42%) left bottom / 64% 2px no-repeat,
                radial-gradient(circle at 88% 18%, rgba(139,230,206,.36), transparent 24%);
        }
        #page-help-page .stat-card-title {
            font-size: 15px;
            margin-bottom: 4px;
        }
        #page-help-page .help-title-icon {
            width: 22px;
            height: 22px;
            object-fit: contain;
            flex: 0 0 auto;
            filter: drop-shadow(0 6px 10px rgba(39,185,159,.18));
        }
        #page-help-page .help-title-fallback {
            display: none;
            font-size: 17px;
            line-height: 1;
        }
        #page-help-page .stat-card-sub {
            font-size: 14px;
            color: #587d82;
        }
        #page-help-page .card {
            background:
                linear-gradient(145deg, rgba(255,255,255,.82), rgba(235,255,249,.56)),
                radial-gradient(circle at 95% 0%, rgba(139,230,206,.28), transparent 20%);
        }
        #page-help-page table td {
            padding: 14px 22px;
            font-size: 14px;
        }
        #page-help-page table td:first-child {
            width: 230px;
        }
        /* 标签 */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 100px;
            font-size: 11px;
            font-weight: 600;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.48);
        }
        .badge-success { background: rgba(34,197,94,0.15); color: #158a55; }
        .badge-warning { background: rgba(217,149,38,0.16); color: #9a6510; }
        .badge-danger { background: rgba(232,91,97,0.14); color: var(--danger); }
        .badge-info { background: rgba(39,185,159,0.16); color: var(--accent); }
        .badge-purple { background: rgba(145,167,255,0.18); color: #6179db; }
        /* 按钮 */
        .btn {
            padding: 7px 16px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,.58);
            color: var(--text-primary);
            border-radius: var(--radius-sm);
            cursor: pointer;
            font-size: 13px;
            transition: var(--transition);
            white-space: nowrap;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.65);
        }
        .btn:hover { background: var(--bg-hover); border-color: rgba(39,185,159,.44); transform: translateY(-1px); }
        .btn-primary { background: linear-gradient(135deg, #27b99f, #9befd2); border-color: transparent; color: #083f42; font-weight: 800; }
        .btn-primary:hover { background: linear-gradient(135deg, var(--accent-hover), #8be6ce); }
        .btn-sm { padding: 4px 10px; font-size: 12px; }
        /* 日志区 */
        .log-container {
            background: linear-gradient(180deg, rgba(10,40,43,.96), rgba(7,29,33,.96));
            border-radius: var(--radius-sm);
            padding: 16px;
            height: 450px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
            font-size: 12px;
            line-height: 1.8;
            border: 1px solid rgba(139,230,206,.18);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
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
            --bg-primary: #f8fff9;
            --bg-secondary: rgba(255,255,255,0.86);
            --bg-card: rgba(255,255,255,0.82);
            --bg-hover: rgba(115,222,200,0.14);
            --border: rgba(74,172,165,0.22);
            --text-primary: #143c40;
            --text-secondary: #5c7e82;
            --text-muted: #8ca5a7;
            --shadow: 0 12px 34px rgba(49,145,139,0.12);
        }
        body.light-theme .log-container { background: #effbf8; }
        body.light-theme .config-item-input input, body.light-theme .config-item-input select { background: #f8fafc; }
        /* 主题切换按钮 */
        .theme-toggle {
            position: fixed; bottom: 20px; left: 20px; z-index: 200;
            width: 42px; height: 42px; border-radius: 14px;
            background: rgba(255,255,255,.72); border: 1px solid var(--border);
            color: var(--text-primary); cursor: pointer; font-size: 16px;
            display: flex; align-items: center; justify-content: center;
            transition: var(--transition);
            box-shadow: 0 10px 28px rgba(49,145,139,.16);
            backdrop-filter: blur(16px);
        }
        .theme-toggle:hover { border-color: var(--accent); }
        /* 汉堡菜单按钮 */
        .hamburger {
            display: none; position: fixed; top: 12px; left: 12px; z-index: 300;
            width: 40px; height: 40px; border-radius: 12px;
            background: linear-gradient(135deg, #27b99f, #9befd2); border: none; color: #083f42;
            font-size: 18px; cursor: pointer;
            box-shadow: 0 10px 28px rgba(39,185,159,.24);
        }
        /* 移动端适配 */
        @media (max-width: 768px) {
            .hamburger { display: flex; align-items: center; justify-content: center; }
            .sidebar {
                transform: translateX(-100%);
                width: 244px; padding: 14px 0;
                transition: transform 0.25s ease;
            }
            .sidebar.open { transform: translateX(0); }
            .sidebar-logo { padding: 0 16px 12px; }
            .sidebar-logo h1, .sidebar-logo .ver, .nav-item span:not(.nav-icon), .nav-label { display: block; }
            .nav-item { justify-content: flex-start; padding: 10px 16px; margin: 2px 8px; }
            .main { margin-left: 0 !important; padding: 56px 12px 16px !important; }
            .page-header { padding: 16px; border-radius: 14px; }
            .page-header::after { width: 48px; height: 48px; opacity:.55; }
            .page-header h2 { font-size: 22px; }
            .stat-grid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }
            .stat-card { padding: 14px; }
            .stat-card-value { font-size: 22px; }
            table { font-size: 11px; }
            th, td { padding: 6px 8px; }
            .config-modal { width: 95vw !important; }
            .page-header { flex-direction: column; align-items: flex-start; gap: 8px; }
            .page-header .btn, .page-header > div { width: 100%; }
            #token-summary-cards { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
            #bot-info-content > div { min-width: 100% !important; }
            input[type="text"], input[type="password"], select { max-width: 100%; }
            .sam-frame, .star-rail, .deco-flower.f2, .scanline-glow, .circuit-lines { display: none; }
            .deco-bubble.b1 { left: 78%; top: 86px; width: 54px; height: 54px; }
            .deco-bubble.b3 { width: 72px; height: 72px; right: 12px; bottom: 68px; }
            .theme-toggle { bottom: 16px; left: auto; right: 16px; }
        }
        /* 侧边栏遮罩 */
        .sidebar-overlay {
            display: none; position: fixed; inset: 0; z-index: 99;
            background: rgba(10,72,76,0.28);
            backdrop-filter: blur(6px);
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
            color: #083f42;
            font-size: 14px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255,255,255,.42);
        }
        @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        .toast-success { background: linear-gradient(135deg, #9befd2, #dffff4); }
        .toast-error { background: linear-gradient(135deg, #ffb6b1, #ffe6e5); color:#762022; }
        .toast-info { background: linear-gradient(135deg, #8be6ce, #dffff4); }
        /* 配置编辑弹窗 */
        .config-overlay {
            position: fixed; inset: 0;
            background: rgba(11,72,76,0.34);
            display: flex; align-items: center; justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(10px);
        }
        .config-modal {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 18px;
            width: 560px; max-width: 95vw; max-height: 80vh;
            display: flex; flex-direction: column;
            box-shadow: 0 24px 80px rgba(31,118,113,0.25), inset 0 1px 0 rgba(255,255,255,.72);
            animation: fadeIn 0.2s ease;
            backdrop-filter: blur(22px);
            overflow: hidden;
        }
        .config-modal-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            display: flex; align-items: center; justify-content: space-between;
            background: linear-gradient(90deg, rgba(232,255,249,.78), rgba(255,255,255,.36));
        }
        .config-modal-header h3 { font-size: 16px; color: var(--teal-dark); }
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
            background: rgba(255,255,255,.58);
            border: 1px solid var(--border);
            color: var(--text-primary);
            border-radius: 10px;
            padding: 6px 10px;
            font-size: 13px;
            font-family: inherit;
            width: 100%;
            box-sizing: border-box;
        }
        .config-item-input input:focus, .config-item-input select:focus { border-color: var(--accent); outline: none; box-shadow: 0 0 0 3px rgba(39,185,159,.13); }
        .config-item-comment {
            font-size: 11px;
            color: var(--text-muted);
        }
        .config-item-type {
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(225,255,247,.62);
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
            font-weight: 700;
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
            box-shadow: 0 10px 28px rgba(49,145,139,.08);
            backdrop-filter: blur(18px);
        }
        .persona-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 16px;
            background: linear-gradient(90deg, rgba(232,255,249,.72), rgba(255,255,255,.3));
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            user-select: none;
        }
        .persona-card-header:hover { background: rgba(115,222,200,0.18); }
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
            background: rgba(255,255,255,.58);
            border: 1px solid var(--border);
            border-radius: 10px;
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
            box-shadow: 0 0 0 3px rgba(39,185,159,0.14);
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
            background: rgba(255,255,255,.58);
            border: 1px solid var(--border);
            border-radius: 10px;
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
            background: rgba(225,255,247,.62);
            border: 1px solid var(--border);
            border-radius: 999px;
            font-size: 12px;
            margin: 2px 4px 2px 0;
        }
        .whitelist-tag .remove-tag {
            cursor: pointer;
            color: var(--danger);
            font-weight: bold;
            margin-left: 2px;
        }
        .firefly-field {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        .firefly-dot {
            position: absolute;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #ddfff0;
            box-shadow: 0 0 18px #8be6ce, 0 0 34px rgba(39,185,159,.55);
            opacity: .65;
            animation: fireflyFloat 8s ease-in-out infinite;
        }
        .firefly-dot:nth-child(1) { left: 18%; top: 14%; animation-delay: -1s; }
        .firefly-dot:nth-child(2) { left: 76%; top: 18%; animation-delay: -3s; transform: scale(.75); }
        .firefly-dot:nth-child(3) { left: 62%; top: 78%; animation-delay: -5s; transform: scale(.9); }
        .firefly-dot:nth-child(4) { left: 90%; top: 55%; animation-delay: -2s; transform: scale(.65); }
        .firefly-dot:nth-child(5) { left: 34%; top: 88%; animation-delay: -6s; transform: scale(.8); }
        .firefly-dot:nth-child(6) { left: 48%; top: 24%; animation-delay: -7s; transform: scale(.55); }
        .firefly-dot:nth-child(7) { left: 84%; top: 86%; animation-delay: -4s; transform: scale(.7); }
        @keyframes fireflyFloat {
            0%, 100% { translate: 0 0; opacity: .38; }
            35% { translate: 18px -22px; opacity: .85; }
            70% { translate: -14px 12px; opacity: .55; }
        }
        .theme-deco {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }
        .deco-bubble {
            position: absolute;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,.58);
            background:
                radial-gradient(circle at 30% 26%, rgba(255,255,255,.76), rgba(255,255,255,.18) 34%, rgba(139,230,206,.12) 70%);
            box-shadow: inset 0 1px 8px rgba(255,255,255,.42), 0 12px 42px rgba(39,185,159,.14);
            opacity: .45;
            animation: bubbleDrift 14s ease-in-out infinite;
        }
        .deco-bubble.b1 { width: 86px; height: 86px; left: 288px; top: 72px; animation-delay: -2s; }
        .deco-bubble.b2 { width: 42px; height: 42px; right: 150px; top: 190px; animation-delay: -8s; }
        .deco-bubble.b3 { width: 120px; height: 120px; right: 72px; bottom: 96px; animation-delay: -5s; opacity:.28; }
        .deco-bubble.b4 { width: 34px; height: 34px; left: 52%; bottom: 12%; animation-delay: -10s; }
        @keyframes bubbleDrift {
            0%, 100% { transform: translate3d(0,0,0) scale(1); }
            45% { transform: translate3d(16px,-28px,0) scale(1.04); }
            75% { transform: translate3d(-12px,10px,0) scale(.98); }
        }
        .deco-flower {
            position: absolute;
            width: 76px;
            height: 76px;
            opacity: .2;
            filter: drop-shadow(0 12px 24px rgba(39,185,159,.18));
            animation: flowerSpin 18s linear infinite;
        }
        .deco-flower::before,
        .deco-flower::after {
            content:"";
            position:absolute;
            inset: 17px;
            border: 2px solid rgba(13,88,91,.26);
            border-radius: 28px 28px 4px 28px;
            transform: rotate(45deg);
            background: linear-gradient(135deg, rgba(255,255,255,.36), rgba(139,230,206,.1));
        }
        .deco-flower::after { transform: rotate(135deg); }
        .deco-flower.f1 { right: 52px; top: 38px; }
        .deco-flower.f2 { left: 286px; bottom: 64px; transform: scale(.7); animation-direction: reverse; }
        @keyframes flowerSpin {
            from { rotate: 0deg; }
            to { rotate: 360deg; }
        }
        .sam-frame {
            position: fixed;
            right: -36px;
            top: 28%;
            width: 190px;
            height: 360px;
            border: 1px solid rgba(13,88,91,.08);
            border-left: 0;
            border-radius: 28px 0 0 28px;
            opacity: .75;
            z-index: 0;
            pointer-events: none;
        }
        .sam-frame::before {
            content:"SAM";
            position:absolute;
            right: 42px;
            top: 36px;
            writing-mode: vertical-rl;
            font-size: 72px;
            line-height: .8;
            font-weight: 900;
            letter-spacing: .1em;
            color: rgba(13,88,91,.055);
        }
        .sam-frame::after {
            content:"";
            position:absolute;
            left: 34px;
            bottom: 44px;
            width: 96px;
            height: 96px;
            border: 10px solid rgba(39,185,159,.055);
            border-left-color: transparent;
            border-bottom-color: transparent;
            transform: rotate(45deg);
            border-radius: 20px;
        }
        .star-rail {
            position: fixed;
            left: 26%;
            top: 12%;
            width: 42vw;
            height: 1px;
            z-index: 0;
            pointer-events: none;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,.9), transparent);
            transform: rotate(-12deg);
            opacity: .36;
            animation: railGlide 9s ease-in-out infinite;
        }
        .star-rail::after {
            content:"";
            position:absolute;
            right: 35%;
            top: -3px;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #fff;
            box-shadow: 0 0 20px #8be6ce;
        }
        @keyframes railGlide {
            0%,100% { transform: translateX(-20px) rotate(-12deg); opacity:.18; }
            50% { transform: translateX(36px) rotate(-12deg); opacity:.42; }
        }
        .scanline-glow {
            position: fixed;
            left: 264px;
            right: 0;
            top: 0;
            height: 38vh;
            z-index: 0;
            pointer-events: none;
            background:
                linear-gradient(180deg, transparent 0%, rgba(255,255,255,.3) 45%, transparent 70%),
                linear-gradient(90deg, transparent, rgba(139,230,206,.28), transparent);
            opacity: .34;
            transform: translateY(-70%);
            animation: scanlineMove 7.5s ease-in-out infinite;
        }
        @keyframes scanlineMove {
            0%, 100% { transform: translateY(-76%); opacity: .08; }
            45%, 58% { transform: translateY(220%); opacity: .34; }
        }
        .circuit-lines {
            position: fixed;
            inset: 0 0 0 264px;
            z-index: 0;
            pointer-events: none;
            opacity: .22;
            background:
                linear-gradient(90deg, transparent 0 18px, rgba(13,88,91,.08) 18px 19px, transparent 19px 100%) 0 0 / 180px 100%,
                linear-gradient(180deg, transparent 0 46px, rgba(13,88,91,.08) 46px 47px, transparent 47px 100%) 0 0 / 100% 160px;
            mask-image: linear-gradient(90deg, transparent, #000 16%, #000 82%, transparent);
        }
        .theme-mark {
            position: fixed;
            right: 28px;
            bottom: 24px;
            z-index: 1;
            color: rgba(13,88,91,.18);
            font-weight: 900;
            letter-spacing: .16em;
            font-size: 12px;
            pointer-events: none;
        }
        .theme-mark::before {
            content: "";
            display: inline-block;
            width: 42px;
            height: 1px;
            margin-right: 10px;
            vertical-align: middle;
            background: currentColor;
        }
    </style>
</head>
<body>
    <div class="firefly-field" aria-hidden="true">
        <span class="firefly-dot"></span>
        <span class="firefly-dot"></span>
        <span class="firefly-dot"></span>
        <span class="firefly-dot"></span>
        <span class="firefly-dot"></span>
        <span class="firefly-dot"></span>
        <span class="firefly-dot"></span>
    </div>
    <div class="theme-deco" aria-hidden="true">
        <span class="deco-bubble b1"></span>
        <span class="deco-bubble b2"></span>
        <span class="deco-bubble b3"></span>
        <span class="deco-bubble b4"></span>
        <span class="deco-flower f1"></span>
        <span class="deco-flower f2"></span>
    </div>
    <div class="sam-frame" aria-hidden="true"></div>
    <div class="star-rail" aria-hidden="true"></div>
    <div class="scanline-glow" aria-hidden="true"></div>
    <div class="circuit-lines" aria-hidden="true"></div>
    <div class="theme-mark" aria-hidden="true">SAM · FIREFLY</div>
    <!-- 汉堡菜单 + 侧边栏遮罩 -->
    <button class="hamburger" onclick="toggleSidebar()" title="菜单">☰</button>
    <div class="sidebar-overlay" id="sidebar-overlay" onclick="toggleSidebar()"></div>
    <!-- 主题切换 -->
    <button class="theme-toggle" onclick="toggleTheme()" title="切换主题" id="theme-btn">🌙</button>
    <!-- 侧边栏 -->
    <aside class="sidebar">
        <div class="sidebar-logo">
            <div class="logo-icon"><img src="/screenshots/main.jpg" alt="logo" onerror="this.style.display='none'"></div>
            <div>
                <h1>LiuYing</h1>
                <div class="ver">v2.4.4 · Web UI</div>
            </div>
        </div>
        <div class="nav-label">主菜单</div>
        <div class="nav-item active" data-page="dashboard">
            <img src="/screenshots/仪表盘.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 仪表盘
        </div>
        <div class="nav-item" data-page="plugins">
            <img src="/screenshots/插件管理.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 插件管理
        </div>
        <div class="nav-item" data-page="bots">
            <img src="/screenshots/Bot连接.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> Bot 连接
        </div>
        <div class="nav-divider"></div>
        <div class="nav-label">工具</div>
        <div class="nav-item" data-page="logs">
            <img src="/screenshots/实时日志.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 实时日志
        </div>
        <div class="nav-item" data-page="commands">
            <img src="/screenshots/指令列表.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 指令列表
        </div>
        <div class="nav-item" data-page="bot-info">
            <img src="/screenshots/用户配置.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 用户配置
        </div>
        <div class="nav-item" data-page="github-plugins">
            <img src="/screenshots/下载插件.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 下载插件
        </div>
        <div class="nav-item" data-page="persona" id="nav-persona" style="display:none;">
            <img src="/screenshots/AI人设.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> AI人设
        </div>
        <div class="nav-item" data-page="help-modules" id="nav-help-modules" style="display:none;">
            <img src="/screenshots/帮助模块.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 帮助模块
        </div>
        <div class="nav-item" data-page="help-page">
            <img src="/screenshots/使用帮助.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 使用帮助
        </div>
        <div class="nav-item" data-page="store">
            <img src="/screenshots/插件商店.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 插件商店
        </div>
        <div class="nav-item" data-page="about">
            <img src="/screenshots/关于.png" class="nav-icon-img" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="nav-icon" style="display:none"></span> 关于
        </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main">
        <!-- 仪表盘 -->
        <div class="page active" id="page-dashboard">
            <div class="page-header flex-between">
                <div>
                    <h2> 仪表盘</h2>
                    <p>系统状态总览</p>
                </div>
                <div style="display:flex;gap:6px;">
                    <button class="btn" onclick="refreshAll()" title="刷新数据" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
                    <button class="btn" onclick="restartBot()" title="重启机器人" style="color:var(--danger);border-color:var(--danger);">⏻ 重启</button>
                </div>
            </div>
            <div class="stat-grid" id="stat-grid">
                <div class="stat-card"><div class="stat-card-header"><span class="stat-card-title">加载中...</span></div></div>
            </div>
            <div class="card" style="margin-bottom:20px;">
                <div class="card-header flex-between">
                    <h3 data-random-icon="1">管理员</h3>
                    <span style="font-size:12px;color:var(--text-muted);">仅管理员可使用 Web UI 指令</span>
                </div>
                <div class="card-body" style="padding:12px 16px;">
                    <div style="display:flex;gap:8px;margin-bottom:8px;">
                        <input type="text" id="admin-qq-input" placeholder="输入 QQ 号" style="background:var(--bg-primary);border:1px solid var(--border);color:var(--text-primary);padding:5px 10px;border-radius:6px;font-size:13px;width:160px;">
                        <button class="btn btn-sm btn-primary" onclick="addAdmin()" data-random-icon="1" data-icon-class="ui-action-icon">添加</button>
                    </div>
                    <div id="admin-list" style="display:flex;flex-wrap:wrap;gap:6px;">
                        <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                    </div>
                </div>
            </div>
            <!-- Token 用量统计 -->
            <div class="card" style="margin-bottom:20px;display:none;" id="token-card">
                <div class="card-header flex-between">
                    <h3 data-random-icon="1">Token 用量统计</h3>
                    <span style="font-size:12px;color:var(--text-muted);">近 14 天</span>
                </div>
                <div class="card-body" style="padding:16px;">
                    <!-- 统计卡片 -->
                    <div class="stat-grid" style="grid-template-columns:repeat(6,1fr);margin-bottom:16px;" id="token-summary-cards">
                        <div class="stat-card"><div class="stat-card-title" data-random-icon="1">累计 Token</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title" data-random-icon="1">今日 Token</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title" data-random-icon="1">累计调用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title" data-random-icon="1">今日调用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title" data-random-icon="1">累计费用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                        <div class="stat-card"><div class="stat-card-title" data-random-icon="1">今日费用</div><div class="stat-card-value" style="font-size:20px;">--</div></div>
                    </div>
                    <!-- 柱状图 -->
                    <div id="token-chart" style="display:flex;align-items:flex-end;gap:6px;height:160px;padding:0 4px;position:relative;overflow-x:auto;">
                        <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                    </div>
                    <!-- 图例 -->
                    <div style="display:flex;gap:20px;margin-top:8px;justify-content:center;font-size:12px;">
                        <span><i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#60a5fa;margin-right:5px;vertical-align:-1px;"></i>输入 Token</span>
                        <span><i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#fb923c;margin-right:5px;vertical-align:-1px;"></i>输出 Token</span>
                        <span style="color:var(--success);">×N 调用次数</span>
                    </div>
                </div>
            </div>
            <div class="card" style="margin-bottom:20px;">
                <div class="card-header flex-between">
                    <h3 data-random-icon="1">指令使用统计</h3>
                    <span style="font-size:12px;color:var(--text-muted);" id="cmd-stats-total">--</span>
                </div>
                <div class="card-body" id="cmd-stats-table">
                    <div style="padding:20px;text-align:center;color:var(--text-muted);">加载中...</div>
                </div>
            </div>
            <div class="card">
                <div class="card-header"><h3 data-random-icon="1">系统信息</h3></div>
                <div class="card-body" id="sysinfo-table"></div>
            </div>
        </div>

        <!-- 插件管理 -->
        <div class="page" id="page-plugins">
            <div class="page-header flex-between">
                <div>
                    <h2> 插件管理</h2>
                    <p>查看已加载插件信息</p>
                </div>
                <div style="display:flex;gap:6px;">
                    <button class="btn btn-sm" onclick="toggleAllPlugins(true)" title="启用所有已禁用的插件">▶ 一键启用</button>
                    <button class="btn btn-sm" onclick="toggleAllPlugins(false)" title="禁用所有已启用的插件" style="color:var(--danger);">⏸ 一键禁用</button>
                    <button class="btn" onclick="loadPlugins()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
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
                    <h2>Bot 连接</h2>
                    <p>查看已连接的机器人实例</p>
                </div>
                <button class="btn" onclick="loadBots()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
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
                    <h2>实时日志</h2>
                    <p>最近 200 条系统日志（每 3 秒自动刷新）</p>
                </div>
                <div style="display:flex;gap:8px;">
                    <button class="btn btn-sm" onclick="toggleAutoRefresh()" id="btn-auto-refresh">⏸ 暂停</button>
                    <button class="btn btn-sm" onclick="clearLogs()">🗑 清屏</button>
                    <button class="btn btn-sm" onclick="loadLogs()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
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
                    <h2> 指令列表</h2>
                    <p>自动扫描所有本地插件，按类型分类展示全部指令触发词</p>
                </div>
                <button class="btn" onclick="loadCommands()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3 data-random-icon="1">on_command（指令）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_command">--</span></div>
                <div class="card-body" id="cmd-table-on_command"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3 data-random-icon="1">on_fullmatch（全匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_fullmatch">--</span></div>
                <div class="card-body" id="cmd-table-on_fullmatch"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3 data-random-icon="1">on_alconna（Alconna）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_alconna">--</span></div>
                <div class="card-body" id="cmd-table-on_alconna"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3 data-random-icon="1">on_startswith（前缀匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_startswith">--</span></div>
                <div class="card-body" id="cmd-table-on_startswith"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3 data-random-icon="1">on_regex（正则匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_regex">--</span></div>
                <div class="card-body" id="cmd-table-on_regex"></div>
            </div>
            <div class="card" style="margin-bottom:16px;">
                <div class="card-header"><h3 data-random-icon="1">on_endswith（后缀匹配）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_endswith">--</span></div>
                <div class="card-body" id="cmd-table-on_endswith"></div>
            </div>
            <div class="card">
                <div class="card-header"><h3 data-random-icon="1">on_message（消息触发）</h3><span style="font-size:12px;color:var(--text-muted);" id="cmd-count-on_message">--</span></div>
                <div class="card-body" id="cmd-table-on_message"></div>
            </div>
        </div>

        <!-- 插件商店 -->
        <div class="page" id="page-store">
            <div class="page-header flex-between">
                <div>
                    <h2> 插件商店</h2>
                    <p>浏览并安装 NoneBot 插件商店的插件（数据来源：registry.nonebot.dev）</p>
                </div>
                <div style="display:flex;gap:8px;">
                    <input type="text" id="store-search" placeholder="搜索插件..." style="background:var(--bg-primary);border:1px solid var(--border);color:var(--text-primary);padding:6px 12px;border-radius:6px;font-size:13px;width:180px;" oninput="searchStore()">
                    <button class="btn btn-sm" onclick="loadStore()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
                </div>
            </div>
            <div id="store-status" style="margin-bottom:12px;font-size:13px;color:var(--text-muted);">加载中...</div>
            <div id="store-list"></div>
        </div>

        <!-- GitHub 插件下载 -->
        <div class="page" id="page-github-plugins">
            <div class="page-header flex-between">
                <div>
                    <h2> 下载插件</h2>
                    <p>从 GitHub 仓库安装/更新 NoneBot 插件（来源：github.com/sangonomiya249）</p>
                </div>
                <div style="display:flex;gap:8px;">
                    <input type="text" id="github-plugins-search" placeholder="搜索插件..." style="background:var(--bg-primary);border:1px solid var(--border);color:var(--text-primary);padding:6px 12px;border-radius:6px;font-size:13px;width:180px;" oninput="searchGithubPlugins()">
                    <button class="btn btn-sm" onclick="loadGithubPlugins()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
                </div>
            </div>
            <div id="github-plugins-status" style="margin-bottom:12px;font-size:13px;color:var(--text-muted);">加载中...</div>
            <div id="github-plugins-list"></div>
        </div>

        <!-- Bot 用户信息 -->
        <div class="page" id="page-bot-info">
            <div class="page-header flex-between">
                <div>
                    <h2> 用户配置</h2>
                    <p>Bot 账号信息总览</p>
                </div>
                <button class="btn" onclick="loadBotInfo()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
            </div>
            <div id="bot-info-content" style="display:flex;gap:24px;flex-wrap:wrap;">
                <div class="stat-card" style="flex:1;min-width:280px;text-align:center;">
                    <img id="bot-avatar" src="" style="width:100px;height:100px;border-radius:50%;margin-bottom:12px;background:var(--bg-primary);" onerror="this.style.display='none'">
                    <div style="font-size:20px;font-weight:700;" id="bot-nickname">--</div>
                    <div style="font-size:13px;color:var(--text-muted);" id="bot-qq">QQ: --</div>
                </div>
                <div style="flex:2;min-width:300px;display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                    <div class="stat-card" style="cursor:pointer;" onclick="showDetailModal('friends')">
                        <div class="stat-card-title" data-random-icon="1">好友数量（点击查看）</div>
                        <div class="stat-card-value" id="bot-friends">--</div>
                    </div>
                    <div class="stat-card" style="cursor:pointer;" onclick="showDetailModal('groups')">
                        <div class="stat-card-title" data-random-icon="1">群聊数量（点击查看）</div>
                        <div class="stat-card-value" id="bot-groups">--</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-title" data-random-icon="1">接收消息</div>
                        <div class="stat-card-value" id="bot-msg-recv">--</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-title" data-random-icon="1">发送消息</div>
                        <div class="stat-card-value" id="bot-msg-sent">--</div>
                    </div>
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <div class="card-header"><h3 data-random-icon="1">私聊排行 Top 10</h3></div>
                <div class="card-body" style="padding:12px 16px;" id="top-users-list">
                    <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                </div>
            </div>
        </div>

        <!-- AI人设管理 -->
        <div class="page" id="page-persona">
            <div class="page-header flex-between">
                <div>
                    <h2> AI人设管理</h2>
                    <p>管理对话机器人的人设提示词（persona_prompts.json）</p>
                </div>
                <div style="display:flex;gap:6px;">
                    <button class="btn" onclick="loadPersona()" title="重新加载" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
                    <button class="btn btn-primary" onclick="savePersona()" title="保存修改" data-random-icon="1" data-icon-class="ui-action-icon">保存</button>
                </div>
            </div>
            <!-- 栏目切换 Tab -->
            <div style="display:flex;gap:8px;margin-bottom:16px;border-bottom:2px solid var(--border);padding-bottom:0;align-items:flex-end;justify-content:space-between;">
                <div style="display:flex;gap:8px;">
                    <button class="persona-tab active" onclick="switchPersonaTab('public')" id="tab-public">
                        <span data-random-icon="1">公开人设 (persona_catalog)</span>
                    </button>
                    <button class="persona-tab" onclick="switchPersonaTab('hidden')" id="tab-hidden">
                        <span data-random-icon="1">隐藏人设 (hidden_persona_catalog)</span>
                    </button>
                </div>
                <div style="display:flex;gap:6px;padding-bottom:8px;">
                    <button class="btn btn-sm btn-primary" onclick="showCreatePersonaModal('public')" id="btn-create-public" data-random-icon="1" data-icon-class="ui-action-icon">新建公开人设</button>
                    <button class="btn btn-sm" onclick="showCreatePersonaModal('hidden')" id="btn-create-hidden" style="display:none;" data-random-icon="1" data-icon-class="ui-action-icon">新建隐藏人设</button>
                </div>
            </div>
            <!-- 人设编辑区域 -->
            <div id="persona-editor" style="display:flex;flex-direction:column;gap:16px;">
                <span style="color:var(--text-muted);font-size:13px;">加载中...</span>
            </div>
            <!-- 隐藏人设白名单区域 -->
            <div id="persona-whitelist-section" style="display:none;margin-top:24px;">
                <div class="card">
                    <div class="card-header"><h3 data-random-icon="1">隐藏人设专属白名单</h3></div>
                    <div class="card-body" style="padding:12px 16px;" id="persona-whitelist-editor">
                        <span style="color:var(--text-muted);font-size:12px;">加载中...</span>
                    </div>
                </div>
            </div>
            <!-- 新建人设弹窗 -->
            <div id="create-persona-overlay" class="config-overlay" style="display:none;" onclick="if(event.target===this)closeCreatePersonaModal()">
                <div class="config-modal" style="max-width:600px;">
                    <div class="config-modal-header">
                        <h3 id="create-persona-title" data-random-icon="1">新建人设</h3>
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
                        <button class="btn btn-primary" onclick="confirmCreatePersona()" data-random-icon="1" data-icon-class="ui-action-icon">确认创建</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 使用帮助 -->
        <!-- 帮助模块管理  —— 渲染风格对照 /帮助 图片 -->
        <div class="page" id="page-help-modules">
            <div class="page-header flex-between">
                <div>
                    <h2> 帮助模块管理</h2>
                    <p>管理 /帮助 命令中各功能模块。修改后点击「保存」即可生效。</p>
                </div>
                <div style="display:flex;gap:12px;align-items:center;">
                    <span style="font-size:12px;color:var(--text-muted);">显示模式:</span>
                    <select id="help-display-mode" onchange="saveDisplayMode()" style="background:var(--bg-card);border:1px solid var(--border);color:var(--text-primary);padding:4px 8px;border-radius:6px;font-size:12px;">
                        <option value="auto">自动分类</option>
                        <option value="flat">单插件模式</option>
                    </select>
                    <button class="btn btn-primary" onclick="saveAllHelp()" style="background:var(--success);" data-random-icon="1" data-icon-class="ui-action-icon">一键保存全部</button>
                    <button class="btn" onclick="loadHelpModules()" data-random-icon="1" data-icon-class="ui-action-icon">刷新</button>
                </div>
            </div>
            <!-- 帮助图全局设置：大标题 / 副标题 -->
            <div class="card" style="margin-bottom:20px;padding:12px 18px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
                <span style="font-size:14px;font-weight:700;white-space:nowrap;" data-random-icon="1">帮助图标题</span>
                <input id="help-page-title" placeholder="大标题（默认: 钰袖Help）" style="flex:1;min-width:180px;font-size:14px;border:1px solid var(--border);background:var(--bg-card);color:var(--text-primary);border-radius:6px;padding:6px 10px;" onchange="savePageMeta()">
                <input id="help-page-subtitle" placeholder="副标题（默认: 输入 /帮助 关键词 可筛选具体功能）" style="flex:2;min-width:250px;font-size:13px;border:1px solid var(--border);background:var(--bg-card);color:var(--text-primary);border-radius:6px;padding:6px 10px;" onchange="savePageMeta()">
                <img id="help-bg-preview" src="/help-data/background.png" onerror="this.style.display='none'" style="height:50px;border-radius:6px;border:1px solid var(--border);cursor:pointer;display:none;" onclick="window.open(this.src)" title="当前背景图预览（点击放大）">
            </div>
            <div id="help-modules-status" style="margin-bottom:16px;font-size:13px;color:var(--text-muted);">加载中...</div>
            <div id="help-modules-container"></div>
        </div>

        <div class="page" id="page-help-page">
            <div class="page-header">
                <h2> 使用帮助</h2>
                <p>Web UI 管理面板功能说明</p>
            </div>
            <div class="stat-grid" style="margin-bottom:20px;">
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/仪表盘.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 仪表盘</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看 CPU/内存/磁盘/运行时间<br>消息收发统计<br>指令使用排行（今日+历史）</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/插件管理.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 插件管理</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看所有插件及加载状态<br>启用/禁用插件（重启生效）<br>编辑插件配置（常量+JSON）<br>修改指令触发词<br>安装/卸载插件（插件商店）<br>一键启用/禁用全部插件</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/Bot连接.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> Bot 连接</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看在线 Bot 实例<br>显示 Bot ID / 昵称 / 适配器<br>快速确认连接状态</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/实时日志.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 实时日志</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看最近 200 条系统日志<br>3 秒自动刷新<br>等级颜色区分</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/指令列表.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 指令列表</div>
                    <div class="stat-card-sub" style="line-height:1.8;">自动扫描所有插件的指令<br>按类型分类展示<br>支持 on_command / fullmatch / alconna / startswith 等</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/用户配置.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 用户配置</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看 Bot QQ 号/头像<br>好友列表（可删除好友）<br>群聊列表（可退出群聊）</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/下载插件.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 下载插件</div>
                    <div class="stat-card-sub" style="line-height:1.8;">从 GitHub 仓库安装/更新插件<br>支持搜索插件<br>适合维护个人插件源</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/AI人设.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> AI 人设</div>
                    <div class="stat-card-sub" style="line-height:1.8;">管理公开/隐藏人设<br>编辑名称、描述和系统提示词<br>配置隐藏人设白名单</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/帮助模块.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 帮助模块</div>
                    <div class="stat-card-sub" style="line-height:1.8;">管理 /帮助 图片模块<br>调整分类、排序和显示名称<br>编辑触发词说明并保存生效</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/插件商店.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 插件商店</div>
                    <div class="stat-card-sub" style="line-height:1.8;">浏览 NoneBot 注册表插件<br>搜索 + 一键安装<br>安装后自动写入 pyproject.toml</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title"><img src="/screenshots/关于.png" class="help-title-icon" onerror="this.style.display='none';this.nextElementSibling.style.display='none'" alt=""><span class="help-title-fallback"></span> 关于</div>
                    <div class="stat-card-sub" style="line-height:1.8;">查看 Web UI 基础信息<br>确认框架、适配器和接口<br>快速定位常用 API</div>
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <div class="card-header"><h3 data-random-icon="1">快捷指令</h3></div>
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
                <h2> 关于</h2>
                <p>关于 LiuYing & Web UI 管理面板</p>
            </div>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title" data-random-icon="1">机器人框架</span></div>
                    <div style="font-size:18px;font-weight:600;">NoneBot v2</div>
                    <div class="stat-card-sub">异步 Python 机器人框架</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title" data-random-icon="1">适配器</span></div>
                    <div style="font-size:18px;font-weight:600;">OneBot V11</div>
                    <div class="stat-card-sub">go-cqhttp / LLOneBot</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title" data-random-icon="1">Web 框架</span></div>
                    <div style="font-size:18px;font-weight:600;">FastAPI</div>
                    <div class="stat-card-sub">高性能异步 Web 框架</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header"><span class="stat-card-title" data-random-icon="1">作者</span></div>
                    <div style="font-size:18px;font-weight:600;">lhc</div>
                    <div class="stat-card-sub">2491434931@qq.com</div>
                </div>
            </div>
            <div class="card" style="margin-top:20px;">
                <div class="card-header"><h3 data-random-icon="1">API 接口列表</h3></div>
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
                    <button class="btn btn-primary" id="btn-save-config" onclick="saveConfig()" data-random-icon="1" data-icon-class="ui-action-icon">保存配置</button>
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
        const _randomIconPool = Array.from({length: 23}, (_, i) => i + 1).sort(() => Math.random() - 0.5);
        let _randomIconCursor = 0;
        function randomIconSrc() {
            if (_randomIconCursor >= _randomIconPool.length) {
                _randomIconPool.sort(() => Math.random() - 0.5);
                _randomIconCursor = 0;
            }
            return '/screenshots/' + _randomIconPool[_randomIconCursor++] + '.png';
        }
        function randomIconHtml(cls = 'inline-random-icon') {
            return '<img src="' + randomIconSrc() + '" class="' + cls + '" alt="">';
        }
        function iconImgHtml(cls = 'ui-action-icon') {
            return '<img src="' + randomIconSrc() + '" class="' + cls + '" alt="">';
        }
        function randomStatIconHtml() {
            return '<span class="stat-card-icon random-art-icon">' + randomIconHtml() + '</span>';
        }
        function replaceBuiltinEmojiIcons(root = document) {
            root.querySelectorAll('[data-random-icon]').forEach(function(el) {
                if (el.dataset.iconReady === '1') return;
                const img = document.createElement('img');
                img.src = randomIconSrc();
                img.className = el.dataset.iconClass || 'title-random-icon';
                img.alt = '';
                img.onerror = function() { this.remove(); };
                el.prepend(img);
                el.dataset.iconReady = '1';
            });
        }
        function decorateActionIcons(root = document) {
            const keep = ['⏸', '▶', '⏻', '⚙', '🗑', '✕', '▲', '▼', '↺', '×', '✓', '✗'];
            const pattern = /^([\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]\uFE0F?)\s*/u;
            root.querySelectorAll('button, .badge, .whitelist-tag, .card-header h3, .stat-card-title, span').forEach(function(el) {
                if (el.dataset.actionIconReady === '1') return;
                const text = el.textContent || '';
                const match = text.match(pattern);
                if (!match || keep.includes(match[1])) return;
                if (el.closest('.nav-item') || el.classList.contains('help-title-fallback')) return;
                el.innerHTML = iconImgHtml() + el.innerHTML.replace(match[0], '');
                el.dataset.actionIconReady = '1';
            });
        }

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
            replaceBuiltinEmojiIcons(document);
            decorateActionIcons(document);
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
                else if (page === 'help-modules') { loadHelpModules(); stopAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'bot-info') { loadBotInfo(); stopAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'persona') {
                    if (!_aichatAvailable) {
                        document.getElementById('page-persona').innerHTML = '<div style="text-align:center;padding:60px;color:var(--text-muted);"><h3>' + randomIconHtml('title-random-icon') + '未检测到 AI 对话插件</h3><p style="margin-top:12px;">需要安装 nonebot_plugin_aichat_baize 才能使用 AI 人设管理功能</p></div>';
                    } else {
                        loadPersona();
                    }
                    stopAutoRefresh(); stopTokenRefresh();
                }
                else if (page === 'help-page') { stopAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'store') { loadStore(); stopAutoRefresh(); stopTokenRefresh(); }
                else if (page === 'github-plugins') { loadGithubPlugins(); stopAutoRefresh(); stopTokenRefresh(); }
                else { stopAutoRefresh(); stopTokenRefresh(); }
            });
        });

        async function restartBot() {
            if (!confirm('确定要重启机器人吗？\n\nBot 进程将退出并由进程管理器自动拉起。')) return;
            showToast('处理中：Bot 即将重启...', 'info');
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
                showToast('错误：请求失败: ' + e.message, 'error');
                return null;
            }
        }
        async function getApi(path) {
            const r = await api(path);
            return r;
        }
        async function putApi(path, body) {
            const token = getToken();
            const headers = {'Content-Type': 'application/json'};
            if (token) headers['Authorization'] = 'Bearer ' + token;
            try {
                const res = await fetch(path, {method: 'PUT', headers, body: JSON.stringify(body)});
                if (res.status === 401) { sessionStorage.removeItem('lhc_token'); location.reload(); return null; }
                const data = await res.json();
                return {ok: res.ok, ...data};
            } catch (e) {
                showToast('错误：请求失败: ' + e.message, 'error');
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
            // 检测帮助模块是否可用
            document.getElementById('nav-help-modules').style.display = (data.help_available === true) ? '' : 'none';
            if (_aichatAvailable) {
                loadTokenStats();
            } else {
                document.getElementById('token-summary-cards').innerHTML =
                    '<div class="stat-card" style="grid-column:1/-1;"><div class="stat-card-title" style="color:var(--text-muted);">' + randomIconHtml('title-random-icon') + '未检测到 AI 对话插件 (nonebot_plugin_aichat_baize)，Token 统计不可用</div></div>';
                document.getElementById('token-chart').innerHTML = '';
            }
            decorateActionIcons(document);
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
                        ${randomStatIconHtml()}
                    </div>
                    <div class="stat-card-value">${cpuPct.toFixed(1)}<span style="font-size:16px;color:var(--text-secondary)">%</span></div>
                    <div class="progress-bar"><div class="progress-fill ${cpuColor}" style="width:${cpuPct}%"></div></div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">内存使用率</span>
                        ${randomStatIconHtml()}
                    </div>
                    <div class="stat-card-value">${memPct.toFixed(1)}<span style="font-size:16px;color:var(--text-secondary)">%</span></div>
                    <div class="progress-bar"><div class="progress-fill ${memColor}" style="width:${memPct}%"></div></div>
                    <div class="stat-card-sub">已用 ${formatBytes(data.memory_used || 0)} / 总计 ${formatBytes(data.memory_total || 0)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">运行时间</span>
                        ${randomStatIconHtml()}
                    </div>
                    <div class="stat-card-value" style="font-size:22px;">${uptime}</div>
                    <div class="stat-card-sub">自 ${data.start_time || '--'} 起</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-header">
                        <span class="stat-card-title">消息统计</span>
                        ${randomStatIconHtml()}
                    </div>
                    <div style="display:flex;gap:24px;margin-top:4px;">
                        <div><div style="font-size:22px;font-weight:700;">${(data.recv_msg_count || 0).toLocaleString()}</div><div style="font-size:11px;color:var(--text-muted);">接收</div></div>
                        <div><div style="font-size:22px;font-weight:700;">${(data.send_msg_count || 0).toLocaleString()}</div><div style="font-size:11px;color:var(--text-muted);">发送</div></div>
                    </div>
                </div>
            `;
            decorateActionIcons(grid);
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
                    ${iconImgHtml()}${esc(qq)}
                    <span style="cursor:pointer;opacity:0.7;" onclick="removeAdmin('${esc(qq)}')" title="移除">✕</span>
                </span>`).join('');
            decorateActionIcons(container);
        }

        async function addAdmin() {
            const inp = document.getElementById('admin-qq-input');
            const qq = inp.value.trim();
            if (!qq) { showToast('请输入 QQ 号', 'error'); return; }
            const data = await postApi('/api/admins/add', {qq: qq});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                inp.value = '';
                loadAdmins();
            } else {
                showToast('错误：' + ((data && data.error) || '添加失败'), 'error');
            }
        }

        async function removeAdmin(qq) {
            if (!confirm('确定移除管理员 ' + qq + ' 吗？')) return;
            const data = await postApi('/api/admins/remove', {qq: qq});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                loadAdmins();
            } else {
                showToast('错误：' + ((data && data.error) || '移除失败'), 'error');
            }
        }

        // ====== 指令统计 ======
        async function loadCmdStats() {
            const data = await api('/api/cmd-stats');
            if (!data) return;

            document.getElementById('cmd-stats-total').innerHTML =
                iconImgHtml() + '今日 ' + (data.today || 0) + ' 次 · ' + iconImgHtml() + '累计 ' + (data.total || 0) + ' 次';

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
                '<div style="font-size:12px;font-weight:600;color:var(--text-secondary);margin-bottom:4px;">' + iconImgHtml() + '今日排行</div>' +
                '<table ' + tblStyle + ' style="margin-bottom:12px;">' + tblHead + '<tbody>' + todayRows + '</tbody></table>' +
                '<div style="font-size:12px;font-weight:600;color:var(--text-secondary);margin-bottom:4px;">' + iconImgHtml() + '历史排行</div>' +
                '<table ' + tblStyle + '>' + tblHead + '<tbody>' + allRows + '</tbody></table>';
            decorateActionIcons(document.getElementById('cmd-stats-table'));
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
                        <div style="width:50%;background:rgba(39,185,159,0.48);border-radius:0 0 3px 3px;height:${inputH}px;min-height:${d.input > 0 ? 2 : 0}px;" title="输入: ${formatNumber(d.input)}"></div>
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
                {key: 'on_command', title: 'on_command', prefix: '/'},
                {key: 'on_fullmatch', title: 'on_fullmatch', prefix: ''},
                {key: 'on_alconna', title: 'on_alconna', prefix: ''},
                {key: 'on_startswith', title: 'on_startswith', prefix: ''},
                {key: 'on_regex', title: 'on_regex', prefix: ''},
                {key: 'on_endswith', title: 'on_endswith', prefix: ''},
                {key: 'on_message', title: 'on_message', prefix: ''},
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
            const titles = {friends: '好友列表', groups: '群聊列表'};
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
                        <button class="btn btn-sm" style="color:var(--danger);" onclick="leaveGroup('${esc(g.id)}', this)" title="退出群聊">${iconImgHtml()}</button>
                    </div>`).join('');
            }
        }

        async function deleteFriend(qq, btn) {
            if (!confirm('确定要删除好友 ' + qq + ' 吗？')) return;
            btn.innerHTML = iconImgHtml(); btn.disabled = true;
            const data = await postApi('/api/bot-info/friends/delete', {qq: qq});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                showDetailModal('friends');
            } else {
                showToast('错误：' + ((data && data.error) || '删除失败'), 'error');
                btn.textContent = '🗑'; btn.disabled = false;
            }
        }

        async function leaveGroup(gid, btn) {
            if (!confirm('确定要退出群聊 ' + gid + ' 吗？')) return;
            btn.innerHTML = iconImgHtml(); btn.disabled = true;
            const data = await postApi('/api/bot-info/groups/leave', {group_id: gid});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                showDetailModal('groups');
            } else {
                showToast('错误：' + ((data && data.error) || '退群失败'), 'error');
                btn.innerHTML = iconImgHtml(); btn.disabled = false;
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
                    : '<button class="btn btn-sm btn-primary" onclick="installStorePlugin(\'' + esc(p.project_link || p.module_name) + '\', this)">' + iconImgHtml() + '安装</button>';
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
            decorateActionIcons(document.getElementById('store-list'));
        }

        function searchStore() {
            clearTimeout(window._storeTimer);
            window._storeTimer = setTimeout(() => loadStore(), 400);
        }

        async function installStorePlugin(project, btn) {
            if (!confirm('确定要安装插件「' + project + '」吗？\n\n安装后需在 pyproject.toml 中添加并重启 Bot。')) return;
            btn.innerHTML = iconImgHtml() + '安装中...';
            btn.disabled = true;
            const data = await postApi('/api/store/install', {project: project});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                loadStore();
            } else {
                showToast('错误：' + ((data && data.error) || '安装失败'), 'error');
                btn.innerHTML = iconImgHtml() + '安装';
                btn.disabled = false;
            }
        }

        async function uninstallStorePlugin(module, btn) {
            if (!confirm('确定要卸载插件「' + module + '」吗？\n\n将执行 pip uninstall 并从 pyproject.toml 移除。')) return;
            btn.innerHTML = iconImgHtml() + '卸载中...';
            btn.disabled = true;
            const data = await postApi('/api/plugins/uninstall', {module: module});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                loadStore();
            } else {
                showToast('错误：' + ((data && data.error) || '卸载失败'), 'error');
                btn.textContent = '🗑 卸载';
                btn.disabled = false;
            }
        }

        // ====== GitHub 插件下载 ======
        async function loadGithubPlugins() {
            document.getElementById('github-plugins-status').textContent = '加载中...';
            document.getElementById('github-plugins-list').innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted);">加载中...</div>';

            const search = document.getElementById('github-plugins-search').value;
            const url = '/api/github-plugins' + (search ? '?search=' + encodeURIComponent(search) : '');
            const data = await api(url);
            if (!data) return;

            document.getElementById('github-plugins-status').textContent = '共 ' + data.total + ' 个插件' + (search ? '（搜索: ' + esc(search) + '）' : '');

            if (!data.plugins || !data.plugins.length) {
                document.getElementById('github-plugins-list').innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted);">没有找到匹配的插件</div>';
                return;
            }

            document.getElementById('github-plugins-list').innerHTML = data.plugins.map(p => {
                const installed = p.installed ? '<span class="badge badge-info" style="font-size:10px;">✓ 已安装</span> ' : '';
                const starsHtml = p.stars ? '<span style="color:#e2b714;margin-right:8px;">' + iconImgHtml() + p.stars + '</span>' : '';
                const langHtml = p.language ? '<span style="background:var(--bg-primary);padding:1px 6px;border-radius:4px;font-size:10px;margin-right:4px;">' + esc(p.language) + '</span>' : '';
                const timeHtml = p.updated_at ? '<span style="color:var(--text-muted);font-size:10px;">' + esc(p.updated_at.slice(0, 10)) + '</span>' : '';
                const topicsHtml = (p.topics && p.topics.length) ? '<span style="margin-left:4px;">' + p.topics.map(t => '<span style="background:var(--bg-hover);padding:1px 6px;border-radius:4px;font-size:10px;margin:1px;">' + esc(t) + '</span>').join('') + '</span>' : '';
                const actionBtn = p.installed
                    ? '<button class="btn btn-sm btn-primary" onclick="installGithubPlugin(\'' + esc(p.name) + '\', \'' + esc(p.default_branch || 'main') + '\', this)">' + iconImgHtml() + '更新</button>'
                    : '<button class="btn btn-sm btn-primary" onclick="installGithubPlugin(\'' + esc(p.name) + '\', \'' + esc(p.default_branch || 'main') + '\', this)">' + iconImgHtml() + '安装</button>';
                return '<div class="stat-card" style="padding:14px 18px;">' +
                    '<div style="display:flex;justify-content:space-between;align-items:flex-start;">' +
                    '<div style="flex:1;">' +
                    '<div style="font-size:14px;font-weight:600;">' + installed + esc(p.name) + '</div>' +
                    '<div style="font-size:12px;color:var(--text-secondary);margin:4px 0;">' + esc(p.description || '暂无描述') + '</div>' +
                    '<div style="margin-top:4px;font-size:11px;">' + starsHtml + langHtml + timeHtml + topicsHtml + '</div>' +
                    '</div>' +
                    '<div style="margin-left:12px;">' + actionBtn + '</div>' +
                    '</div></div>';
            }).join('');
            decorateActionIcons(document.getElementById('github-plugins-list'));
        }

        function searchGithubPlugins() {
            clearTimeout(window._githubPluginsTimer);
            window._githubPluginsTimer = setTimeout(() => loadGithubPlugins(), 400);
        }

        async function installGithubPlugin(repoName, branch, btn) {
            const action = btn.textContent.includes('更新') ? '更新' : '安装';
            if (!confirm('确定要' + action + '插件「' + repoName + '」吗？\n\n将通过 pip install git+https 安装到 plugins 目录。')) return;
            btn.innerHTML = iconImgHtml() + action + '中...';
            btn.disabled = true;
            const data = await postApi('/api/github-plugins/install', {repo_name: repoName, branch: branch});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                loadGithubPlugins();
            } else {
                showToast('错误：' + ((data && data.error) || action + '失败'), 'error');
                btn.innerHTML = iconImgHtml() + (action === '更新' ? '更新' : '安装');
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
                const statusBadge = isExternal ? '<span class="badge badge-info">' + iconImgHtml() + '外部</span>'
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
            decorateActionIcons(document.getElementById('plugin-table'));
        }

        async function uninstallPlugin(module, isExternal) {
            const warn = isExternal
                ? '确定要卸载 pip 插件「' + module + '」吗？\n\n这将执行 pip uninstall 并从 pyproject.toml 移除。'
                : '确定要删除插件「' + module + '」吗？\n\n这将永久删除插件文件，不可恢复！';
            if (!confirm(warn)) return;
            const data = await postApi('/api/plugins/uninstall', {module: module});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                setTimeout(() => loadPlugins(), 300);
            } else {
                showToast('错误：' + ((data && data.error) || '卸载失败'), 'error');
            }
        }

        async function toggleAllPlugins(enable) {
            const action = enable ? '启用' : '禁用';
            if (!confirm('确定要一键' + action + '所有本地插件吗？\n\n这将' + action + ' src/plugins/ 下的所有插件并触发热重载。')) return;
            const data = await postApi('/api/plugins/toggle-all', {enabled: enable});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                setTimeout(() => loadPlugins(), 500);
            } else {
                showToast('错误：' + ((data && data.error) || '操作失败'), 'error');
            }
        }

        async function togglePlugin(module, enable) {
            const action = enable ? '启用' : '禁用';
            if (!confirm('确定要' + action + '插件「' + module + '」吗？\n\n重启 Bot 后生效。')) return;
            const data = await postApi('/api/plugins/toggle', {module: module, enabled: enable});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                setTimeout(() => loadPlugins(), 300);
            } else {
                showToast('错误：' + ((data && data.error) || '操作失败'), 'error');
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
            decorateActionIcons(document.getElementById('bot-table'));
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
            replaceBuiltinEmojiIcons(document.getElementById('config-modal-body'));
        }

        function renderFormatHelp() {
            return `<details style="margin-top:20px;font-size:12px;color:var(--text-muted);border-top:1px solid var(--border);padding-top:12px;">
                <summary style="cursor:pointer;font-weight:600;color:var(--text-secondary);user-select:none;" data-random-icon="1">支持识别的配置项与指令格式</summary>
                <div style="margin-top:10px;line-height:1.8;">
                    <div style="font-weight:600;color:var(--accent);margin-bottom:4px;" data-random-icon="1">配置常量</div>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">API_KEY = "sk-xxx"</code> &nbsp;模块级大写常量<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">CONFIG = {"KEY": value}</code> &nbsp;字典式配置（支持 _env 包装）<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">config.py</code> &nbsp;dataclass / 构造函数参数<br>

                    <div style="font-weight:600;color:var(--accent);margin-top:10px;margin-bottom:4px;" data-random-icon="1">指令触发词</div>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">cmd = on_command("触发词")</code> &nbsp;标准指令<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">matcher = on_fullmatch("完全匹配")</code> &nbsp;全匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">rule = on_startswith("前缀")</code> &nbsp;前缀匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">rule = on_regex(r"正则")</code> &nbsp;正则匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">rule = on_endswith("后缀")</code> &nbsp;后缀匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">cmd = on_alconna(Alconna("..."))</code> &nbsp;Alconna 匹配<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">("/gif倒放", "action")</code> &nbsp;函数体内嵌命令元组（on_message 手动解析模式）<br>
                    <code style="background:var(--bg-primary);padding:1px 5px;border-radius:3px;">on_command(("词1", "词2"))</code> &nbsp;元组触发词<br>

                    <div style="font-weight:600;color:var(--accent);margin-top:10px;margin-bottom:4px;" data-random-icon="1">JSON 配置文件</div>
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
            return '<div style="font-size:12px;color:var(--text-muted);margin-bottom:8px;font-weight:600;" data-random-icon="1">config.py 配置 (' + esc(configPy.path || '') + ')</div>' +
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
            return '<div style="font-size:12px;color:var(--text-muted);margin-bottom:8px;font-weight:600;" data-random-icon="1">Python 常量</div>' +
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
            return '<div style="font-size:12px;color:var(--text-muted);margin:16px 0 8px;font-weight:600;" data-random-icon="1">JSON 配置文件</div>' +
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
            return '<div style="font-size:12px;color:var(--text-muted);margin:16px 0 8px;font-weight:600;" data-random-icon="1">指令触发词（修改后需重启）</div>' +
                matchers.map(m => {
                    const isInline = m.variable && m.variable.startsWith('_inline:');
                    const displayVar = isInline ? '内嵌命令' : m.variable;
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
            btn.innerHTML = iconImgHtml() + '保存中...';
            btn.disabled = true;

            const data = await postApi('/api/plugins/config', {module: currentConfigModule, changes, json_changes: jsonChanges, matcher_changes: matcherChanges, config_py_changes: configPyChanges});
            if (data && data.ok) {
                showToast('成功：' + data.message, 'success');
                hideConfigEditor();
            } else {
                showToast('错误：' + ((data && data.error) || '未知错误'), 'error');
            }
            btn.innerHTML = iconImgHtml() + '保存配置';
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
                title.textContent = '新建公开人设';
                keyHint.textContent = '— 输入数字ID，如 6';
                keyInput.placeholder = '输入数字ID（如 6）';
            } else {
                title.textContent = '新建隐藏人设';
                keyHint.textContent = '— 输入唯一字符串ID，如 明月定制3';
                keyInput.placeholder = '输入唯一字符串ID（如 明月定制3）';
            }
            title.dataset.iconReady = '0';
            replaceBuiltinEmojiIcons(title.parentElement);
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
                showToast('成功：人设已创建并保存', 'success');
                renderPersonaEditor();
                // 切换到对应 tab
                switchPersonaTab(_createPersonaType);
            } else {
                showToast('错误：创建失败: ' + (result ? result.error : '网络错误'), 'error');
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
            showToast('已标记删除 "#' + key + ' ' + personaName + '"，请点击保存按钮生效', 'info');
        }

        async function savePersona() {
            if (!_personaData) { showToast('没有可保存的数据', 'error'); return; }
            const result = await postApi('/api/persona/save', _personaData);
            if (result && result.ok) {
                showToast('成功：' + (result.message || '人设配置已保存'), 'success');
            } else {
                showToast('错误：保存失败: ' + (result ? result.error : '网络错误'), 'error');
            }
        }

        // ====== 帮助模块管理 ======
        function escHtml(s) { if (!s) return ''; return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
        function escAttr(s) { if (!s) return ''; return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/'/g,'&#39;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

        // 浅色版本：hex → 加白变浅
        function lightenColor(hex, factor) {
            factor = factor || 0.72;
            hex = hex.replace('#', '');
            if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
            var r = Math.min(255, Math.round(parseInt(hex.substr(0,2),16) + (255 - parseInt(hex.substr(0,2),16)) * factor));
            var g = Math.min(255, Math.round(parseInt(hex.substr(2,2),16) + (255 - parseInt(hex.substr(2,2),16)) * factor));
            var b = Math.min(255, Math.round(parseInt(hex.substr(4,2),16) + (255 - parseInt(hex.substr(4,2),16)) * factor));
            return '#' + [r,g,b].map(function(c){ return ('0'+c.toString(16)).slice(-2); }).join('');
        }

        let _helpModulesData = [];

        // 显示模式（全局配置）
        var _displayMode = 'auto';
        async function loadDisplayMode() {
            var result = await getApi('/api/help/config');
            _displayMode = (result && result.display_mode) ? result.display_mode : 'auto';
            var sel = document.getElementById('help-display-mode');
            if (sel) sel.value = _displayMode;
            // 同时加载页面标题/副标题
            var tEl = document.getElementById('help-page-title');
            var sEl = document.getElementById('help-page-subtitle');
            if (tEl) tEl.value = (result && result.page_title) ? result.page_title : '';
            if (sEl) sEl.value = (result && result.page_subtitle) ? result.page_subtitle : '';
            // 检测背景图是否存在并显示预览
            checkBgPreview();
        }

        function checkBgPreview() {
            var img = document.getElementById('help-bg-preview');
            if (!img) return;
            // 尝试加载背景图预览
            img.src = '/help-data/background.png?t=' + Date.now();
            img.onload = function() { img.style.display = ''; };
            img.onerror = function() { img.style.display = 'none'; };
        }
        async function savePageMeta() {
            var tEl = document.getElementById('help-page-title');
            var sEl = document.getElementById('help-page-subtitle');
            await putApi('/api/help/config', {
                display_mode: _displayMode,
                page_title: tEl ? tEl.value.trim() : '',
                page_subtitle: sEl ? sEl.value.trim() : '',
            });
        }
        async function saveDisplayMode() {
            var sel = document.getElementById('help-display-mode');
            if (!sel) return;
            _displayMode = sel.value;
            var tEl = document.getElementById('help-page-title');
            var sEl = document.getElementById('help-page-subtitle');
            await putApi('/api/help/config', {
                display_mode: _displayMode,
                page_title: tEl ? tEl.value.trim() : '',
                page_subtitle: sEl ? sEl.value.trim() : '',
            });
            showToast('显示模式已切换为: ' + (_displayMode === 'flat' ? '单插件模式' : '自动分类'), 'info');
            if (_helpModulesData.length > 0) renderHelpModules();
        }

        async function loadHelpModules() {
            document.getElementById('help-modules-status').textContent = '加载中...';
            loadDisplayMode();
            const result = await getApi('/api/help/modules');
            if (result && result.modules) {
                _helpModulesData = result.modules;
                renderHelpModules();
                var totalPlugins = 0;
                for (var i = 0; i < _helpModulesData.length; i++) totalPlugins += _helpModulesData[i].plugin_count;
                if (_displayMode === 'flat') {
                    document.getElementById('help-modules-status').textContent = '单插件模式: ' + totalPlugins + ' 个插件（修改后点击「保存」生效）';
                } else {
                    document.getElementById('help-modules-status').textContent = '自动分类: ' + _helpModulesData.length + ' 个模块, ' + totalPlugins + ' 个插件（修改后点击「保存模块」生效）';
                }
            } else {
                document.getElementById('help-modules-status').textContent = '加载失败或暂无活跃插件';
            }
        }

        function renderHelpModules() {
            var container = document.getElementById('help-modules-container');
            if (_helpModulesData.length === 0) {
                container.innerHTML = '<div style="text-align:center;padding:60px;color:var(--text-muted);">暂无活跃插件</div>';
                return;
            }
            if (_displayMode === 'flat') {
                container.innerHTML = renderFlatView();
            } else {
                // 自动编号：全部为 0 时按顺序赋值
                var allZero = true;
                for (var i = 0; i < _helpModulesData.length; i++) {
                    if ((_helpModulesData[i].sort_order || 0) !== 0) { allZero = false; break; }
                }
                if (allZero) {
                    for (var i = 0; i < _helpModulesData.length; i++) {
                        _helpModulesData[i].sort_order = i;
                    }
                }
                container.innerHTML = _helpModulesData.map(function(m) {
                    return renderModuleCard(m);
                }).join('');
            }
            replaceBuiltinEmojiIcons(container);
            decorateActionIcons(container);
        }

        function reRenderGroupedView() {
            var container = document.getElementById('help-modules-container');
            container.innerHTML = _helpModulesData.map(function(m) {
                return renderModuleCard(m);
            }).join('');
            replaceBuiltinEmojiIcons(container);
            decorateActionIcons(container);
        }

        function onModuleSortChange(moduleName, newVal) {
            var targetPos = parseInt(newVal) || 0;
            // 找到被移动的模块
            var movedIdx = -1;
            for (var i = 0; i < _helpModulesData.length; i++) {
                if (_helpModulesData[i].name === moduleName) { movedIdx = i; break; }
            }
            if (movedIdx < 0) { reRenderGroupedView(); return; }
            // 取出并插入到目标位置
            var moved = _helpModulesData.splice(movedIdx, 1)[0];
            targetPos = Math.max(0, Math.min(targetPos, _helpModulesData.length));
            _helpModulesData.splice(targetPos, 0, moved);
            // 重新编号
            for (var i = 0; i < _helpModulesData.length; i++) {
                _helpModulesData[i].sort_order = i;
            }
            reRenderGroupedView();
            // 自动保存排序
            autoSaveModuleSort();
        }

        var _autoSaveModTimer = null;
        function autoSaveModuleSort() {
            if (_autoSaveModTimer) clearTimeout(_autoSaveModTimer);
            _autoSaveModTimer = setTimeout(async function() {
                for (var i = 0; i < _helpModulesData.length; i++) {
                    var m = _helpModulesData[i];
                    await putApi('/api/help/modules/' + encodeURIComponent(m.name), {
                        display_name: m.display_name,
                        subtitle: m.subtitle || '',
                        color: m.color,
                        enabled: m.enabled !== false,
                        sort_order: m.sort_order || 0,
                    });
                }
                showToast('模块排序已自动保存', 'info');
            }, 600);
        }

        // ====== 平坦模式：每个插件独立卡片 ======
        function renderFlatView() {
            var html = '';
            // 收集所有插件
            var allPlugins = [];
            for (var i = 0; i < _helpModulesData.length; i++) {
                var mod = _helpModulesData[i];
                for (var j = 0; j < mod.plugins.length; j++) {
                    var p = mod.plugins[j];
                    var order = p.override_sort_order || 0;
                    allPlugins.push({ plugin: p, color: mod.color, moduleName: mod.name, moduleSort: mod.sort_order || 0, sort_order: order });
                }
            }
            // 如果全部为 0，按模块排序 + 名称自动编号
            var allZero = true;
            for (var k = 0; k < allPlugins.length; k++) {
                if (allPlugins[k].sort_order !== 0) { allZero = false; break; }
            }
            if (allZero) {
                allPlugins.sort(function(a, b) { return a.moduleSort - b.moduleSort || a.plugin.display_name.localeCompare(b.plugin.display_name); });
                for (var k = 0; k < allPlugins.length; k++) {
                    allPlugins[k].sort_order = k;
                    allPlugins[k].plugin.override_sort_order = k;
                }
            } else {
                allPlugins.sort(function(a, b) { return a.sort_order - b.sort_order || a.plugin.display_name.localeCompare(b.plugin.display_name); });
            }

            for (var k = 0; k < allPlugins.length; k++) {
                html += renderFlatPluginCard(allPlugins[k]);
            }
            return html;
        }

        function reRenderFlatView() {
            var container = document.getElementById('help-modules-container');
            container.innerHTML = renderFlatView();
            replaceBuiltinEmojiIcons(container);
            decorateActionIcons(container);
        }

        function onFlatColorChange(pluginId, newColor) {
            // 更新本地数据
            for (var i = 0; i < _helpModulesData.length; i++) {
                for (var j = 0; j < _helpModulesData[i].plugins.length; j++) {
                    if (_helpModulesData[i].plugins[j].plugin_id === pluginId) {
                        _helpModulesData[i].plugins[j].override_color = newColor;
                        break;
                    }
                }
            }
            reRenderFlatView();
        }

        function onFlatSortChange(pluginId, newVal) {
            var targetPos = parseInt(newVal) || 0;
            // 收集全部插件（当前顺序）
            var all = [];
            for (var i = 0; i < _helpModulesData.length; i++) {
                var mod = _helpModulesData[i];
                for (var j = 0; j < mod.plugins.length; j++) {
                    all.push({ p: mod.plugins[j], m: mod });
                }
            }
            // 找到被移动的插件
            var movedIdx = -1;
            for (var k = 0; k < all.length; k++) {
                if (all[k].p.plugin_id === pluginId) { movedIdx = k; break; }
            }
            if (movedIdx < 0) { reRenderFlatView(); return; }
            // 从当前位置取出，插入到目标位置
            var moved = all.splice(movedIdx, 1)[0];
            targetPos = Math.max(0, Math.min(targetPos, all.length));
            all.splice(targetPos, 0, moved);
            // 重新编号
            for (var k = 0; k < all.length; k++) {
                all[k].p.override_sort_order = k;
            }
            reRenderFlatView();
            // 自动保存排序（异步，不阻塞 UI）
            autoSaveFlatSort();
        }

        var _autoSaveTimer = null;
        function autoSaveFlatSort() {
            if (_autoSaveTimer) clearTimeout(_autoSaveTimer);
            _autoSaveTimer = setTimeout(async function() {
                var all = [];
                for (var i = 0; i < _helpModulesData.length; i++) {
                    for (var j = 0; j < _helpModulesData[i].plugins.length; j++) {
                        all.push(_helpModulesData[i].plugins[j]);
                    }
                }
                for (var k = 0; k < all.length; k++) {
                    var p = all[k];
                    await putApi('/api/help/plugins/' + encodeURIComponent(p.plugin_id), {
                        display_name: p.display_name,
                        description: p.description,
                        sort_order: p.override_sort_order || 0,
                        triggers: p.trigger_overrides || {},
                        color: p.override_color || '',
                    });
                }
                showToast('排序已自动保存', 'info');
            }, 600);
        }

        function renderFlatPluginCard(item) {
            var p = item.plugin;
            // 插件级颜色优先，否则用模块颜色
            var pluginFg = p.override_color || item.color;
            var fg = pluginFg;
            var bg = lightenColor(fg);
            var html = '';

            html += '<div class="card" style="margin-bottom:20px;overflow:visible;">';
            // 彩色标题栏（仿渲染器的气泡）
            html += '<div style="display:flex;align-items:center;gap:8px;padding:8px 18px;background:' + bg + ';border-radius:10px 10px 0 0;transition:background 0.2s;">';
            html += '<input id="hp-n-' + escAttr(p.plugin_id) + '" value="' + escAttr(p.display_name) + '" style="font-weight:700;font-size:15px;border:none;background:transparent;color:' + fg + ';width:150px;" placeholder="插件名">';
            html += '<input id="hp-d-' + escAttr(p.plugin_id) + '" value="' + escAttr(p.description || '') + '" style="flex:1;font-size:12px;border:none;background:transparent;color:' + fg + ';opacity:0.7;min-width:100px;" placeholder="插件描述">';
            html += '<input type="color" id="hp-cl-' + escAttr(p.plugin_id) + '" value="' + fg + '" style="width:22px;height:22px;border:none;cursor:pointer;border-radius:4px;flex-shrink:0;" oninput="var p=this.parentElement;p.style.background=lightenColor(this.value);var inps=p.querySelectorAll(\'input[type=text],textarea\');for(var i=0;i<inps.length;i++)inps[i].style.color=this.value;" onchange="onFlatColorChange(\'' + escAttr(p.plugin_id) + '\',this.value)" title="插件颜色">';
            html += '<span style="font-size:10px;opacity:0.5;color:' + fg + ';">排序:</span>';
            html += '<span style="display:inline-flex;align-items:center;gap:2px;">';
            html += '<button onclick="event.preventDefault();onFlatSortChange(\'' + escAttr(p.plugin_id) + '\',' + Math.max(0, (p.override_sort_order || 0) - 1) + ')" style="cursor:pointer;background:transparent;border:none;color:' + fg + ';font-size:16px;line-height:1;padding:0 2px;" title="上移">▲</button>';
            html += '<input id="hp-so-' + escAttr(p.plugin_id) + '" type="number" value="' + (p.override_sort_order || 0) + '" style="width:48px;font-size:14px;font-weight:700;border:1px solid ' + fg + ';color:' + fg + ';border-radius:6px;padding:4px 4px;background:transparent;text-align:center;" min="0" step="1" onchange="onFlatSortChange(\'' + escAttr(p.plugin_id) + '\',this.value)">';
            html += '<button onclick="event.preventDefault();onFlatSortChange(\'' + escAttr(p.plugin_id) + '\',' + ((p.override_sort_order || 0) + 1) + ')" style="cursor:pointer;background:transparent;border:none;color:' + fg + ';font-size:16px;line-height:1;padding:0 2px;" title="下移">▼</button>';
            html += '</span>';
            html += '<span style="font-size:10px;opacity:0.5;color:' + fg + ';">' + escHtml(item.moduleName) + '</span>';
            html += '<button class="btn btn-sm" style="margin-left:auto;background:' + fg + ';color:#fff;border:none;padding:4px 12px;font-size:12px;" onclick="saveFlatPlugin(\'' + escAttr(p.plugin_id) + '\')">' + iconImgHtml() + '保存</button>';
            html += '</div>';

            // 命令网格（描述可编辑）
            var cmds = p.commands || [];
            var notes = p.notes || [];
            var trigOv = p.trigger_overrides || {};
            html += '<div style="padding:10px 18px;">';
            if (cmds.length > 0) {
                html += '<div style="display:flex;flex-wrap:wrap;gap:8px;">';
                for (var c = 0; c < cmds.length; c++) {
                    var cmd = cmds[c];
                    var noteVal = (trigOv[cmd] !== undefined) ? trigOv[cmd] : (notes[c] || '');
                    html += '<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:5px 8px;min-width:130px;max-width:170px;text-align:center;display:flex;flex-direction:column;align-items:center;">';
                    html += '<div style="font-size:11px;font-weight:700;color:' + fg + ';background:' + bg + ';border-radius:4px;padding:2px 8px;margin-bottom:4px;white-space:nowrap;">' + escHtml(cmd) + '</div>';
                    html += '<textarea id="hp-t-' + escAttr(p.plugin_id) + '-' + c + '" style="width:100%;font-size:11px;border:1px solid var(--border);background:var(--bg-primary);color:var(--text-primary);text-align:center;border-radius:4px;padding:3px 4px;resize:vertical;min-height:28px;line-height:1.65;" onfocus="this.style.borderColor=\'var(--accent)\';this.style.background=\'var(--bg-card)\';this.style.minHeight=\'50px\'" onblur="this.style.borderColor=\'var(--border)\';this.style.background=\'var(--bg-primary)\';this.style.minHeight=\'28px\'" placeholder="描述" rows="1">' + escHtml(noteVal) + '</textarea>';
                    html += '</div>';
                }
                html += '</div>';
            }
            html += '</div>';
            html += '</div>';
            return html;
        }

        async function saveFlatPlugin(pluginId) {
            var dnEl = document.getElementById('hp-n-' + pluginId);
            var dsEl = document.getElementById('hp-d-' + pluginId);
            if (!dnEl || !dsEl) { showToast('错误：插件未找到', 'error'); return; }

            // 找原始数据
            var origPlugin = null;
            for (var i = 0; i < _helpModulesData.length && !origPlugin; i++) {
                for (var j = 0; j < _helpModulesData[i].plugins.length; j++) {
                    if (_helpModulesData[i].plugins[j].plugin_id === pluginId) {
                        origPlugin = _helpModulesData[i].plugins[j];
                        break;
                    }
                }
            }

            var newDn = dnEl.value.trim();
            var newDs = dsEl.value.trim();
            var soEl = document.getElementById('hp-so-' + pluginId);
            var sortOrder = soEl ? parseInt(soEl.value) || 0 : 0;
            var clEl = document.getElementById('hp-cl-' + pluginId);
            var color = clEl ? clEl.value : '';

            // 收集触发词覆盖
            var cmds = (origPlugin ? origPlugin.commands : []) || [];
            var trigOv = {};
            for (var c = 0; c < cmds.length; c++) {
                var tEl = document.getElementById('hp-t-' + pluginId + '-' + c);
                if (!tEl) continue;
                var val = tEl.value.trim();
                if (val) trigOv[cmds[c]] = val;
            }

            var result = await putApi('/api/help/plugins/' + encodeURIComponent(pluginId), {
                display_name: newDn,
                description: newDs,
                triggers: trigOv,
                sort_order: sortOrder,
                color: color,
            });
            if (result && result.success) {
                showToast('成功：' + newDn + ' 已保存', 'success');
                if (origPlugin) {
                    origPlugin.display_name = newDn;
                    origPlugin.description = newDs;
                    origPlugin.override_sort_order = sortOrder;
                    origPlugin.override_color = color;
                }
            } else {
                showToast('错误：保存失败', 'error');
            }
        }

        function renderModuleCard(m) {
            var bg = lightenColor(m.color);
            var fg = m.color;
            var html = '';
            // 模块头部 —— 仿 help 渲染器的分类标签
            html += '<div class="card" style="margin-bottom:24px;overflow:visible;">';
            // 分类标题栏（彩色）
            html += '<div style="display:flex;align-items:center;gap:12px;padding:10px 18px;background:' + bg + ';border-radius:10px 10px 0 0;">';
            html += '<input id="hm-dn-' + escAttr(m.name) + '" value="' + escAttr(m.display_name) + '" style="font-weight:700;font-size:16px;border:none;background:transparent;color:' + fg + ';width:180px;" placeholder="分类名">';
            html += '<input id="hm-st-' + escAttr(m.name) + '" value="' + escAttr(m.subtitle || '') + '" style="font-size:12px;border:none;background:transparent;color:' + fg + ';opacity:0.7;flex:1;min-width:120px;" placeholder="副标题（可选）">';
            // 颜色选择器
            html += '<input type="color" id="hm-cl-' + escAttr(m.name) + '" value="' + m.color + '" style="width:24px;height:24px;border:none;cursor:pointer;border-radius:4px;" oninput="var c=this.value;var p=this.parentElement;p.style.background=lightenColor(c);var inps=p.querySelectorAll(\'input[type=text],textarea\');for(var i=0;i<inps.length;i++)inps[i].style.color=c;" onchange="var c=this.value;this.parentElement.style.background=lightenColor(c);var inps=this.parentElement.querySelectorAll(\'input[type=text],textarea\');for(var i=0;i<inps.length;i++)inps[i].style.color=c;" title="模块颜色">';
            html += '<span style="font-size:11px;opacity:0.6;color:' + fg + ';">' + m.plugin_count + ' 插件</span>';
            // 保存 & 重置
            html += '<button class="btn btn-sm" style="margin-left:auto;background:' + fg + ';color:#fff;border:none;padding:4px 14px;font-size:12px;" onclick="saveHelpModuleCard(\'' + escAttr(m.name) + '\')">' + iconImgHtml() + '保存</button>';
            html += '<button class="btn btn-sm" style="background:transparent;color:' + fg + ';border:1px solid ' + fg + ';padding:3px 10px;font-size:11px;" onclick="resetHelpModuleCard(\'' + escAttr(m.name) + '\')">↺</button>';
            html += '</div>';

            // 副标题行单独一行显示模块描述
            html += '<div style="padding:6px 18px;border-bottom:1px solid var(--border);background:var(--bg-primary);">';
            html += '<span style="font-size:12px;color:var(--text-muted);">模块标识: ' + escHtml(m.name) + ' &nbsp;|&nbsp; 排序:</span>';
            html += '<span style="display:inline-flex;align-items:center;gap:2px;margin-left:4px;">';
            html += '<button onclick="event.preventDefault();onModuleSortChange(\'' + escAttr(m.name) + '\',' + Math.max(0, (m.sort_order || 0) - 1) + ')" style="cursor:pointer;background:transparent;border:none;color:var(--text-primary);font-size:16px;line-height:1;padding:0 2px;opacity:0.6;" title="上移">▲</button>';
            html += '<input id="hm-so-' + escAttr(m.name) + '" type="number" value="' + (m.sort_order || 0) + '" style="width:48px;font-size:14px;font-weight:700;border:1px solid var(--border);border-radius:6px;padding:4px 4px;background:var(--bg-card);color:var(--text-primary);text-align:center;" min="0" step="1" onchange="onModuleSortChange(\'' + escAttr(m.name) + '\',this.value)" title="排序">';
            html += '<button onclick="event.preventDefault();onModuleSortChange(\'' + escAttr(m.name) + '\',' + ((m.sort_order || 0) + 1) + ')" style="cursor:pointer;background:transparent;border:none;color:var(--text-primary);font-size:16px;line-height:1;padding:0 2px;opacity:0.6;" title="下移">▼</button>';
            html += '</span>';
            html += '<label style="margin-left:12px;font-size:12px;color:var(--text-muted);"><input type="checkbox" id="hm-en-' + escAttr(m.name) + '" ' + (m.enabled !== false ? 'checked' : '') + ' style="vertical-align:middle;"> 启用</label>';
            html += '</div>';

            // 插件列表
            html += '<div style="padding:12px 18px;">';
            for (var i = 0; i < m.plugins.length; i++) {
                html += renderPluginCard(m, m.plugins[i], i === m.plugins.length - 1);
            }
            html += '</div>';
            html += '</div>';
            return html;
        }

        function renderPluginCard(mod, p, isLast) {
            var fg = mod.color;
            var html = '';
            html += '<div style="display:flex;gap:12px;' + (isLast ? '' : 'margin-bottom:14px;padding-bottom:14px;border-bottom:1px dashed var(--border);') + '">';
            // 左侧装饰条
            html += '<div style="width:4px;border-radius:2px;background:' + fg + ';flex-shrink:0;margin-top:4px;"></div>';
            // 右侧内容
            html += '<div style="flex:1;min-width:0;">';
            // 插件名 + 描述（可编辑）
            html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">';
            html += '<input id="hp-n-' + escAttr(p.plugin_id) + '" value="' + escAttr(p.display_name) + '" style="font-weight:700;font-size:14px;border:1px solid transparent;background:transparent;color:var(--text-primary);width:160px;border-radius:4px;padding:2px 4px;" onfocus="this.style.borderColor=\'var(--accent)\'" onblur="this.style.borderColor=\'transparent\'" placeholder="插件名" title="插件显示名称">';
            html += '<span style="font-size:12px;color:var(--text-muted);">·</span>';
            html += '<input id="hp-d-' + escAttr(p.plugin_id) + '" value="' + escAttr(p.description || '') + '" style="flex:1;font-size:12px;border:1px solid transparent;background:transparent;color:var(--text-secondary);min-width:200px;border-radius:4px;padding:2px 4px;" onfocus="this.style.borderColor=\'var(--accent)\'" onblur="this.style.borderColor=\'transparent\'" placeholder="插件描述" title="插件描述">';
            html += '</div>';

            // 指令触发词网格（描述可编辑，聚焦放大显示完整文本）
            var cmds = p.commands || [];
            var notes = p.notes || [];
            var trigOv = p.trigger_overrides || {};
            if (cmds.length > 0) {
                html += '<div style="display:flex;flex-wrap:wrap;gap:8px;">';
                for (var c = 0; c < cmds.length; c++) {
                    var cmd = cmds[c];
                    // 优先使用用户覆盖的描述，否则用原始 notes
                    var noteVal = (trigOv[cmd] !== undefined) ? trigOv[cmd] : (notes[c] || '');
                    html += '<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:5px 8px;min-width:130px;max-width:170px;text-align:center;display:flex;flex-direction:column;align-items:center;">';
                    html += '<div style="font-size:11px;font-weight:700;color:' + fg + ';background:' + lightenColor(fg) + ';border-radius:4px;padding:2px 8px;margin-bottom:4px;white-space:nowrap;">' + escHtml(cmd) + '</div>';
                    html += '<textarea id="hp-t-' + escAttr(p.plugin_id) + '-' + c + '" style="width:100%;font-size:11px;border:1px solid var(--border);background:var(--bg-primary);color:var(--text-primary);text-align:center;border-radius:4px;padding:3px 4px;resize:vertical;min-height:28px;line-height:1.65;" onfocus="this.style.borderColor=\'var(--accent)\';this.style.background=\'var(--bg-card)\';this.style.minHeight=\'50px\'" onblur="this.style.borderColor=\'var(--border)\';this.style.background=\'var(--bg-primary)\';this.style.minHeight=\'28px\'" placeholder="描述" rows="1">' + escHtml(noteVal) + '</textarea>';
                    html += '</div>';
                }
                html += '</div>';
            }

            html += '</div></div>';
            return html;
        }

        // 保存一个模块的所有设置（模块配置 + 其下所有插件的覆盖）
        async function saveHelpModuleCard(name) {
            var mod = _helpModulesData.find(function(m) { return m.name === name; });
            if (!mod) { showToast('错误：模块未找到: ' + name, 'error'); return; }

            // 模块级配置（从 DOM 读取）
            var dnEl = document.getElementById('hm-dn-' + name);
            var stEl = document.getElementById('hm-st-' + name);
            var clEl = document.getElementById('hm-cl-' + name);
            var enEl = document.getElementById('hm-en-' + name);
            var soEl = document.getElementById('hm-so-' + name);
            if (!dnEl) { showToast('错误：找不到模块元素，请刷新页面', 'error'); return; }

            var modBody = {
                display_name: dnEl.value.trim(),
                subtitle: stEl ? stEl.value.trim() : '',
                color: clEl ? clEl.value : mod.color,
                enabled: enEl ? enEl.checked : true,
                sort_order: soEl ? parseInt(soEl.value) || 0 : (mod.sort_order || 0),
            };

            // 先保存模块配置
            var modResult = await putApi('/api/help/modules/' + encodeURIComponent(name), modBody);
            if (!modResult || !modResult.success) {
                showToast('错误：模块保存失败: ' + (modResult ? modResult.error : '网络错误'), 'error');
                return;
            }

            // 再收集并保存该模块所有插件的覆盖（含触发词描述）
            for (var i = 0; i < mod.plugins.length; i++) {
                var p = mod.plugins[i];
                var dnEl = document.getElementById('hp-n-' + p.plugin_id);
                var dsEl = document.getElementById('hp-d-' + p.plugin_id);
                if (!dnEl || !dsEl) continue;
                var newDn = dnEl.value.trim();
                var newDs = dsEl.value.trim();

                // 收集触发词描述覆盖
                var cmds = p.commands || [];
                var notes = p.notes || [];
                var trigOv = {};
                for (var c = 0; c < cmds.length; c++) {
                    var tEl = document.getElementById('hp-t-' + p.plugin_id + '-' + c);
                    if (!tEl) continue;
                    var val = tEl.value.trim();
                    var origNote = (p.trigger_overrides && p.trigger_overrides[cmds[c]] !== undefined) ? p.trigger_overrides[cmds[c]] : (notes[c] || '');
                    if (val !== origNote) {
                        trigOv[cmds[c]] = val;
                    }
                }

                // 只有有变更才发送
                var hasChanges = (newDn !== p.display_name || newDs !== (p.description || '') || Object.keys(trigOv).length > 0);
                if (hasChanges) {
                    // 分组模式：携带已有的排序和颜色，避免覆盖
                    await putApi('/api/help/plugins/' + encodeURIComponent(p.plugin_id), {
                        display_name: newDn,
                        description: newDs,
                        triggers: trigOv,
                        sort_order: p.override_sort_order || 0,
                        color: p.override_color || '',
                    });
                    // 更新本地插件数据
                    p.display_name = newDn;
                    p.description = newDs;
                    if (Object.keys(trigOv).length > 0) p.trigger_overrides = trigOv;
                }
            }

            // 更新本地模块数据
            var modIdx = _helpModulesData.findIndex(function(m) { return m.name === name; });
            if (modIdx >= 0) {
                _helpModulesData[modIdx].display_name = modBody.display_name;
                _helpModulesData[modIdx].subtitle = modBody.subtitle;
                _helpModulesData[modIdx].color = modBody.color;
                _helpModulesData[modIdx].enabled = modBody.enabled;
                _helpModulesData[modIdx].sort_order = modBody.sort_order;
            }
            showToast('成功：模块 "' + (modBody.display_name || name) + '" 已保存', 'success');
        }

        // 一键保存全部
        async function saveAllHelp() {
            var saved = 0;
            if (_displayMode === 'flat') {
                var allPlugins = [];
                for (var i = 0; i < _helpModulesData.length; i++) {
                    var mod = _helpModulesData[i];
                    for (var j = 0; j < mod.plugins.length; j++) {
                        allPlugins.push({ p: mod.plugins[j], m: mod });
                    }
                }
                for (var k = 0; k < allPlugins.length; k++) {
                    var p = allPlugins[k].p;
                    var dnEl = document.getElementById('hp-n-' + p.plugin_id);
                    var dsEl = document.getElementById('hp-d-' + p.plugin_id);
                    var soEl = document.getElementById('hp-so-' + p.plugin_id);
                    var clEl = document.getElementById('hp-cl-' + p.plugin_id);
                    if (!dnEl || !dsEl) continue;
                    var body = {
                        display_name: dnEl.value.trim(),
                        description: dsEl.value.trim(),
                        sort_order: soEl ? parseInt(soEl.value) || 0 : 0,
                        color: clEl ? clEl.value : '',
                        triggers: {},
                    };
                    var cmds = p.commands || [];
                    for (var c = 0; c < cmds.length; c++) {
                        var tEl = document.getElementById('hp-t-' + p.plugin_id + '-' + c);
                        if (tEl && tEl.value.trim()) body.triggers[cmds[c]] = tEl.value.trim();
                    }
                    var r = await putApi('/api/help/plugins/' + encodeURIComponent(p.plugin_id), body);
                    if (r && r.success) saved++;
                }
            } else {
                // 分组模式：先保存模块，再保存插件
                for (var i = 0; i < _helpModulesData.length; i++) {
                    var m = _helpModulesData[i];
                    var soEl = document.getElementById('hm-so-' + m.name);
                    var modBody = {
                        display_name: document.getElementById('hm-dn-' + m.name).value,
                        subtitle: document.getElementById('hm-st-' + m.name).value,
                        color: document.getElementById('hm-cl-' + m.name).value,
                        enabled: document.getElementById('hm-en-' + m.name).checked,
                        sort_order: soEl ? parseInt(soEl.value) || 0 : 0,
                    };
                    var mr = await putApi('/api/help/modules/' + encodeURIComponent(m.name), modBody);
                    if (mr && mr.success) saved++;
                    // 保存该模块下所有插件
                    for (var j = 0; j < m.plugins.length; j++) {
                        var p = m.plugins[j];
                        var dnEl = document.getElementById('hp-n-' + p.plugin_id);
                        var dsEl = document.getElementById('hp-d-' + p.plugin_id);
                        if (!dnEl || !dsEl) continue;
                        var pBody = { display_name: dnEl.value.trim(), description: dsEl.value.trim(), triggers: {} };
                        var cmds = p.commands || [];
                        for (var c = 0; c < cmds.length; c++) {
                            var tEl = document.getElementById('hp-t-' + p.plugin_id + '-' + c);
                            if (tEl && tEl.value.trim()) pBody.triggers[cmds[c]] = tEl.value.trim();
                        }
                        await putApi('/api/help/plugins/' + encodeURIComponent(p.plugin_id), pBody);
                    }
                }
            }
            showToast('成功：已保存 ' + saved + ' 项', 'success');
        }

        async function resetHelpModuleCard(name) {
            if (!confirm('确定要重置模块 "' + name + '" 为默认值吗？（会清除所有自定义设置）')) return;
            var result = await postApi('/api/help/modules/reset', { name: name });
            if (result && result.success) {
                showToast('成功：' + result.message, 'success');
                loadHelpModules();
            } else {
                showToast('错误：重置失败', 'error');
            }
        }

        // ====== 初始加载 ======
        refreshAll();
    </script>
</body>
</html>"""


