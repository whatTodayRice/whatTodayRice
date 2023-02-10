from datetime import datetime ,timezone,timedelta


KST = timezone(timedelta(hours=9))
time_record=datetime.now(KST)
print(time_record)
print(datetime.today().strftime("%A"))
print(time_record.strftime("%A"))