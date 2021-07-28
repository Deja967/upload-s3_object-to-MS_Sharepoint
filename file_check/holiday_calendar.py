import datetime as dt
from pandas.tseries.holiday import *


class CustomBusinessCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Year', month=1, day=1, observance=sunday_to_monday),
        Holiday('USMartinLutherKingDay', month=1, day=18, observance=sunday_to_monday),
        Holiday('USPresidentsDay', month=2, day=15, observance=sunday_to_monday),
        Holiday('MemorialDay', month=5, day=31, observance=sunday_to_monday),
        Holiday('Juneteenth', month=6, day=19, observance=sunday_to_monday),
        Holiday('IndependenceDay', month=7, day=4, observance=sunday_to_monday),
        Holiday('LaborDay', month=9, day=6, observance=sunday_to_monday),
        Holiday('ColumbusDay', month=10, day=11, observance=sunday_to_monday),
        Holiday('VeteransDay', month=11, day=11, observance=sunday_to_monday),
        Holiday('ThanksgivingDay', month=11, day=25, observance=sunday_to_monday),
        Holiday('Christmas', month=12, day=25, observance=sunday_to_monday)
    ]


def getting_year():
    get_year = datetime.now()
    current_year = get_year.year
    return current_year


def no_business_holiday():
    current_year = getting_year()
    today = datetime.today().strftime('%Y-%m-%d')
    calendar = CustomBusinessCalendar()
    work_holidays = calendar.holidays(dt.datetime(current_year - 1, 12, 31), dt.datetime(current_year, 12, 31))

    if today in work_holidays:
        print("today is a holiday, not expecting new file")
    else:
        print("today is not a holiday, raising error...")
        raise FileNotFoundError("FILE NOT FOUND: no new file added")
    return work_holidays


if __name__ == '__main__':
    getting_year()
    print(no_business_holiday())
