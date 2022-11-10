#from running_setup import DATE_START, INFO_FILE
import pandas as pd

def get_runners(filename):
	info  = pd.read_csv(filename)
	IDs = list(info['id'])
	names = list(info['Name'])
	files = list(info['Filename'])
	start_dates = list(info['start_date'])
	end_dates   = list(info['end_date'])

	runners = {}
	for r in range(len(names)):
		runner_id = IDs[r]
		runner_name = names[r]
		runner_file = files[r]

		data = pd.read_csv(runner_file)
		dates       = list(data['Date'])
		distances   = list(data['Distance'])
		#dates, distances = __ensure_ascending__(dates, distances) # Just a simple reverse for now; no sorting.

		runner = {
			'name': runner_name,
			'distances': distances,
			'dates': dates,
			'start_date': start_dates[r],
			'end_date': end_dates[r],
			#'progress': None,
			#'path_to_target_total': None,
			#'path_to_target_year': None,
			'moving_average': None,
			'userinput': None
		}
		del data
		#runners.append(runner)
		runners[runner_id] = runner
	return runners

#def __ensure_ascending__(dates, distances):
#	first_item = __str_to_date__(dates[0])
#	last_item  = __str_to_date__(dates[-1])
#	if first_item > last_item:
#		dates.reverse()
#		distances.reverse()
#	del first_item, last_item
#	return dates, distances

#def str_to_date(day):
#	return __str_to_date__(day)

#def __str_to_date__(day):
#	year, month, day = int(day[0:4]), int(day[5:7]), int(day[8:10])
#	return date(year, month, day)