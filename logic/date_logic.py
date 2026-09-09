from datetime import date

class DateLogic:

    def calculate_difference(self, from_date, to_date):

        if to_date < from_date:
            from_date, to_date = to_date, from_date

        total_days = (to_date - from_date).days

        years, months, days = self._difference_breakdown(from_date, to_date)

        return {
            'total_days': total_days,
            'total_months': total_days / 30.44,
            'total_years': total_days / 365.25,
            'years': years,
            'months': months,
            'days': days,
        }


    def validate_date(self, day, month, year):
        try:
            return date(year, month, day)
        except ValueError:
            return None


    def _difference_breakdown(self, from_date, to_date):

        years = to_date.year - from_date.year
        months = to_date.month - from_date.month
        days = to_date.day - from_date.day

        if days < 0:
            months -= 1
            if to_date.month == 1:
                prev_month_start = date(to_date.year - 1, 12, 1)
            else:
                prev_month_start = date(to_date.year, to_date.month - 1, 1)
            days += (date(to_date.year, to_date.month, 1) - prev_month_start).days

        if months < 0:
            years -= 1
            months += 12

        return years, months, days