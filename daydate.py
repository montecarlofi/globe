# daydate
#
# Mikal Rian 2022
#
#

from datetime import date, timedelta, datetime
#import datetime

def first_day_of_current_year_cycle(start_date, current=date.today()):
	D = __str_to_date__(start_date)
	start_month = D.month
	start_day   = D.day
	current = __str_to_date__(current)
	if (current-D).days < 0:
		raise ValueError("You can't have a 'current' date before the start date!")
	y = current.year
	m = current.month
	d = current.day

	if m > start_month: # We're in the same year.
		the_year = y
	elif m < start_month:
		the_year = y - 1
	elif m == start_month and d < start_day:
		the_year = y - 1
	elif m == start_month and d >= start_day:
		the_year = y

	return date(the_year, start_month, start_day)

def last_day_of_current_year_cycle(start_date, current=date.today()):
	D = __str_to_date__(start_date)
	start_month = D.month
	start_day   = D.day
	current = __str_to_date__(current)
	if (current-D).days < 0:
		raise ValueError("You can't have a 'last' date before the start date!")
	y = current.year
	m = current.month
	d = current.day

	if m > start_month:
		the_year = y + 1
	elif m < start_month:
		the_year = y
	elif m == start_month and d < start_day:
		the_year = y
	elif m == start_month and d >= start_day:
		the_year = y + 1

	return date(the_year, start_month, start_day-1)

def today():
	return datetime.today()

def todate(*a):
	if len(a) == 1:
		return __str_to_date__(a[0])
	elif len(a) == 3:
		return date(a[0], a[1], a[2])

def todatetime(string): ######################·······
	print(f'You passed {string}')

def str_to_date(day):
	return __str_to_date__(day)

def time_between(start, end, timeunit='days'):
	if timeunit == 'days':
		start = __str_to_date__(start)
		end   = __str_to_date__(end)
		gone = (end-start).days
	return gone

def add_days(initial, n_beforeorafter): # Initial is str or date.
	initial = __str_to_date__(initial)
	other = initial + timedelta(days=n_beforeorafter)
	return other

def add_days_as_str(initial, n):
	initial = __str_to_date__(initial)
	other = initial + timedelta(days=n)
	y = other.year
	m = other.month
	d = other.day
	m = '0' + str(m) if m < 10 else str(m)
	d = '0' + str(d) if d < 10 else str(d)
	y = str(y)
	o = y + '-' + m + '-' + d + ' 00:00:00'
	return o
	
def days_from_someday_to_today(someday):
	someday = __str_to_date__(someday)
	today = date.today()
	return (today-someday).days


# Internal functions.
def __str_to_date__(day):
	#exit()
	if isinstance(day, str):
		y = int(str(day)[0:4])
		m = int(str(day)[5:7])
		d = int(str(day)[8:10])
		#D = date(y, m, d)
	#elif isinstance(day, datetime.date):
	elif type(day) == "<class 'datetime.date'>": # Doesn'w work.
		#print("You to the correct type", type(day))
		#D = day
		y = day.year
		m = day.month
		d = day.day
	else:
		#print("You came here", type(day))
		#D = day
		y = day.year
		m = day.month
		d = day.day
	D = date(y, m, d)
	return D


def main():
	d = "2022-09-03"
	#d = date(2022, 2, 2)
	print(first_day_of_current_year_cycle(d, "2024-09-30"))
	#print(today())
	print(todate(1, 2, 3))
	print(add_days(today(), 900))
	print(add_days_as_str(today(), -333))

	d = datetime(2000, 12, 1, 15, 15, 36)
	print(d)

	mr = "1978-02-11"
	print(days_from_someday_to_today(mr))

if __name__ == '__main__':
	main()