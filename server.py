from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread
import time

clients = {}
addresses= {}
times = []
threads = []

HOST =''
PORT = 33002
BUFFERSIZE=1024
CLIENT_NO = 1
ADDR=(HOST,PORT)
SERVER=socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

all_times = []

def accept_in_connections():

	while len(clients) < CLIENT_NO:
		client,client_addr=SERVER.accept()
		print("%s:%s has joined fellows."%client_addr)
		client.send(bytes("greetings from ritzz!"+"now enter your name and press enter","utf8"))
		addresses[client]=client_addr
		clients[client]="ritz"
		thr = Thread(target=handle_client,args=(client,))
		threads.append(thr)
		thr.start()
		time.sleep(1)


	for t in threads:
		t.join()

	print("test")

def handle_client(client):

	name=client.recv(BUFFERSIZE).decode("utf8")
	welcome='Welcome %s! If you want to quit,you hit {quit} to exit.' %name
	client.send(bytes(welcome,"utf8"))
	msg='%s has joined the chat XD' %name
	print(welcome, msg)
	
	print("Waiting for more users to join")
	while (len(clients) != CLIENT_NO):
		pass
	start_game(client,name)

def start_game(client,name):
	
	q_file = open("question.csv", "r")
	line = q_file.readline()
	line = q_file.readline()
	tot_time = 0

	while(line != ''):

		client.send(bytes(line[0:-2],"utf8"))
		print(len(line))
		if line=="END_OF_QUIZ__" :
			break

		crct_ans = line.split(sep=',')[6][0]
		
		print("waiting for answer")

		ans=str(client.recv(1).decode("utf8"))
		time=(client.recv(BUFFERSIZE).decode("utf8"))
		time=float(time)
		
		print("ans "+str(ans),flush=True)
		print("crct_ans "+str(crct_ans),flush=True)
		print("time "+str(time),flush=True)

		if ans==crct_ans :
			client.send(bytes("1","utf8"))
			tot_time+=time
		else:
			client.send(bytes("0","utf8"))
			client.close()
			return

		# print("sent")
		# recv (answer, time) from client, compare with ans, add time
		# if answer is 'e' timeout, terminate thread

		# print(q_no + ". " + question)
		line = q_file.readline()

	avg_time = tot_time / 5
	all_times.append({
		"name" : name,
		"time" : avg_time
	})

if __name__ == "__main__":
	SERVER.listen(4)
	# start_game()
	accept_in_connections()
	# ACCEPT_THREAD=Thread(target=accept_in_connections)
	# ACCEPT_THREAD.start()
	# ACCEPT_THREAD.join()

	print("Rithic is da bomb")
	all_times = sorted(all_times, key=lambda x: x["time"])

	print(all_times)

	# broadcast all_times to all clients