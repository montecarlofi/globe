from datetime import date

DATE_START  = date(2022, 8, 2)
DATE_END    = date(2032, 8, 1)
INFO_FILE   = 'runners.csv'
#START_MONTH = 8
#START_YEAR  = 2022
n_days_year = 365
years = round((DATE_END-DATE_START).days / n_days_year)
#print("years", years)

date_today = date.today()
days_total = (DATE_END-DATE_START).days
weeks_total= int(days_total/7)
days_gone  = (date_today-DATE_START).days
weeks_gone = days_gone/7
days_left  = (DATE_END-date_today).days
weeks_left = days_left/7

TOTAL       = 40075
n_days 		= 10*n_days_year
weekly_math = TOTAL / (n_days/7) # 76.85616438356165
yearly      = TOTAL/10
n_weeks 	= n_days/7 # 521.4285714285714
daily_math	= TOTAL/n_days
yearly_math	= TOTAL/years

Y_YEAR = [x*daily_math for x in range(1, n_days_year+1)]
X_YEAR = range(1, n_days_year+1)
