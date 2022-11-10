from itertools import accumulate
from running_setup import TOTAL

def make_like_sql_table(runners):
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
				'latitude': r['latitude'],
				'longitude': r['longitude']
			}
			rdata.append(data)

			ideal_data = {
				'name': r['name'] + ' benchmark',
				'day': i,
				'distance_acc': benchmark[i],
				'distance_day': ideal,
			}
			rdata.append(ideal_data)
	return rdata

def make_graph_data(r):
	rdata = []
	seq = list(accumulate(r['year_series']))

	ideal = r['average_math_daily']
	benchmark = list(accumulate([ideal for x in range(len(seq))]))

	for i in range(len(seq)):
		data = {
			'name': r['name'],
			'day': i,
			'distance_acc': seq[i],
			'distance_day': r['year_series'][i],
			'latitude': r['latitude'],
			'longitude': r['longitude']
		}
		rdata.append(data)

		ideal_data = {
			'name': r['name'] + ' benchmark',
			'day': i,
			'distance_acc': benchmark[i],
			'distance_day': ideal,
		}
		rdata.append(ideal_data)
	return rdata

def get_position(r):
	positions = []
	xy = [r['latitude'], r['longitude']]
	positions.append(xy)
	return positions

def get_positions(runners):
	positions = []
	for ID in runners:
		xy = [runners[ID]['latitude'], runners[ID]['longitude']]
		positions.append(xy)
	return positions

def streamlit_hide(markdown):
	hide_streamlit_style = """
	            <style>
	            #MainMenu {visibility: hidden;}
	            footer {visibility: hidden;}
	            </style>
	            """
	markdown(hide_streamlit_style, unsafe_allow_html=True) 

	markdown("""
	<style>
	div[data-testid="metric-container"] {
	   background-color: rgba(240, 242, 246, 0.7);
	   border: 1px solid rgba(240, 242, 246, 0.7);
	   padding: 10% 10% 10% 10%;
	   border-radius: 5px;
	   color: rgb(30, 103, 119);
	   overflow-wrap: break-word;
	}

	/* breakline for metric text         */
	div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
	   overflow-wrap: break-word;
	   white-space: break-spaces;
	   color: black;
	}
	</style>
	"""
	, unsafe_allow_html=True)

	#st.metric(label="This is a very very very very very long sentence", value="70 °F")

def progress_bar_all(runners, st_progress, st_text):
	names = []
	pees = []
	for ID in runners:
		name = runners[ID]['name']
		progress = runners[ID]['progress_total']/TOTAL
		percent = round(progress * 100, 0)
		st_progress(progress)
		st_text(f"{name} — progress total ({percent}%)")


def others(st):
	st.write("HHHHHHHHHHHHHHH")