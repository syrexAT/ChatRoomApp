import socket
import threading
import sockettools

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# instead of binding the socket to host and port, we are connecting it
client.connect(('127.0.0.1', 55555))

DisconnectMessage = 'Client disconnected'

# define 2 methods
# run 2 threads at the same time
# receive data from the server all the time, so receive function running constantly
# at the same time have a thread for all messages that we are going to send

def receive():
    while True:
        try:
            # try receive messages from the server, we are saying client.recv but its receiving from the server
            message = client.recv(1024).decode('UTF-8')
            # check if message that we just receive, is NICK or something else
            if message == 'NICK':
                client.send(nickname.encode('UTF-8'))
            else:
                print(message)
        except:
            print("Disconnected!")
            client.close()
            break

def write():
    while True:
        # constantly running new input functions, as sooon as the user presses enter we are asking for the next one
        # the only option that the user has is to close the client or write new messages
        # receive and write will run a the same time
        text = input("")
        message = f'{nickname}: {text}'
        if text == 'quit':
            client.send(DisconnectMessage.encode('UTF-8'))
            print('You disconnected from the server!')
            client.close()
            break
        else:
            client.send(message.encode('UTF-8'))



# run receive thread and write thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()