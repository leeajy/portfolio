import json
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from datetime import datetime

def lambda_handler(event, context):
    date_str = event.get('date', '')

    # check that the date is not a weekend or holiday
    date_datetime = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = date_datetime.weekday()
    if weekday > 4: 
        raise Exception('Markets closed - weekend.')
    cal = USFederalHolidayCalendar()
    year = date_datetime.year
    holidays = cal.holidays(start=f'{year}-01-01', end=f'{year+1}-01-01').to_pydatetime()
    if date_datetime in holidays:
        raise Exception('Markets closed - holiday.')
    return {
        'statusCode': 200,
        'dateStr': date_str
    }
