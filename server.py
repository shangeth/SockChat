import select
import socket
from threading import Thread




def accepting_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("New Client {} Connected from port {}".format(client_address[0], client_address[1]))
        client.send(bytes("Welcome to the ChatApp  Enter your username and press ENTER!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = "Welcome {}! , If you want to exit the chat , type \" quit \"".format(name)
    client.send(bytes(welcome, "utf8"))
    msg = "{} has joined the chat!".format(name)
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while 1:
        try:
            ready_to_read, ready_to_write, in_error = select.select([client, ], [client, ], [], 5)
            msg = client.recv(BUFSIZ)
        except select.error:
            client.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
            client.close()
            print("{} disconnected".format(addresses[client]))
            del clients[client]
            broadcast(bytes("{} has left the chat.".format(name), "utf8"))
            break


        if msg != bytes("quit", "utf8"):
            broadcast(msg, name + " : ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            print("{} disconnected".format(addresses[client]))
            del clients[client]
            broadcast(bytes("{} has left the chat.".format(name), "utf8"))
            break





def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(prefix.encode("utf-8") + msg)




clients = {}
addresses = {}

host = ""
port = 9997
BUFSIZ = 1024
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((host, port))


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accepting_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

