import schedule
import asyncio
import time
from scrape_jobs import main

def job():
    print("⏰ Running job scraping script...")
    asyncio.run(main())

# Schedule it every 30 minutes
schedule.every(30).minutes.do(job)

job()

print("📅 Scheduler started. Running every 30 minutes...")
while True:
    schedule.run_pending()
    time.sleep(1)
