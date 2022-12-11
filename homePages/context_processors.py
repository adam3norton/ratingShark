from datetime import datetime as dt
from datetime import timedelta

def date_processor(request):

    current_date = (dt.now() - timedelta(hours=7)).date()
    formatted_date = f'{current_date.strftime("%b")} {current_date.strftime("%d")}, {current_date.strftime("%Y")}'

    return {
        'formatted_date' : formatted_date
    }