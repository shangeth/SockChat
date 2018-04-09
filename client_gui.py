from tkinter import *
import socket
from threading import Thread
import backend
import sys


global HOST
global PORT
global client_socket
global BUFSIZ
BUFSIZ = 1024
con_res = 1

def receive():
    global client_socket
    BUFSIZ =1024
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf-8")
            msg_list.insert(END, msg)
            winsound.Beep(400, 300)
            backend.insert(msg)
            msg_list.see(END)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    global client_socket
    client_socket.send(bytes(msg,"utf-8"))
    if msg == "quit":
        client_socket.close()
        top.quit()
        sys.exit()


def clear_textbox(event=None):
    entry_field.delete(0, END)

def clear_ip(event=None):
    ip_entry.delete(0, END)

def clear_port(event=None):
    port_entry.delete(0, END)

def validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True

def send_ip(event=None):
    global HOST
    global PORT
    if validIP(ip_entry.get()) and port_entry.get() != "" and ip_entry.get() != "" and port_entry.get().isdigit():
        HOST = ip_entry.get()
        PORT = int(port_entry.get())
        connect_recieve(HOST,PORT)

    else:
        msg_list.delete(0, END)
        msg_list.insert(END,"Enter a valid Server IP and Port!!")



def connect_recieve(HOST,PORT):
    global BUFSIZ
    global con_res
    BUFSIZ = 1024
    global client_socket
    ADDR = (HOST, PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    entry_field.delete(0, END)
    msg_list.insert(END, "Connecting to the Server...")
    client_socket.settimeout(1)
    con_res=client_socket.connect_ex(ADDR)
    if con_res == 0:
        client_socket.settimeout(None)
        ip_frame.pack_forget()
        entry_frame.pack()
        msg_list.delete(0, END)
        for row in backend.view():
            msg_list.insert(END, row)
        msg_list.see(END)
        receive_thread = Thread(target=receive)
        receive_thread.start()
    else:
        msg_list.delete(0, END)
        msg_list.insert(END, "Server Not found at IP and Port")

def close_window(event=None):
    if con_res == 0 :
        client_socket.close()
        top.destroy()
        sys.exit(0)
    else:
        sys.exit(0)


#-----------------------------------------------------------------------------------------------------------------------

top = Tk()
top.title("ChatApp")
top.resizable(False, False)
top.geometry("600x730-0+40")
top.protocol('WM_DELETE_WINDOW', close_window)

ip_frame = Frame(top)
ip_host_entry = StringVar()
ip_host_entry.set("Enter Host IP")
port_host_entry = StringVar()
port_host_entry.set("Enter Host port")
ip_entry = Entry(ip_frame,textvariable=ip_host_entry,width=80)
ip_entry.bind("<Button-1>", clear_ip)
ip_entry.pack()
port_entry = Entry(ip_frame,textvariable=port_host_entry, width=80)
port_entry.bind("<Button-1>", clear_port)
port_entry.pack()
ip_button = Button(ip_frame, text="submit ip",command=send_ip,width=20)
ip_button.pack()
ip_button.bind("<Button-1>", send_ip)
ip_frame.pack()




messages_frame = Frame(top)
my_msg = StringVar()
my_msg.set("Type your message here.")
scrollbar = Scrollbar(messages_frame)
msg_list = Listbox(messages_frame,height=40 , width=100, yscrollcommand = scrollbar.set, background="#dee4ed")
scrollbar['command'] = msg_list.yview
scrollbar.pack(side=RIGHT, fill=Y)

msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()

msg_list.yview(END)


messages_frame.pack()




entry_frame = Frame(top)
entry_field = Entry(entry_frame, textvariable=my_msg, width=80)
entry_field.bind("<Return>", send)
entry_field.pack(padx=5)
entry_field.bind("<Button-1>", clear_textbox)
bu2 = Button(entry_frame, text='CLEAR', command=clear_textbox)
bu2.pack()
send_button = Button(entry_frame, text="Send", command=send,width=20)
send_button.pack()
entry_field.pack()
entry_frame.pack_forget()




#-----------------------------------------------------------------------------------------------------------------------


top.mainloop()