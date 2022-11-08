# Does not work with more than one record per day... I think (haven't implemented time comparison; only date).
import streamlit as st; st.set_page_config(layout="wide")
import altair as alt
#import pandas as pd
import matplotlib.pyplot as plt
#from datetime import date, timedelta
from itertools import accumulate
#from running_setup import INFO_FILE, TOTAL, n_days_year #weekly_math, n_days_year, daily_math, days_gone, yearly_math, Y_YEAR, X_YEAR, weeks_left, TOTAL
import run_get_data as get_data
from run_processing import *

# Setup:
INFO_FILE, TOTAL, n_days_year = 'runners.csv', 40075, 365
#START = '2020-08-02'

# Get data.
runners = get_data.get_runners(INFO_FILE) # name, distances, dates, start, end

# Process data.
def process(runners):
	runners = apply_cutoff(runners)
	runners = calc_progress(runners)
	#runners = ascending(runners, column='dates')
	#runners = fill_past_blank_days_with_zero(runners) # Un until today.
	#runners = moving_average(runners, 7) # Gives average across period; not for units within.
	#runners = ante_last_seven(runners) # Gives average across period; not for units within.
	runners = fill_year_to_current(runners) # Creates sequence with 0 for blank days.
	runners = fill_year_to_end(runners)
	runners = sum_moving_sequence(runners, 'last_seven', -7, -0)
	runners = sum_moving_sequence(runners, 'ante_last_seven', -14, -7)
	return runners
runners = process(runners)
#runners = process(runners)


#for r in runners:
#	r['sum_moving_sequence'] = sum_moving_sequence(r, -14, -7)
#runners = sum_moving_sequence(runners, -7, -0)
#[r['sum_moving_sequence'] := sum_moving_sequence(r, -14, -7) for r in runners]

#name = 'last_seven'; [print(f'{name}: {r[name]}') for r in runners]

# Get user input.

# Display data.
s = accumulate(runners[0]['year_series'])
ditances0 = runners[0]['year_series']
ditances1 = runners[1]['year_series']
seq0 = list(accumulate(runners[0]['year_series']))
seq1 = list(accumulate(runners[1]['year_series']))
ideal0 = list(accumulate([runners[0]['path_year_ideal'] for x in range(len(seq0))]))
ideal1 = list(accumulate([runners[1]['path_year_ideal'] for x in range(len(seq1))]))



left1, left2, wide = st.columns((1, 1, 5))

a, b = [1, 2, 3], [1, 2, 3]
for i in a, b:
	#print("i", i)
	pass

import numpy as np 
import pandas as pd 

r_earth = 6371 # From different models (Wikipedia).
r_earth = 6378.137 # Equator.
p = 180/np.pi

with left1:
	r = runners[1]
	percent = r['progress_total']/TOTAL
	percent = percent * 100
	percent = round(percent, 2)
	name_percent = r['name'] + ': ' + str(percent) + "%"
	progress_year = str(round(r['progress_year'])) + " km"
	last_seven = r['last_seven']
	diff = last_seven - r['average_math_weekly']
	#st.metric(name_percent, last_seven, diff)
	#st.progress(r['progress_total']/TOTAL)

	latitude, longitude = 0, -71.2450076 # Pacoa, Colombia.
	dy, dx = 0, -r['progress_total']
	new_latitude  = latitude  + (dy / r_earth) * p
	new_longitude = longitude + (dx / r_earth) * p / np.cos(latitude * p)

	point = np.ones([1,1])
	df = pd.DataFrame(
    	point / [50, 50] + [new_latitude, new_longitude],
    	columns=['lat', 'lon'])

	#st.map(df, zoom=3)

with left2:
	st.metric('1', '2', '3')
	st.markdown("***")
	gui_end_date = st.slider("End date", 2032, 2037, 2032, 1)
	new_date = str(gui_end_date) + '-08-01'
	print(new_date)

	#runners[0]['end_date'] = "2040-01-01"
	for r in runners:
		r['end_date'] = new_date
	runners = process(runners)
	print(daydate(gui_end_date, 8, 1))


	r = runners[0]

	percent = r['progress_total']/TOTAL
	percent = percent * 100
	percent = round(percent, 2)
	title = r['name'] + ', last seven days:'
	name_percent = r['name'] + ': ' + str(percent) + "%"
	progress_year = str(round(r['progress_year'])) + " km"
	#moving_average = r['moving_average']
	#st.metric(name_percent, progress_year, diff_avgs)
	to_week = last_seven - r['average_math_weekly']
	to_week = round(to_week)

	last_seven = r['last_seven']
	ante_last_seven = round(r['ante_last_seven'],2)
	diff = last_seven - ante_last_seven
	math_weekly = r['average_math_weekly']

	small = round((last_seven/ante_last_seven)*100 - 100, 2)
	small = str(small) + '% from week before'

	small = round((last_seven/math_weekly)*100 - 100, 2)
	small = str(small) + '% from ideal'

	big = str(last_seven) + '(' + str(round(math_weekly,2)) + ')'
	#st.metric(title, big, small)

	#st.metric(name_percent, last_seven, to_week)
	#st.progress(r['progress_total']/TOTAL)

	# Apple health

	#user = st.slider("km", 0, TOTAL, 0, 1)

	circumference_at_latitude = 2*np.pi*r_earth*(np.cos(latitude)) # circumference_at_latitude = TOTAL*np.cos(latitude)
	#print("circumference_at_latitude", circumference_at_latitude)
	multiplier = TOTAL/circumference_at_latitude
	#360/multiplier

	adjustment = 122.11365439095317 - 3.7343
	#st.title("Around the world")
	# 40.4355° N, 31.1186° E # Ormanpinari
	circ_at_madrid = 36547.726550852494
	latitude, longitude = 40.4168, -3.7038 # Madrid
	latitude, longitude = 40.4180, -3.7143 # Palacio Real, Madrid: Circ = 36547.726550852494. Total - circ = 3527.289686
	latitude, longitude = 40.3980, -3.7343 + adjustment # Palacio Real, adjusted for openmaps.
	latitude, longitude = 0, -71.2450076 # Pacoa, Colombia.

	dy, dx = 0, -runners[0]['progress_total'] # user
	#dx = 0
	new_latitude  = latitude  + (dy / r_earth) * p
	new_longitude = longitude + (dx / r_earth) * p / np.cos(latitude * p)

	#print(np.random.randn(10, 2))

	point = np.ones([1,1])
	df = pd.DataFrame(
    	point / [50, 50] + [new_latitude, new_longitude],
    	columns=['lat', 'lon'])

	#st.map(df, zoom=3)

	with wide:
		st.title("Around the world")
		chart = {
			'P': seq1,
			'P-target': ideal1,
			'M': seq0,
			'M-target': ideal0
		}
		#chart = [[1, 2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7]]
		#st.line_chart(chart, height=600)


days0 = list(range(len(seq0)))
days1 = list(range(len(seq1)))
colour = [10 for x in range(len(seq0))]
name0 = ['M' for x in range(len(seq0))]
name1 = ['P' for x in range(len(seq0))]

rdata = []
for r in runners:
	seq = list(accumulate(r['year_series']))

	ideal = r['average_math_daily']
	benchmark = list(accumulate([ideal for x in range(len(seq))]))

	for i in range(len(seq)):
		data = {
			'name': r['name'],
			'day': i,
			'distance_acc': seq[i],
			'distance_day': r['year_series'][i],
		}
		rdata.append(data)

		ideal_data = {
			'name': r['name'] + ' benchmark',
			'day': i,
			'distance_acc': benchmark[i],
			'distance_day': ideal,
		}
		rdata.append(ideal_data)

df = pd.DataFrame(
    rdata,
    columns=['name', 'day', 'distance_acc', 'distance_day', 'average_math_daily'])

chart = alt.Chart(df).mark_circle().encode(
    x='day', 
    y='distance_acc', 
    size='distance_day', 
    color='name', 
    tooltip=['day', 'distance_day'])

with wide:
	st.altair_chart(chart, use_container_width=True)