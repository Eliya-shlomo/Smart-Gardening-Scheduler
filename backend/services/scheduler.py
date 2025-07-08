from apscheduler.schedulers.background import BackgroundScheduler
from .recommendation_scheduler import run_recommendation_job

scheduler = BackgroundScheduler()

# def start_scheduler():
    # scheduler.add_job(run_recommendation_job, "cron", hour=7) 
    # scheduler.start()
