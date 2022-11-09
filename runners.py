#from datetime import date, timedelta
import daydate
from running_setup import TOTAL, DATE_START, n_days_year #, INFO_FILE
import pandas as pd
import numpy as np

def calc_progress(runners):
	#first_day_of_cycle = daydate.first_day_of_current_year_cycle()
	#n_days_in_cycle = count_days_between(first_day_of_cycle, today()) # days_gone_since(first_day_of_cycle())
	#n_left_in_cycle = n_days_year - n_days_in_cycle

	for r in runners:
		dates, distances = r['dates'], r['distances']
		start_date = daydate.str_to_date(r['start_date'])
		end_date   = daydate.str_to_date(r['end_date'])
		#print(f'start_date {start_date}\n')
		first_day_of_cycle = daydate.first_day_of_current_year_cycle(start_date)
		r['first_day_of_current_year_cycle'] = first_day_of_cycle
		last_day_of_cycle = daydate.last_day_of_current_year_cycle(start_date)
		r['last_day_of_current_year_cycle'] = last_day_of_cycle
		#start_date = r['start_date']
		#end_date   = r['end_date']
		#r['start_date'] = start_date
		#r['end_date']   = end_date
		progress_total  = __progress_since__(dates, distances, cutoff_date=start_date)
		progress_year   = __progress_since__(dates, distances, cutoff_date=first_day_of_cycle)
		n_years_left    = daydate.time_between(daydate.today(), end_date)/n_days_year
		#print (n_years_left)
		#__count_days_between__(daydate.today(), end_date)
		n_years_left    = n_years_left/n_days_year
		n_years         = round(daydate.time_between(start_date, end_date)/n_days_year) # Bad method.
		n_days_running  = daydate.time_between(start_date, daydate.today())
		n_days_in_cycle = daydate.time_between(first_day_of_cycle, daydate.today()) # Until, and including, yesterday.
		n_left_in_cycle = daydate.time_between(daydate.today(), daydate.add_days(last_day_of_cycle, 1)) # +1 since we've set the end date at the date before the start date.
		n_days_left     = daydate.time_between(daydate.today(), daydate.add_days(end_date, 1))
		r['n_left_in_cycle'] = n_left_in_cycle
		r['n_days_in_cycle'] = n_days_in_cycle
		r['n_days_running'] = n_days_running
		r['path_year_ideal'] = TOTAL / n_years / n_days_year
		r['progress_total'] = progress_total
		r['progress_year'] = progress_year
		r['remain_total'] = TOTAL - progress_total
		r['remain_year'] = (TOTAL/n_years) - progress_year
		r['yearly_remain'] = (TOTAL-progress_total) / n_years_left
		r['path_to_total'] = (TOTAL - progress_total) / n_days_left
		#r['path_to_year'] = ((TOTAL/n_years) - progress_year) / n_left_in_cycle
		r['week_path_to_year'] = (((TOTAL/n_years) - progress_year) / n_left_in_cycle) * 7
		r['average_math_weekly'] = (TOTAL/n_years/n_days_year) * 7
		r['average_math_daily'] = (TOTAL/n_years/n_days_year)
		r['last_seven'] = __sum_moving_sequence__(r, 'last_seven', -7, -0)
		r['ante_last_seven'] = __sum_moving_sequence__(r, 'ante_last_seven', -14, -7)

		latitude, longitude = 0, 0

		dx = r['progress_total']
		latitude, longitude = __get_coord__(latitude, longitude, -dx)
		r['latitude'], r['longitude'] = latitude, longitude

	return runners

def apply_cutoff(runners): # OK
	for runner in runners:
		#try:
		#	cutoff_date = __str_to_date__(runner['start_date'])
		#except Exception as e:
		#	cutoff_date = runner['start_date']
		cutoff_date = runner['start_date']
		#print(f'Cutoff_date {cutoff_date}\n')
		dates, distances = runner['dates'], runner['distances']
		dates, distances = __trim__(cutoff_date, dates, distances) # Cuts of data before start date.
		runner['dates'], runner['distances'] = dates, distances
	return runners

def __progress_since__(dates, distances, cutoff_date):
#	print(f'Prog since {dates} and {distances} for cutoff {cutoff_date}')
	cutoff_date = daydate.todate(cutoff_date) # strtodate?
	asum = 0
	for i in range(len(dates)):
		the_date = daydate.str_to_date(dates[i])
		#print(f'the_date {the_date} and for cutoff {cutoff_date}')
		asum = asum+distances[i] if the_date >= cutoff_date else asum
	return asum

def __trim__(cutoff_date, dates, distances):
	cutoff_date = daydate.todate(str(cutoff_date))
	newdates, newdistances = [], []
	index = 0
	for day in dates:
		year, month, day = int(day[0:4]), int(day[5:7]), int(day[8:10])
		some_date = daydate.todate(year, month, day)
		#print("some_date", some_date)
		#diff = (some_date - date_cutoff).days
		#print("Diff", diff)
		#if diff >= 0:
		if some_date >= cutoff_date:
			#print(f'some_date = {some_date}')
			newdates.append(dates[index])
			newdistances.append(distances[index])
		index += 1
	return newdates, newdistances

def sum_moving_sequence(*a, **k):
	return __sum_moving_sequence__(*a, **k)

def __sum_moving_sequence__(runners, var_name, fromm, until=0):
	try:
		_ = runners[0] # If runners is more than one,
		loop = len(runners) # do nothing.
	except Exception as e:
		runners = [runners]
		loop = 1

	for r in runners:
		start = fromm
		if start < -r['n_days_running']:
			start = -r['n_days_running']

		sequence = [daydate.add_days_as_str(daydate.today(), x)[0:10] for x in range(start, until)]
		dates = r['dates']
		dates = [d[0:10] for d in dates]
		distances = r['distances']

		suma = 0
		for i in range(len(dates)): # If data were ordered, I could loop only the last m.
			if dates[i] in sequence:
				suma += distances[i]
		r[var_name] = suma
	return runners

def fill_year_to_current(runners): # year_series_to_current
	for r in runners:
		#print("n_days_in_cycle", r['n_days_in_cycle'])
		r['year_series'] = __fill__(r['dates'], r['distances'], daydate.first_day_of_current_year_cycle(r['start_date']), daydate.today())
		#r['year_series'] = __fill__(r['dates'], r['distances'], -r['n_days_in_cycle'], 0)
		#print("- ndays", -r['n_days_in_cycle'])
	return runners

def fill_year_to_end(runners):
	for r in runners:
		start = daydate.first_day_of_current_year_cycle(r['start_date'])
		end = daydate.last_day_of_current_year_cycle(r['start_date'])
		end = daydate.add_days(end, 1)
		r['year_series_complete'] = __fill__(r['dates'], r['distances'], start, end)
	return runners

def __fill__(dates, distances, start, end):
	#end = daydate.todate(end)
	#print(f'dates{dates} \ndistances {distances} \n start {start} \n end {end}')
	
	n = daydate.time_between(end, start, timeunit='days')
	#m = daydate.time_between(start, daydate.today(), timeunit='days')
	#print("start", start, "end", end, " = ", -start+end)
	#n = (end-start).days
	#print("nnnnn", n, m)
	#o = daydate.add_days_as_str(end, n)[0:10]
	#print(o)

	sequence = [daydate.add_days_as_str(end, x)[0:10] for x in range(n, 0)]
	#sequence = [__add_to_date_as_str__(end, -x)[0:10] for x in range(n, 0, -1)]
	#print(sequence)
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

def __get_coord__(current_lat, current_long, dx):
	p = 180/np.pi	
	r_earth = 6378.137
	dy, dx = 0, dx
	new_latitude  = current_lat + (dy / r_earth) * p
	new_longitude = current_long + (dx / r_earth) * p / np.cos(current_lat * p)
	return new_latitude, new_longitude

def main():
	print("before")
	#print(daydate.__str_to_date__("2001-03-03"))
	#d = daydate.today()
	print(daydate.today())

	print(__get_coord__(0, -71.2450076, -300))

if __name__ == '__main__':
	main()
