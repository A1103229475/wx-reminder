from apscheduler.schedulers.blocking import BlockingScheduler


class Scheduler():
    def __init__(self):
        self.scheduler = BlockingScheduler(timezone='Asia/Shanghai')

    def start(self):
        print("定时器开始了")
        self.scheduler.start()

    def add_job(self, job_func):
        print(f"新增任务 {job_func}")
        self.scheduler.add_job(job_func, 'cron', hour='7', minute='30')

    def shutdown(self):
        self.scheduler.shutdown()