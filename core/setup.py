from services.service import WXService
from common.scheduler import Scheduler


if __name__ == '__main__':
    scheduler = Scheduler()
    wxService = WXService()

    scheduler.add_job(wxService.send_everyday_reminder)
    scheduler.add_job(wxService.send_today_weather_reminder)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()