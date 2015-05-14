import socket
import thread
import time

address = ('localhost', 22222)
mySocket = socket.socket()

mySocket.connect(address)
mySocket.send('REG:1'.encode())
print(mySocket.recv(1024))

def command():
    while True:
        inp = raw_input('in:')
        mySocket.send(inp.encode())


def listen():
    while True:
        msg = mySocket.recv(1024)
        message = msg.split(':')
        print msg

        if 'OK' in msg:
            continue

        if message[0] == 'UDP_LISTEN':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((message[1], int(message[2])))
            def udp_recv():
                temp = ' '
                byte_count = 0
                time_stamps = [time.time(), time.time()]


                while True:
                    data, addr = sock.recvfrom(1024)
        

                    if byte_count % 10 == 0:
                        time_stamps.append(time.time())
                    byte_count += 1
                    t = (time_stamps[-1] - time_stamps[-2])
                    print "DL:", 10.0 / t, '(byte/s)'



                    if data == "...":
                        # print "endfile"
                        break
                    temp += data
                # print "check checksum", message[4]
                with open('dl/%s' % message[3], 'wb') as f:
                    f.write(temp)

                import hashlib
                with open('dl/%s' % message[3], 'rb') as f:
                    print "Downloaded sha1: %s , file sha1: %s" % (
                        hashlib.sha1(f.read()).hexdigest(),
                        message[4]
                    )


            thread.start_new_thread(udp_recv, ())

        if message[0] == "UDP_SEND":
            def udp_send():
                byte_count = 0
                time_stamps = [time.time(), time.time()]
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                with open('up/%s' % message[3], "rb") as f:
                    byte = f.read(1)
                    while byte != "":

                        if byte_count % 10 == 0:
                            time_stamps.append(time.time())
                        byte_count += 1
                        t = (time_stamps[-1] - time_stamps[-2])
                        print "SEND", 10.0 / t, '(byte/s)'


                        byte = f.read(1)
                        sock.sendto(byte, (message[1], int(message[2])))
                sock.sendto('...', (message[1], int(message[2])))

            thread.start_new_thread(udp_send, ())

thread.start_new_thread(command, ())
thread.start_new_thread(listen, ())

while 1:
   pass