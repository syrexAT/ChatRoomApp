import threading
import socket

host = '127.0.0.1'  # localhost, can be changed to public IP Address to make it viable through internet
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding server to the host and IP address
server.bind((host, port))  # TUPLE, server is bound to localhost on 55555
server.listen()  # listening mode for incoming connections

# define 3 methods
# broadcast method
# handle method for client connections
# receive method to combine all methods in a main method

# 2 empty lists
clients = []  # where we put all our clients in, and get nickname of the client
nicknames = []

# BROADCAST FUNCTION, sends message to all clients that are connected to the server
def broadcast(message):
    for client in clients:
        client.send(message) # getting all the clients and sending a particular message

# handle the client connection, when a client connect we want to receive messages from the client
# and send back messages to all the other clients

# later this will be run on all the clients
def handle(client):
    while True: # endless loop
        try:
            message = client.recv(1024) # 1024 bytes # as long as it works, that we receive message from the client, are broadcasting it to all the other clients
            broadcast(message)
        except: # will give error when the client is not there anymore/has disconnected
            # cut the connection, remove it from the list and terminate this loop
            index = clients.index(client) # getting the index of the client from the list
            clients.remove(client)
            client.close()
            nickname = nicknames[index] # when we remove the client we also remove the nickname from that index
            # broadcast that the client has left
            broadcast(f'{nickname} left the chat!'.encode('UTF-8')) # could also be ascii
            nicknames.remove(nickname)
            break


#main method/receive method
def receive():
    while True: #accepting all connections
        client, address = server.accept() # running the accept method all the time, it returns a client and the address
        # if this happens, when a client connects ->
        print(f"{str(address)} has connected") # if a connection comes, we print that we are now connected

        # getting the nickname from the client --> ask the client for the nickname
        client.send('NICK'.encode('UTF-8')) # if the client receives the NICK, then it should be informed that it should send the nickname
        nickname = client.recv(1024).decode('UTF-8')
        nicknames.append(nickname) # put nickname in list
        clients.append(client) # put client in list

        print(f'Nickname of the client is {nickname}!')
        # broadcast so every client gets informed that this client has connected
        broadcast(f'{nickname} joined the chat!'.encode('UTF-8'))
        client.send('Connected to the server!'.encode('UTF-8')) #send this particular client that he has now connected!

        # define a thread and run a thread
        # running 1 thread for each client connected
        thread = threading.Thread(target=handle, args=(client,))
        thread.start() # use the start method not the run method
print("Server is listening...")
receive()


