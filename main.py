from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import asyncio

app = FastAPI()

# ======================== API কনফিগারেশন ========================
# 🟢 MNIT API CONFIG (একমাত্র প্যানেল)
MNIT_API_URL = "https://x.mnitnetwork.com/mapi/v1/mdashboard/console/info"

# নতুন Mauthtoken আপডেট করা হয়েছে
MNIT_MAUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJNX0k0VkE3RkU2UiIsInJvbGUiOiJ1c2VyIiwiYWNjZXNzX3BhdGgiOlsiL2Rhc2hib2FyZCJdLCJleHBpcnkiOjE3Nzc0MzIxMTksImNyZWF0ZWQiOjE3NzczNDU3MTksIjJvbzkiOiJNc0giLCJleHAiOjE3Nzc0MzIxMTksImlhdCI6MTc3NzM0NTcxOSwic3ViIjoiTV9JNFZBN0ZFNlIifQ.C-yNKJJZSRCXA1DHNoo2NQ6eGrPbHI4UrvwLMWLyjeI"

# নতুন Cookie আপডেট করা হয়েছে
MNIT_COOKIE = "cf_clearance=uClutdvcwOeVatW5_fDJYtc0kJH2.KmVkd44mW7hTh0-1777345712-1.2.1.1-hFKnn925n6n.82YBiSg2WTdR4nXI3_dx3EgAMo.63IpTM__24mNgsps6AhNInGBW31DhLcDX.DrSrQ43TD2bgMVw7SlDtm8I9oB5b630Hyl0KtR0Dkv3vD_0QwACSRjHVTjbrBTpG_tozXLj1xHNPj4yORJgzAhRwh9SzpKkQh2GYKetcFf.hYZaA_uTP_Y.SR59jVP3qq6eGohJCH9663nOkYnHlymq7YVANa3oboggXdAn.55on5cVCafVpBUln5XqTnFWGKUUi9hCNd85OjbKHXMrSXnrzm2FogeH9uwY_uuBnE8Gk5Y705FiciyLrQyNcxE9yJJERPpVUk7Abw; mauthtoken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJNX0k0VkE3RkU2UiIsInJvbGUiOiJ1c2VyIiwiYWNjZXNzX3BhdGgiOlsiL2Rhc2hib2FyZCJdLCJleHBpcnkiOjE3Nzc0MzIxMTksImNyZWF0ZWQiOjE3NzczNDU3MTksIjJvbzkiOiJNc0giLCJleHAiOjE3Nzc0MzIxMTksImlhdCI6MTc3NzM0NTcxOSwic3ViIjoiTV9JNFZBN0ZFNlIifQ.C-yNKJJZSRCXA1DHNoo2NQ6eGrPbHI4UrvwLMWLyjeI"

# ======================== Data Fetching Logic ========================
async def fetch_mnit(client):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Mauthtoken": MNIT_MAUTH_TOKEN,
        "Cookie": MNIT_COOKIE,
        "Referer": "https://x.mnitnetwork.com/mdashboard/console"
    }
    try:
        response = await client.get(MNIT_API_URL, headers=headers, timeout=10.0)
        if response.status_code == 200:
            data = response.json()
            logs = data.get("data", {}).get("logs", [])
            if logs:
                for l in logs: l['sys_node'] = "mnit"
                return logs[:100] # ১০০ টা ডেটা নিয়ে আসবে
    except Exception:
        pass
    return []

# ======================== API Endpoints ========================
@app.get("/api/logs")
async def get_logs():
    try:
        async with httpx.AsyncClient() as client:
            mnit_logs = await fetch_mnit(client)
            return mnit_logs if mnit_logs else []
    except Exception:
        return []

@app.get("/")
def read_root():
    return HTMLResponse(content=INDEX_HTML)

# ======================== ULTIMATE PREMIUM UI (SINGLE PANEL) ========================
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SKY RANGE ⚡ - SUPREME DASHBOARD</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
    <style>
        :root { 
            --bg-main: #030712; 
            --card-bg: rgba(17, 24, 39, 0.7); 
            --card-border: rgba(255, 255, 255, 0.1); 
            --text-main: #f8fafc; 
            --text-muted: #94a3b8; 
            --accent: #00f2fe; 
            --panel-color: #10b981; /* NEON GREEN */
        }
        
        body { 
            background-color: var(--bg-main); 
            color: var(--text-main); 
            font-family: 'Orbitron', sans-serif; 
            text-transform: uppercase; 
            margin: 0; 
            padding: 0; 
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(0, 242, 254, 0.08) 0%, transparent 60%),
                linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 100% 100%, 30px 30px, 30px 30px;
            background-attachment: fixed; 
        }
        
        .top-header { display: flex; justify-content: space-between; padding: 15px 25px; background: rgba(3, 7, 18, 0.9); backdrop-filter: blur(15px); position: sticky; top: 0; z-index: 50; border-bottom: 2px solid var(--accent); box-shadow: 0 5px 20px rgba(0, 242, 254, 0.15);}
        .brand-title { font-size: 1.4rem; font-weight: 900; color: white; letter-spacing: 2px; text-shadow: 0 0 10px var(--accent);}
        
        .logo-area { padding: 40px 20px 30px 20px; display: flex; flex-direction: column; align-items: center; gap: 15px; }
        .logo-text { font-size: 3.5rem; font-weight: 900; background: linear-gradient(to right, #4facfe, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 4px; text-shadow: 0px 0px 20px rgba(0,242,254,0.4); text-align: center;}
        .logo-text span { background: linear-gradient(to right, #a18cd1, #fbc2eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .live-badge { background: rgba(0, 242, 254, 0.1); color: var(--accent); padding: 8px 25px; border-radius: 5px; font-weight: 900; letter-spacing: 2px; border: 1px solid var(--accent); box-shadow: 0 0 20px rgba(0, 242, 254, 0.4); animation: pulse 2s infinite;}
        
        @keyframes pulse { 0% { box-shadow: 0 0 10px rgba(0, 242, 254, 0.2); } 50% { box-shadow: 0 0 25px rgba(0, 242, 254, 0.6); } 100% { box-shadow: 0 0 10px rgba(0, 242, 254, 0.2); } }

        .filters { display: flex; gap: 15px; padding: 0 20px; overflow-x: auto; margin-bottom: 40px; scrollbar-width: none; justify-content: center;}
        .filters::-webkit-scrollbar { display: none; }
        .filter-btn { background: var(--card-bg); border: 1px solid var(--card-border); color: var(--text-muted); padding: 12px 25px; border-radius: 4px; cursor: pointer; white-space: nowrap; font-weight: 700; font-family: 'Orbitron', sans-serif; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s; }
        .filter-btn.active { background: rgba(0, 242, 254, 0.15); color: var(--accent); border-color: var(--accent); box-shadow: 0 0 20px rgba(0, 242, 254, 0.3); }
        .btn-high-power { background: linear-gradient(135deg, #ff0844, #ffb199); color: white !important; border: none; font-weight: 900; box-shadow: 0 0 20px rgba(255, 8, 68, 0.5); }
        
        /* 🟢 SINGLE LAYOUT (MAKING IT CENTERED & WIDE) */
        .main-container { display: flex; flex-direction: column; gap: 30px; padding: 0 30px 60px 30px; max-width: 900px; margin: 0 auto;}
        
        .panel-box { background: rgba(0,0,0,0.4); border-radius: 12px; padding: 25px; border: 1px solid rgba(255,255,255,0.05); }
        
        .column-header { text-align: center; padding: 15px; margin-bottom: 30px; font-weight: 900; font-size: 1.5rem; letter-spacing: 3px; border-radius: 8px; backdrop-filter: blur(10px); background: rgba(16, 185, 129, 0.1); color: var(--panel-color); border: 2px solid var(--panel-color); box-shadow: 0 0 25px rgba(16, 185, 129, 0.2); text-shadow: 0 0 10px var(--panel-color);}
        
        .column-content { display: flex; flex-direction: column; gap: 20px; }

        .range-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 8px; padding: 20px; transition: all 0.3s; position: relative; overflow: hidden; backdrop-filter: blur(10px); border-left: 5px solid var(--panel-color); }
        .range-card:hover { transform: translateY(-5px) scale(1.02); z-index: 10; background: rgba(17, 24, 39, 0.9); border-color: var(--panel-color); box-shadow: 0 10px 30px -5px rgba(16, 185, 129, 0.3); }
        
        .high-power-card { background: linear-gradient(145deg, rgba(30, 10, 15, 0.9), rgba(67, 20, 30, 0.6)) !important; border: 1px solid rgba(255, 8, 68, 0.4) !important; border-left: 5px solid #ff0844 !important;}
        
        .range-header { display: flex; justify-content: space-between; align-items: center; color: var(--text-muted); font-size: 0.9rem; margin-bottom: 15px; font-weight: 700; }
        .service-name { color: #fff; font-weight: 900; font-size: 1.2rem; letter-spacing: 1px; display: flex; align-items: center; gap: 10px;}
        
        .sms-box { background: rgba(0, 242, 254, 0.05); border: 1px dashed rgba(0, 242, 254, 0.4); border-radius: 4px; padding: 12px 15px; margin-bottom: 15px; font-size: 0.9rem; color: #e0f2fe; display: flex; align-items: center; gap: 10px; font-family: 'JetBrains Mono', monospace; font-weight: bold;}
        .high-power-card .sms-box { background: rgba(255, 8, 68, 0.05); border-color: rgba(255, 8, 68, 0.4); color: #ffe4e6;}
        .sms-icon { font-size: 1.3rem; }
        
        .copy-area { background: #000; border-radius: 6px; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.1); }
        .range-number { font-size: 1.6rem; font-family: 'JetBrains Mono', monospace; color: var(--accent); font-weight: 800; letter-spacing: 3px; text-shadow: 0 0 10px rgba(0,242,254,0.3);}
        .high-power-card .range-number { color: #ffb199; text-shadow: 0 0 10px rgba(255,177,153,0.3); }
        
        .copy-btn { background: var(--accent); color: #000; border: none; padding: 8px 18px; border-radius: 4px; cursor: pointer; font-weight: 900; font-size: 0.9rem; transition: all 0.2s; font-family: 'Orbitron', sans-serif; text-transform: uppercase;}
        .copy-btn:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .copy-btn:active { transform: scale(0.9); }
        
        .hit-badge { background: linear-gradient(45deg, #ff0844, #ffb199); color: white; padding: 5px 12px; border-radius: 4px; font-weight: 900; font-size: 0.8rem; letter-spacing: 1px; box-shadow: 0 0 15px rgba(255,8,68,0.4);}
        
        .footer-brand { text-align: center; color: rgba(255,255,255,0.3); font-size: 1rem; margin: 50px 0; font-weight: 700; letter-spacing: 2px;}
        .footer-brand span { color: var(--accent); font-weight: 900;}

        #toast { visibility: hidden; min-width: 300px; background: rgba(0, 242, 254, 0.9); backdrop-filter: blur(10px); color: #000; text-align: center; border-radius: 8px; padding: 18px; position: fixed; z-index: 1000; bottom: 40px; left: 50%; transform: translateX(-50%); font-weight: 900; font-size: 1.1rem; letter-spacing: 1px; box-shadow: 0 0 30px rgba(0,242,254,0.6);}
        #toast.show { visibility: visible; animation: popUp 0.3s forwards, fadeOut 0.4s ease-in 2.5s forwards; }
        @keyframes popUp { 0% { bottom: 0; opacity: 0; transform: translateX(-50%) scale(0.8); } 100% { bottom: 40px; opacity: 1; transform: translateX(-50%) scale(1); } }
        @keyframes fadeOut { from { opacity: 1; } to { opacity: 0; visibility: hidden;} }
    </style>
</head>
<body>
    <div class="top-header"><div class="brand-title">☁️ SKY RANGE SYSTEM</div></div>
    
    <div class="logo-area">
        <div class="live-badge">⚡ SECURE CONNECTION</div>
        <div class="logo-text">SKY<span>·RANGE</span></div>
    </div>
    
    <div class="filters">
        <button class="filter-btn active" onclick="switchTab('all')">◉ ALL TRAFFIC</button>
        <button class="filter-btn" onclick="switchTab('facebook')">FACEBOOK</button>
        <button class="filter-btn" onclick="switchTab('whatsapp')">WHATSAPP</button>
        <button class="filter-btn btn-high-power" onclick="switchTab('high-power')">🔥 TOP HITS</button>
    </div>
    
    <div class="main-container">
        <div class="panel-box">
            <div class="column-header">🟢 SECURE PANEL [ LIVE DATA ]</div>
            <div class="column-content" id="main-data-col">
                <p style="text-align:center; color: #10b981; font-weight:bold; letter-spacing:2px;">SCANNING DATA...</p>
            </div>
        </div>
    </div>
    
    <div class="footer-brand">SYS DEPLOYED BY <span>SKY NETWORKS</span></div>
    <div id="toast">✅ NUMBER COPIED!</div>

    <script>
        let currentTab = 'all';

        function switchTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            fetchData();
        }

        function copyText(text) {
            navigator.clipboard.writeText(text).then(() => {
                var toast = document.getElementById("toast");
                toast.innerText = "📋 " + text + " COPIED!";
                toast.classList.remove("show");
                void toast.offsetWidth; toast.classList.add("show");
            });
        }

        async function fetchData() {
            try {
                const response = await fetch('/api/logs');
                const logs = await response.json();
                renderData(logs);
            } catch (err) { console.error("API ERROR", err); }
        }

        function formatNumberToRange(val) {
            if (!val) return "";
            if (val.toUpperCase().includes('X')) return val.toUpperCase();
            return val + "XXX";
        }

        function buildCard(item, isHighPower) {
            const displayRange = formatNumberToRange(isHighPower ? (item.prefix + "XXXX") : (item.range || item.number || item.number_raw || ''));
            const srvName = isHighPower ? item.service : (item.app_name || item.service || 'SERVICE');
            const ctry = item.country || 'GLOBAL';
            const extraClass = isHighPower ? 'high-power-card' : '';
            
            const topRight = isHighPower ? `<span class="hit-badge">🔥 ${item.count} HITS</span>` : `<span>${item.time || item.delivered_at || ''}</span>`;
            const btmRight = isHighPower ? `<span style="color: #10b981; font-weight:bold;">HIGHLY ACTIVE</span>` : `<span>🏢 ${item.carrier || 'UNKNOWN'}</span>`;

            const rawSms = item.sms || item.message || "NO SMS CONTENT FOUND";
            const cleanSms = rawSms.length > 55 ? rawSms.substring(0, 52) + "..." : rawSms;
            
            const smsHtml = `
            <div class="sms-box" title="FULL MSG: ${rawSms}">
                <span class="sms-icon">💬</span>
                <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${cleanSms}</span>
            </div>`;

            return `
            <div class="range-card ${extraClass}">
                <div class="range-header">
                    <span class="service-name">${srvName}</span>
                    ${topRight}
                </div>
                ${smsHtml} 
                <div class="copy-area">
                    <div class="range-number">${displayRange}</div>
                    <button class="copy-btn" onclick="copyText('${displayRange}')">COPY</button>
                </div>
                <div class="range-header" style="margin: 0; color: #fff;">
                    <span>🌐 ${ctry}</span>
                    ${btmRight}
                </div>
            </div>`;
        }

        function renderData(logs) {
            const mainCol = document.getElementById('main-data-col');
            let htmlContent = '';

            if(!logs || logs.length === 0) {
                mainCol.innerHTML = '<p style="text-align:center; color:#94a3b8; font-weight:bold; margin-top:20px;">NO ACTIVE DATA FOUND</p>';
                return;
            }

            if (currentTab === 'high-power') {
                let rangeCounts = {};
                logs.forEach(log => {
                    const srv = (log.app_name || log.service || 'UNKNOWN').toUpperCase();
                    const rawNum = log.range || log.number || log.number_raw || '';
                    const cleanNum = rawNum.replace(/[^0-9]/g, '');
                    if(cleanNum.length >= 7) {
                        const prefix = cleanNum.substring(0, 7);
                        const key = srv + "|" + prefix;
                        if(!rangeCounts[key]) {
                            rangeCounts[key] = { 
                                prefix: prefix, service: srv, count: 0, 
                                country: log.country, sms: log.sms || log.message || "NO SMS CONTENT"
                            };
                        }
                        rangeCounts[key].count++;
                    }
                });

                const sortedRanges = Object.values(rangeCounts).sort((a, b) => b.count - a.count);
                sortedRanges.forEach(r => { htmlContent += buildCard(r, true); });
            } else {
                logs.forEach(log => {
                    const srv = (log.app_name || log.service || 'UNKNOWN').toLowerCase();
                    let matchSrv = currentTab === 'whatsapp' ? 'whatsapp|twilio' : currentTab;
                    if (currentTab !== 'all' && !matchSrv.includes(srv) && !srv.includes(currentTab)) return;

                    htmlContent += buildCard(log, false);
                });
            }

            mainCol.innerHTML = htmlContent || '<p style="text-align:center; color:#94a3b8; font-weight:bold; margin-top:20px;">NO DATA MATCHES THIS FILTER</p>';
        }
        
        setInterval(fetchData, 5000); 
        fetchData();
    </script>
</body>
</html>
"""
