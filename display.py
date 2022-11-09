from itertools import accumulate

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

def get_positions(runners):
	positions = []
	for r in runners:
		xy = [r['latitude'], r['longitude']]
		positions.append(xy)
	return positions

	positions = []
	xy = [1, 2]
	positions.append(xy)
	xy = [31, 2]
	positions.append(xy)
	xy = [10, 2]
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

def others(st):
	st.write("HHHHHHHHHHHHHHH")