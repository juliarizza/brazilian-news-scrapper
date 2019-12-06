import datetime

def daterange(start_date, end_date):
    date = start_date
    delta = datetime.timedelta(days=1)
    while date <= end_date:
        yield date
        date += delta

def beautify(text):
    if text:
        return text.strip() \
                .replace('<BR>', ' ') \
                .replace('<br>', ' ') \
                .replace('<BR />', ' ') \
                .replace('<br /', ' ')