import sys
import time

file_name = sys.argv[1]
f = open(file_name, "r")
f1 = f.readlines()
number_of_elevators = int(f1[0])
number_of_floors = int(f1[1])
distance_between_floors = []
lift_access = []   
lift_level = []
look_lift = []
spf_lift = []
fcfs_lift = []
elevator_buffer = []
active_elevators = [] # boolean array, if its 1 then its active else its not
floor_heights_from_ground = []
request_params = []
global_timestamp = 0
j = 2

def reassignAlgorithms():
	it = 0
	global look_lift,spf_lift,fcfs_lift
	look_lift = []
	spf_lift = []
	fcfs_lift = []
	#print(len(active_elevators))
	for i in range(0,number_of_elevators):
		if active_elevators[i] == 1:
			if it%3 == 0:
				look_lift.append(i)
			elif it%3 == 1:
				fcfs_lift.append(i)
			elif it%3 == 2:
				spf_lift.append(i)
			it = it + 1	
	#print("len ", len(spf_lift))					
for i in range(1,number_of_floors):
	j = j+1
	x = f1[i+1]
	x = int(x)
	distance_between_floors.append(x)
floor_heights_from_ground.append(0)

for i in distance_between_floors:
	floor_heights_from_ground.append(i+floor_heights_from_ground[-1])

for i in range(j, j + number_of_elevators):
	x = f1[i]
	#print(x)
	lift_access.append(x.rstrip())
	lift_level.append(0)
	active_elevators.append(1)
#print("sdsdsd ",len(active_elevators))	
for i in range(0,number_of_elevators):
	elevator_buffer.append(set([]))
#print("sdsdsssd ",len(elevator_buffer))	
reassignAlgorithms()	
print("splift len ",len(spf_lift))
def add_request(source,destination):
	global request_params,global_timestamp
	request_params.append({"source":source,"destination":destination,"global_timestamp":global_timestamp})
def increment_timer():
	global global_timestamp,spf_lift,request_params,elevator_buffer
	#print(global_timestamp)
	global_timestamp = global_timestamp + 1
	for i in spf_lift:
		#print(i)
		if len(elevator_buffer[i]) == 0:
			dist = 100000
			for j in request_params:
				print(j["source"])

				#if(floor_heights_from_ground[lift_level[i]] - )	
def get_requests():
	print("Do you want to request give a request - y/n")
	ch = input()
	if ch=='y':
		source = int(input())
		destination = int(input())
		add_request(source,destination)
		print(request_params)
		increment_timer()
	#time.sleep(2)	
get_requests()



#print(request_params)
