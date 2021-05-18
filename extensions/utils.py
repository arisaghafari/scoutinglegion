from . import jalali
from django.utils import timezone

def persian_number_converter(num):
    numbers = {
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
        "0": "۰",
    }
    for e, p in numbers.items():
        num = num.replace(e ,p)
    return num

def jalali_converter(time):

    time = timezone.localtime(time)
    jmonth = ["فرودین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    time_str = "{},{},{}".format(
        time.year,
        time.month,
        time.day)
    time_to_tuple = jalali.Gregorian(time_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    output = "{} {} {} , ساعت {}:{}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute
    )

    return persian_number_converter(output)