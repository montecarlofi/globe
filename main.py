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
display.streamlit_hide(st.markdown)

#selected = option_menu(None, ["You", 'Everyone', 'Settings'], 
#        icons=['geo-fill', 'globe2', 'gear'], menu_icon="cast", default_index=0, orientation='horizontal')
#selected

main = st.container() #Map = st.empty()

with st.sidebar:
	# Menu
	lnk = "https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py"
	link = f'[Check this out]({lnk})'
	#st.write(link)
	names = [str(i).zfill(3)+' '+runners[i]['name'] for i in range(len(runners))]
	#links = 
	linknames = ['Everyone'] + names + ['Settings']
	runnerindex = list(range(len(names)))
	
	the_icons = ['globe'] + ['geo-fill' for x in range(len(runners))] + ['gear']

	selected2 = option_menu(None, linknames, 
	        icons=the_icons, menu_icon="cast", default_index=1)
	selected2

	try:
		choice = int(selected2[0:3])
		choice_flag = 'id'
	except Exception as e:
		choice = selected2
		choice_flag = 'name'

with main:
	st.title("Gaia Endurance") # La Terra # Endurance # Vigor, Vim # Dashing # Zooming

	if choice_flag == 'id':
		positions = display.get_position(runners[choice])
		positions = [positions[0]]
		zoom = 4
	elif choice == 'Everyone':
		positions = display.get_positions(runners)
		zoom = 0.44
	else:
		st.write(f"Ain't no settings.")

	#latitude, longitude = 0, -71.2450076 # Pacoa, Colombia.
	df = pd.DataFrame(positions, columns=['lat', 'lon'])
	st.map(df, zoom=zoom)

	if choice_flag == 'id':
		st.markdown("***")
		percent = runners[choice]['progress_year']/runners[choice]['remain_year']
		st.progress(percent)
		percent = round(percent*100, 2)
		st.text(f"Progress current year-cycle ({percent}%)")
		percent = runners[choice]['progress_total']/TOTAL
		st.progress(percent)
		percent = round(percent*100, 2)
		st.text(f"Progress total ({percent}%)")

wide = st.empty()

if choice_flag == 'id':
	col1, col2, col3 = st.columns((1, 1, 1))

	with col3:
		runner_name = runners[choice]['name']
		end_date = runners[choice]['end_date']
		end_year = int(end_date[0:4])
		#print(end_date); exit()
		gui_end_date = st.slider("End date "+runner_name, 2027, 2042, end_year, 1)	
		new_date = str(gui_end_date) + '-08-01'
		runners[choice]['end_date'] = new_date
		runners = process(runners)

	with col1:
		week_path_to_year = runners[choice]['week_path_to_year']
		last_seven = runners[choice]['last_seven']
		progress_year = runners[choice]['progress_year']

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
		value = str(last_seven)+' km'
		st.metric(title, value)
		#st.metric(title, value, updown)

	with col2:
		title = "Weekly target to current section"

		weekly_avg_before_last_seven = (progress_year-last_seven)/7
		updown = (last_seven/weekly_avg_before_last_seven) * 100
		updown = round(updown-100, 2)
		#updown = str(updown) + msg
		st.metric(title, round(week_path_to_year, 2))
		#st.success("<h2>HEI")



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

if choice_flag == 'id':
	with wide:
		rdata = display.make_graph_data(runners[choice])
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

