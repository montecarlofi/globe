import streamlit as st; #st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
#import leafmap.foliumap as leafmap
import altair as alt
from itertools import accumulate
import run_get_data as get_data
import runners as runnrs
import display
#from run_processing import TOTAL
import numpy as np 
import pandas as pd 

# Does not work with more than one record per day... I think.
# (Haven't implemented time comparison; only date.)

# Setup:
INFO_FILE, TOTAL, n_days_year = 'runners.csv', 40075, 365 #START = '2020-08-02'

# Get data.
runners = get_data.get_runners(INFO_FILE) # name, distances, dates, start, end

# Process data.
def process(runners):
	runners = runnrs.apply_cutoff(runners)
	runners = runnrs.calc_progress(runners)
	#runners = ascending(runners, column='dates')
	#runners = fill_past_blank_days_with_zero(runners) # Un until today.
	#runners = moving_average(runners, 7) # Gives average across period; not for units within.
	#runners = ante_last_seven(runners) # Gives average across period; not for units within.
	runners = runnrs.fill_year_to_current(runners) # Creates sequence with 0 for blank days.
	runners = runnrs.fill_year_to_end(runners)
	runners = runnrs.sum_moving_sequence(runners, 'last_seven', -7, -0)
	runners = runnrs.sum_moving_sequence(runners, 'ante_last_seven', -14, -7)
	return runners
runners = process(runners)


# Display interactive.
s = accumulate(runners[0]['year_series'])
distances0 = runners[0]['year_series']
distances1 = runners[1]['year_series']
seq0 = list(accumulate(runners[0]['year_series']))
seq1 = list(accumulate(runners[1]['year_series']))
ideal0 = list(accumulate([runners[0]['path_year_ideal'] for x in range(len(seq0))]))
ideal1 = list(accumulate([runners[1]['path_year_ideal'] for x in range(len(seq1))]))

display.streamlit_hide(st.markdown)

selected = option_menu(None, ["You", 'Everyone', 'Settings'], 
        icons=['geo-fill', 'globe2', 'gear'], menu_icon="cast", default_index=0, orientation='horizontal')
selected

main = st.container() #Map = st.empty()

with st.sidebar:
	pass


with main:
	st.title("Gaia Endurance") # La Terra # Endurance # Vigor, Vim # Dashing # Zooming

	if selected == 'You':
		positions = display.get_positions(runners)
		positions = [positions[1]]
		zoom = 4

	if selected == 'Everyone':
		positions = display.get_positions(runners)
		zoom = 1

	#latitude, longitude = 0, -71.2450076 # Pacoa, Colombia.
	df = pd.DataFrame(positions, columns=['lat', 'lon'])
	st.map(df, zoom=zoom)
	st.markdown("***")

	if selected == 'You':
		st.progress(runners[1]['progress_year']/runners[1]['remain_year'])
		st.text("Progress current year-cycle")
		st.progress(runners[1]['progress_total']/TOTAL)
		st.text("Progress total")

wide = st.empty()

if selected == 'You':
	col1, col2, col3 = st.columns((1, 1, 1))

	with col3:
		gui_end_date = st.slider("End date Per", 2027, 2042, 2037, 1)	
		new_date = str(gui_end_date) + '-08-01'
		runners[1]['end_date'] = new_date
		runners = process(runners)

	with col1:
		week_path_to_year = runners[1]['week_path_to_year']
		last_seven = runners[1]['last_seven']
		progress_year = runners[1]['progress_year']

		title = "Last 7 days:"
		updown = (last_seven/week_path_to_year) * 100
		updown = round(updown-100, 2)
		if updown > 0:
			msg = '% above weekly target'
		elif updown < 0:
			msg = '% below weekly target'
		else:
			msg = 'right at weekly target'
		if last_seven == 0:
			msg = ' Far below target!'
			#updown = -0
		updown = str(updown) + msg
		week_path_to_year = round(week_path_to_year, 2)
		st.metric(title, str(last_seven)+' km', updown)

	with col2:
		title = "Weekly target to current section"

		weekly_avg_before_last_seven = (progress_year-last_seven)/7
		updown = (last_seven/weekly_avg_before_last_seven) * 100
		updown = round(updown-100, 2)
		#updown = str(updown) + msg
		st.metric(title, round(week_path_to_year, 2), updown)



	#st.title("Gaia Endurance") # La Terra # Endurance # Vigor, Vim # Dashing # Zooming
	#gui_end_date = st.slider("End date Per", 2032, 2037, 2037, 1)
	#new_date = str(gui_end_date) + '-08-01'
	#runners[1]['end_date'] = new_date
	#runners = process(runners)
	#st.markdown("***")
	#gui_end_date = st.slider("End date Mikal", 2032, 2037, 2032, 1)
	#new_date = str(gui_end_date) + '-08-01'
	#runners[0]['end_date'] = new_date
	#runners = process(runners)
	#selected = option_menu("Menu", ["You", 'Others', 'Settings'], 
	#        icons=['geo-fill', 'globe2', 'gear'], menu_icon="cast", default_index=0)
	#selected

	#if selected == 'Others':
	#	display.others(st)

	#if selected == 'You':
	#	pass

if selected == 'You':
	with wide:
		rdata = display.make_graph_data(runners[1])
		df = pd.DataFrame(
		    rdata,
		    columns=['name', 'day', 'distance_acc', 'distance_day', 'average_math_daily'])

		chart = alt.Chart(df).mark_circle().encode(
		    x='day', 
		    y='distance_acc', 
		    size='distance_day', 
		    color='name', 
		    tooltip=['day', 'distance_day'])

		st.markdown("***")
		st.altair_chart(chart, use_container_width=True)	

