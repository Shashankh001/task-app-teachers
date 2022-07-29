import socket
import time

def get_ip():
    with open('ip2.txt') as f:
        return f.read()

IP = get_ip()

def sendd(arg, message): #usage: send("HW","The notification message")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP,2231))

    s.send(bytes(arg,'utf-8'))
    
    time.sleep(1.5)
    message = f"{message[:30]}..."
    s.send(bytes(message,'utf-8'))

