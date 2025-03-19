import datetime
from pytz import timezone

class Calendar():
    MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    def time_since(self, year, month, day, hour, minute, second):
        now = datetime.datetime.now()
        date = datetime.datetime(year, month, day, hour, minute, second)

        result = {"Y": 0, "M": 0, "D": 0, "h": 0, "m": 0, "s": 0}

        # First Adjustment (different year)
        if now.year != year: 
            if second > 0:
                result["s"] += 60 - second
                minute += 1
                second = 0
            
            if minute == 60:
                hour += 1

            if minute > 0:
                result["m"] += 60 - minute
                hour += 1
            elif minute < 0:
                hour -= 2
                result["m"] += 1
            minute = 0
            
            if hour == 24:
                hour = 0

            if hour > 0:
                result["h"] += 24 - hour
            elif hour < 0:
                day += 1
                result["h"] += 1
            hour = 0

            if day > self.MONTH_DAYS[month-1]:
                day = 1
            if day < 1:
                month += 1
                result["D"] += 1
            elif day > 1:
                result["D"] += self.MONTH_DAYS[month-1] - day
            day = 1

            if month > 12:
                year += 1
                month = 1
            if month < 1:
                year += 1
                result["M"] += 1
            elif month > 1:
                year += 1
                result["M"] += 12 - month
            month = 1

            result["Y"] += now.year - year
        
            result["s"] += now.second
            result["m"] += now.minute + result["s"]//60
            result["s"] %= 60
            result["h"] += now.hour + result["m"]//60
            result["m"] %= 60
            result["D"] = self.MONTH_DAYS[now.month-2] + (now.month == 2 and now.year%4 == 0) - date.day + now.day - 1 + result["h"]//24
            result["h"] %= 24
            result["M"] += now.month - 1

        print(now, date)
        return result


