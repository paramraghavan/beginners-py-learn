import schedule
import time


def my_job():
    print("I'm working...")


schedule.every(10).minutes.do(my_job)
schedule.every().hour.do(my_job)
schedule.every().day.at("10:30").do(my_job)

while True:
    schedule.run_pending()
    time.sleep(1)