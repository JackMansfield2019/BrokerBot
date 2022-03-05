def market_closed(now=None):
    tz = pytz.timezone('US/Eastern')
    us_holidays = holidays.US()

    openTime = datetime.time(hour=9, minute=30, second=0)
    closeTime = datetime.time(hour=16, minute=0, second=0)

    if not now:
        now = datetime.datetime.now(tz)

    # If a holiday
    if now.strftime('%Y-%m-%d') in us_holidays:
        return True
    # If before 0930 or after 1600
    if (now.time() < openTime) or (now.time() > closeTime):
        return True
    # If it's a weekend
    if now.date().weekday() > 4:
        return True

    return False