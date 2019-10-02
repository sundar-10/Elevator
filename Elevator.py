from argparse import ArgumentParser
import pprint

global_variables = {
	"timestamp" : 0,
	"requests_incoming" : 0,
	"floor_heights" : [],
	"elevators" : [],
	"algorithms" : {
		"look_lift" : set([]),
		"spf_lift" : set([]),
		"fcfs_lift" : set([])
	},
	"requests" : []
}

def main():
	readInput()
	assignAlgorithms()
	executeLoop()

def orientedDirection(source,destination):
	if source < destination:
		return 1
	elif source > destination:
		return -1
	else:
		return 0

def readInput():
	global global_variables
	parser = ArgumentParser()
	parser.add_argument("-f","--file",required=True)
	args = parser.parse_args()
	file_name = args.file
	f = open(file_name,"r")
	file_contents = f.readlines()
	number_of_elevators = int(file_contents[0].split()[0])
	number_of_floors = int(file_contents[0].split()[1])
	separation_floors = [int(i) for i in file_contents[1].split()]
	global_variables['floor_heights'].append(0)
	for i in separation_floors:
		global_variables['floor_heights'].append(i + global_variables['floor_heights'][-1])
	for i in range(2,number_of_elevators + 2):
		global_variables['elevators'].append(
			{
				"current_height" : 0,
				"accessible_levels" : file_contents[i],
				"working_state" : True,
				"to_visit" : []
			})
	data = []
	data.append(number_of_elevators)
	data.append(number_of_floors)
	return str(data)	

def assignAlgorithms():
	global global_variables
	it = 0
	for i in range(0,len(global_variables['elevators'])):
		if global_variables['elevators'][i]['working_state']:
			if it%2 == 0:
				global_variables['algorithms']['look_lift'].add(i)
				global_variables['elevators'][i]['following_algorithm'] = "LOOK"
			elif it%2 == 1:
				global_variables['algorithms']['spf_lift'].add(i)
				global_variables['elevators'][i]['following_algorithm'] = "SPF"
			it = it + 1

def incrementTimer():
	global global_variables
	global_variables['timestamp'] = global_variables['timestamp'] + 1
	# Assigning request to elevators
	#SPF
	for i in range(0,len(global_variables['requests'])):
		cur_req = global_variables['requests'][i]
		if cur_req['assigned_elevator'] == -1:
			s = cur_req['source']
			d = cur_req['destination']
			elevator_index = -1
			min_dist = 1000000
			# SPF
			for e in global_variables['algorithms']['spf_lift']:
				cur_elevator = global_variables['elevators'][e]
				if cur_elevator['accessible_levels'][s] !='1' or cur_elevator['accessible_levels'][d] != '1' or (not cur_elevator['working_state']):
					continue
				if len(cur_elevator['to_visit']) == 0:
					if abs(cur_elevator['current_height'] - global_variables['floor_heights'][s]) < min_dist:
						elevator_index = e
						min_dist = abs(cur_elevator['current_height'] - global_variables['floor_heights'][s])
			if elevator_index != -1:
				global_variables['elevators'][elevator_index]['to_visit'].append(i)
				global_variables['requests'][i]['assigned_elevator'] = elevator_index
				continue
			min_dist = 1000000

			# LOOK
			for e in global_variables['algorithms']['look_lift']:
				cur_elevator = global_variables['elevators'][e]
				if cur_elevator['accessible_levels'][s] !='1' or cur_elevator['accessible_levels'][d] != '1' or (not cur_elevator['working_state']):
					continue
				if len(cur_elevator['to_visit']) == 0:
					if abs(cur_elevator['current_height'] - global_variables['floor_heights'][s]) < min_dist:
						elevator_index = e
						min_dist = abs(cur_elevator['current_height'] - global_variables['floor_heights'][s])
			if elevator_index != -1:
				global_variables['elevators'][elevator_index]['to_visit'].append(i)
				global_variables['requests'][i]['assigned_elevator'] = elevator_index
				continue
				
	# Incrementing elevator positions
	# SPF
	for i in global_variables['algorithms']['spf_lift']:
		elevator_pos = global_variables['elevators'][i]['current_height']
		if len(global_variables['elevators'][i]['to_visit']) == 0:
			continue
		# Accept New Requests
		for r in range(0, len(global_variables['requests'])):
			if global_variables['requests'][r]['assigned_elevator'] != -1:
				continue
			new_req_source = global_variables['requests'][r]['source']
			new_req_destination = global_variables['requests'][r]['destination']
			new_req_source = global_variables['floor_heights'][new_req_source]
			new_req_destination = global_variables['floor_heights'][new_req_destination]
			prim_req_id = global_variables['elevators'][i]['to_visit'][0]
			prim_dest = global_variables['requests'][prim_req_id]['destination']
			prim_dest = global_variables['floor_heights'][prim_dest]
			prim_sour = global_variables['requests'][prim_req_id]['source']
			prim_sour = global_variables['floor_heights'][prim_sour]
			new_req_orientation = orientedDirection(new_req_source, new_req_destination)
			if global_variables['requests'][prim_req_id]['service_state'] == 1:
				ele_orientation = orientedDirection(elevator_pos, prim_dest)
				sat_range = [i for i in range(min(elevator_pos,prim_dest),max(elevator_pos,prim_dest) + 1)]
				if ele_orientation == new_req_orientation and new_req_source in sat_range and new_req_destination in sat_range:
					global_variables['requests'][r]['assigned_elevator'] = i
					global_variables['elevators'][i]['to_visit'].append(r)
			elif global_variables['requests'][prim_req_id]['service_state'] == 0:
				ele_to_source = [i for i in range(min(elevator_pos,prim_sour),max(elevator_pos,prim_dest) + 1)]
				source_to_dest = [i for i in range(min(prim_sour,prim_dest),max(prim_sour,prim_dest) + 1)]
				ele_to_source_orien = orientedDirection(elevator_pos, prim_sour)
				source_to_dest_orien = orientedDirection(prim_sour, prim_dest)
				if ele_to_source_orien == new_req_orientation and new_req_source in ele_to_source and new_req_destination in ele_to_source:
					global_variables['requests'][r]['assigned_elevator'] = i
					global_variables['elevators'][i]['to_visit'].append(r)
				elif new_req_source in ele_to_source and new_req_destination in source_to_dest:
					global_variables['requests'][r]['assigned_elevator'] = i
					global_variables['elevators'][i]['to_visit'].append(r)
				elif source_to_dest_orien == new_req_orientation and new_req_source in source_to_dest and new_req_destination in source_to_dest:
					global_variables['requests'][r]['assigned_elevator'] = i
					global_variables['elevators'][i]['to_visit'].append(r)	
		# Move Elevator
		req_index = global_variables['elevators'][i]['to_visit'][0]
		print("req_ index ", req_index)
		to_move = 0
		source = global_variables['requests'][req_index]['source']
		destination = global_variables['requests'][req_index]['destination']
		if global_variables['requests'][req_index]['service_state'] == 0:
			to_move = orientedDirection(elevator_pos, global_variables['floor_heights'][source])
		elif global_variables['requests'][req_index]['service_state'] == 1:
			to_move = orientedDirection(elevator_pos, global_variables['floor_heights'][destination])
		else:
			print("SOMETHING SCREWED UP")
		global_variables['elevators'][i]['current_height'] = global_variables['elevators'][i]['current_height'] + to_move
		
		# Resolve Requests
		for r in range(len(global_variables['elevators'][i]['to_visit'])-1,-1,-1):
			req_id = global_variables['elevators'][i]['to_visit'][r]
			req_service_state = global_variables['requests'][req_id]['service_state']
			req_source = global_variables['requests'][req_id]['source']
			req_destination = global_variables['requests'][req_id]['destination']
			if req_service_state == 0:
				if global_variables['elevators'][i]['current_height'] == global_variables['floor_heights'][req_source]:
					global_variables['requests'][req_id]['service_state'] = 1
			elif req_service_state == 1:
				if global_variables['elevators'][i]['current_height'] == global_variables['floor_heights'][req_destination]:
					global_variables['elevators'][i]['to_visit'].remove(req_id)
					# del global_variables['requests'][req_id]

	# LOOK
	for i in global_variables['algorithms']['look_lift']:
		elevator_pos = global_variables['elevators'][i]['current_height']
		if len(global_variables['elevators'][i]['to_visit']) == 0:
			continue
		# Accept New Requests
		for r in range(0, len(global_variables['requests'])):
			if global_variables['requests'][r]['assigned_elevator'] != -1:
				continue
			new_req_source = global_variables['requests'][r]['source']
			new_req_destination = global_variables['requests'][r]['destination']
			new_req_source = global_variables['floor_heights'][new_req_source]
			new_req_destination = global_variables['floor_heights'][new_req_destination]
			new_req_orientation = orientedDirection(new_req_source, new_req_destination)
			prim_req_id = global_variables['elevators'][i]['to_visit'][0]
			prim_dest = global_variables['requests'][prim_req_id]['destination']
			prim_dest = global_variables['floor_heights'][prim_dest]
			prim_sour = global_variables['requests'][prim_req_id]['source']
			prim_sour = global_variables['floor_heights'][prim_sour]
			prim_orien = orientedDirection(elevator_pos,prim_dest)
			if new_req_orientation == prim_orien:
				if prim_orien > 0 and new_req_source >=  elevator_pos:
					global_variables['elevators'][i]['to_visit'].append(r)
					global_variables['requests'][r]['assigned_elevator'] = i
					continue
				elif prim_orien < 0 and new_req_source <= elevator_pos:
					global_variables['elevators'][i]['to_visit'].append(r)
					global_variables['requests'][r]['assigned_elevator'] = i
					continue

		# Move Elevator
		req_index = global_variables['elevators'][i]['to_visit'][0]
		print("req_ index ", req_index)
		to_move = 0
		source = global_variables['requests'][req_index]['source']
		destination = global_variables['requests'][req_index]['destination']
		if global_variables['requests'][req_index]['service_state'] == 0:
			to_move = orientedDirection(elevator_pos, global_variables['floor_heights'][source])
		elif global_variables['requests'][req_index]['service_state'] == 1:
			to_move = orientedDirection(elevator_pos, global_variables['floor_heights'][destination])
		else:
			print("SOMETHING SCREWED UP")
		global_variables['elevators'][i]['current_height'] = global_variables['elevators'][i]['current_height'] + to_move
		
		# Resolve Requests
		for r in range(len(global_variables['elevators'][i]['to_visit'])-1,-1,-1):
			req_id = global_variables['elevators'][i]['to_visit'][r]
			req_service_state = global_variables['requests'][req_id]['service_state']
			req_source = global_variables['requests'][req_id]['source']
			req_destination = global_variables['requests'][req_id]['destination']
			if req_service_state == 0:
				if global_variables['elevators'][i]['current_height'] == global_variables['floor_heights'][req_source]:
					global_variables['requests'][req_id]['service_state'] = 1
			elif req_service_state == 1:
				if global_variables['elevators'][i]['current_height'] == global_variables['floor_heights'][req_destination]:
					global_variables['elevators'][i]['to_visit'].remove(req_id)
					# del global_variables['requests'][req_id]
 	

def addRequest(source,destination):
	global global_variables
	global_variables['requests'].append(
		{
			"request_id" : global_variables['requests_incoming'],
			"source" : source,
			"destination" : destination,
			"creation_timestamp" : global_variables['timestamp'],
			"assigned_elevator" : -1,
			"service_state" : 0
		})
	global_variables['requests_incoming'] = global_variables['requests_incoming'] + 1

def abortElevator(elevator_index):
	global global_variables
	global_variables['elevators'][elevator_index]['working_state'] = False
	nearest_floor = 0
	while global_variables['floor_heights'][nearest_floor] < global_variables['elevators'][elevator_index]['current_height']:
		nearest_floor = nearest_floor + 1
	nearest_floor = nearest_floor - 1
	for r in global_variables['elevators'][elevator_index]['to_visit']:
		global_variables['requests'][r]['source'] = nearest_floor
		global_variables['requests'][r]['assigned_elevator'] = -1
	global_variables['elevators'][elevator_index]['to_visit'] = []
	assignAlgorithms()

# Command Line specific function
def executeLoop():
	global global_variables
	while True:
		incrementTimer()
		ch = input("Do you want to give a request?[0/1/2]")

		if ch == '1':
			source = int(input())
			destination = int(input())
			addRequest(source,destination)
		elif ch=='2':
			ele = int(input())
			abortElevator(ele)
		pretty_print = pprint.PrettyPrinter(indent=4)
		pretty_print.pprint(global_variables)
def printt():
	global global_variables
	pretty_print = pprint.PrettyPrinter(indent=4)
	pretty_print.pprint(global_variables)		

if __name__ == "__main__":
	main()