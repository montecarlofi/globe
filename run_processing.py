from datetime import date, timedelta
from running_setup import TOTAL, DATE_START, n_days_year #, INFO_FILE
import pandas as pd

def calc_progress(runners):
	first_day_of_cycle = __first_day_of_cycle__()
	n_days_in_cycle = count_days_between(first_day_of_cycle, today()) # days_gone_since(first_day_of_cycle())
	n_left_in_cycle = n_days_year - n_days_in_cycle

	first_day_of_cycle = __first_day_of_cycle__()
	for r in runners:
		dates, distances = r['dates'], r['distances']
		start_date = __str_to_date__(r['start_date'])
		end_date   = __str_to_date__(r['end_date'])
		#start_date = r['start_date']
		#end_date   = r['end_date']
		#r['start_date'] = start_date
		#r['end_date']   = end_date
		progress_total  = __progress_since__(dates, distances, cutoff_date=start_date)
		progress_year   = __progress_since__(dates, distances, cutoff_date=first_day_of_cycle)
		n_years_left    = __count_days_between__(today(), end_date)
		n_years_left    = n_years_left/n_days_year
		n_years         = round(__count_days_between__(start_date, end_date)/n_days_year) # Bad method.
		n_days_running  = __count_days_between__(start_date, today())
		n_days_in_cycle = __count_days_between__(today(), first_day_of_cycle)
		n_days_left     = __count_days_between__(today(), end_date)
		r['n_days_running'] = n_days_running
		r['path_year_ideal'] = TOTAL / n_years / n_days_year
		r['progress_total'] = progress_total
		r['progress_year'] = progress_year
		r['remain_total'] = TOTAL - progress_total
		r['remain_year'] = (TOTAL/n_years) - progress_year
		r['path_to_total'] = (TOTAL - progress_total) / n_days_left
		r['path_to_year'] = ((TOTAL/n_years) - progress_year) / n_left_in_cycle
		r['week_path_to_year'] = (((TOTAL/n_years) - progress_year) / n_left_in_cycle) * 7
		r['average_math_weekly'] = (TOTAL/n_years/n_days_year) * 7
		r['average_math_daily'] = (TOTAL/n_years/n_days_year)
	return runners

def daydate(*a):
	return date(*a) 

def today():
	return date.today()

def apply_cutoff(runners):
	for runner in runners:
		try:
			cutoff_date = __str_to_date__(runner['start_date'])
		except Exception as e:
			cutoff_date = runner['start_date']
		
		#print(f'cutoff_date {cutoff_date}')
		dates, distances = runner['dates'], runner['distances']
		dates, distances = __trim__(cutoff_date, dates, distances) # Cuts of data before start date.
		runner['dates'], runner['distances'] = dates, distances
	return runners

def __progress_since__(dates, distances, cutoff_date):
#	print(f'Prog since {dates} and {distances} for cutoff {cutoff_date}')
	asum = 0
	for i in range(len(dates)):
		the_date = __str_to_date__(dates[i])
		#print(f'the_date {the_date} and for cutoff {cutoff_date}')
		asum = asum+distances[i] if the_date >= cutoff_date else asum
	return asum

def count_days_between(*aa):
	return __count_days_between__(*aa)

def __count_days_between__(a, b):
	return (b-a).days

def cycle_days_gone(first_day):
	start_month = int(str(first_day)[5:7])
	start_day   = int(str(first_day)[8:10])
	this_year   = date.today().year
	this_month  = date.today().month
	this_day    = date.today().day

	if this_month > start_month: # We're in the same year.
		the_year = this_year
	elif this_month < start_month:
		the_year = this_year - 1
	elif this_month == start_month and this_day < start_day:
		the_year = this_year - 1
	elif this_month == start_month and this_day >= start_day:
		the_year = this_year

	a = date(the_year, start_month, start_day)
	b = date(this_year, this_month, this_day)
	diff = (b-a).days
	return diff  # - 1 # We don't include today, i.e., from the 10th to the 1st, nine days passed.

def days_gone_since(first_day, last_day=date.today()):
	start_year  = int(str(first_day)[0:4])
	start_month = int(str(first_day)[5:7])
	start_day   = int(str(first_day)[8:10])
	first_day   = date(start_year, start_month, start_day)
	return (last_day-first_day).days
#print(days_gone_since(date(2021, 4, 5), date.today()))

def first_day_of_cycle(*a, **k):
	return __first_day_of_cycle__(*a, **k)

def __first_day_of_cycle__(D=DATE_START):
	start_month = int(str(D)[5:7])
	start_day   = int(str(D)[8:10])
	today = date.today()
	y = today.year
	m = today.month
	d = today.day

	if m > start_month: # We're in the same year.
		the_year = y
	elif m < start_month:
		the_year = y - 1
	elif m == start_month and d < start_day:
		the_year = y - 1
	elif m == start_month and d >= start_day:
		the_year = y

	return date(the_year, start_month, start_day)

def __last_day_of_cycle__(D=DATE_START):
	start_month = int(str(D)[5:7])
	start_day   = int(str(D)[8:10])
	today = date.today()
	y = today.year
	m = today.month
	d = today.day

	if m > start_month:
		the_year = y + 1
	elif m < start_month:
		the_year = y
	elif m == start_month and d < start_day:
		the_year = y
	elif m == start_month and d >= start_day:
		the_year = y + 1

	return date(the_year, start_month, start_day)

def __trim__(cutoff_date, dates, distances):
	newdates, newdistances = [], []
	index = 0
	for day in dates:
		year, month, day = int(day[0:4]), int(day[5:7]), int(day[8:10])
		some_date = date(year, month, day)
		#diff = (some_date - date_cutoff).days
		#print("Diff", diff)
		#if diff >= 0:
		if some_date >= cutoff_date:
			#print(f'some_date = {some_date}')
			newdates.append(dates[index])
			newdistances.append(distances[index])
		index += 1
	return newdates, newdistances

def __ensure_ascending__(dates, distances):
	first_item = __str_to_date__(dates[0])
	last_item  = __str_to_date__(dates[-1])
	if first_item > last_item:
		dates.reverse()
		distances.reverse()
	del first_item, last_item
	return dates, distances

def ascending(runners, column): # Doesn't do what it's supposed to do.
	for r in runners:
		data = { 
			'dates': r['dates'],
			'distances': r['distances']
		}
		df = pd.DataFrame(data)
		#df['dates'] = pd.to_datetime(df['dates'])
		df.sort_values(by='dates', inplace=True)
		r['dates'] = list(df['dates'])
		r['distances'] = list(df['distances'])
	return runners

def sum_moving_sequence(*a, **k):
	return __sum_moving_sequence__(*a, *k)

def __sum_moving_sequence__(runners, var_name, fromm, until=0):
	for r in runners:
		start = fromm
		if start < -r['n_days_running']:
			start = -r['n_days_running']

		sequence = [__add_to_date_as_str__(today(), x)[0:10] for x in range(start, until)]
		dates = r['dates']
		dates = [d[0:10] for d in dates]
		distances = r['distances']

		suma = 0
		for i in range(len(dates)): # If data were ordered, I could loop only the last m.
			if dates[i] in sequence:
				suma += distances[i]
		r[var_name] = suma
	return runners

def moving_average(runners, m=7, until=0):
	if until == 0 or until == None or until == "":
		until = today()


	for r in runners:
		maxcount = __count_days_between__(r['start_date'], today())
		if m > maxcount:
			m = maxcount

		sequence = [__add_to_date_as_str__(today(), -x)[0:10] for x in range(m, 0, -1)]

		dates = r['dates']
		dates = [d[0:10] for d in dates]
		distances = r['distances']

		suma = 0
		for i in range(len(dates)): # If data were ordered, I could loop only the last m.
			if dates[i] in sequence:
				suma += distances[i]

		#r['moving_average'] = suma/m
		r['moving_average'] = suma
	return runners

def fill_year_to_current(runners):
	for r in runners:
		r['year_series'] = __fill__(r['dates'], r['distances'], __first_day_of_cycle__(), today())
	return runners

def fill_year_to_end(runners):
	for r in runners:
		r['year_series_complete'] = __fill__(r['dates'], r['distances'], __first_day_of_cycle__(), __last_day_of_cycle__())
	return runners

def __fill__(dates, distances, start, end):
	n = (end-start).days
	sequence = [__add_to_date_as_str__(end, -x)[0:10] for x in range(n, 0, -1)]

	dates = [d[0:10] for d in dates]
	newdistances = []
	newdates = []

	for i in range(len(sequence)): # If data were ordered, I could loop only the last n.
		if not sequence[i] in dates:
			newdistances.append(0)
		else:
			index = dates.index(sequence[i])
			newdistances.append(distances[index])
		newdates.append(sequence[i])

	return newdistances

def fill_year_series(dates, distances):
	day_before_first = __add_to_date_as_str__(__str_to_date__(dates[0]), -1)
	last_record = __str_to_date__(dates[-1])
	today = date.today()

	y = []
	dates     = [day_before_first] + dates
	distances = [0] + distances

	# Fill with empty after last recorded date until (and including) yesterday.
	days_from_last = __days_from_someday_to_today__(last_record)
	for i in range(1, days_from_last):
		dates.append(__add_to_date_as_str__(today, i - days_from_last))
		distances.append(0)	

	# Fill dates with record and dates between records with 0.
	null_value = 0
	date_previous = __str_to_date__(dates[0])
	for i in range(0, len(dates)):
		day = dates[i]
		year, month, day = int(day[0:4]), int(day[5:7]), int(day[8:10])
		the_date = date(year, month, day)
		diff = int((the_date-date_previous).days)

		for ii in range(1, diff+1): # Fill every day with progress recorded.
			value = distances[i] if ii == diff else null_value # Fill with record or blank.
			y.append(value)

		date_previous = date(year, month, day)

	return y

def prepend(series, value, n):
	return [value for x in range(n)] + series

def __days_from_someday_to_today__(someday):
	today = date.today()
	return (today-someday).days

def str_to_date(day):
	return __str_to_date__(day)

def __str_to_date__(day):
	year, month, day = int(day[0:4]), int(day[5:7]), int(day[8:10])
	return date(year, month, day)

def add_to_date_as_str(daydate, days):
	return __add_to_date_as_str__(daydate, days)

def __add_to_date_as_str__(daydate, days):
	year   = daydate.year
	month  = daydate.month
	day    = daydate.day
	new_daydate = date(year, month, day) + timedelta(days=days)
	year   = new_daydate.year
	month  = new_daydate.month
	day    = new_daydate.day
	if month < 10:
		month = '0' + str(month)
	if day < 10:
		day = '0' + str(day)
	return (f'{year}-{month}-{day} 00:00:00')
	#return date(year, month, day)

def __add_day__(daydate, n):
	year   = daydate.year
	month  = daydate.month
	day    = daydate.day
	new_daydate = date(year, month, day) + timedelta(days=n)
	year   = new_daydate.year
	month  = new_daydate.month
	day    = new_daydate.day
	return date(year, month, day)	

def main():
	pass

if __name__ == '__main__':
	main()