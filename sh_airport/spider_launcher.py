from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import os


def run_spider():
    os.system('scrapy crawl sh-airport')


if __name__ == '__main__':
    executors = {
        'default': ThreadPoolExecutor(max_workers=5)
    }
    scheduler = BlockingScheduler(executors=executors)
    scheduler.add_job(run_spider, "cron", hour=23, minute=30)
    scheduler.start()

