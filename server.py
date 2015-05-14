import socket
import random
import threading
from mongoengine import connect
from models import ClientModel, FileModel


class ClientThread(threading.Thread):

    def __init__(self, serv, client_object):
        threading.Thread.__init__(self)
        self.client = client_object
        self.server = serv
        self.running = True
        self.model = None
        self.port_list = []

    def _reg(self, message):

        try:
            self.model = ClientModel(name=message[1], addr=str(self.client.address)).save()
            self.client.update(message='OK(1)')
        except:
            self.client.update(message='NOK:Errno(1)')

    def _get(self, message):
        GEN_PORT = -1 # Unvalid
        while True:
            GEN_PORT = random.randint(6666,9999)
            if GEN_PORT not in self.port_list:
                self.port_list.append(GEN_PORT)
                break
            else:
                continue

        if not GEN_PORT:
            print "Port full"

        requested_file = FileModel.objects(name=message[1]).first()
        if requested_file:
            for cl in self.server.client_list:
                if str(cl.address) == requested_file.client.addr:
                    self.client.update('UDP_LISTEN:%s:%d:%s:%s' % (self.client.address[0], GEN_PORT, requested_file.name,requested_file.checksum))
                    cl.update('UDP_SEND:%s:%d:%s' % (
                        self.client.address[0], GEN_PORT, message[1])
                    )
        else:
            self.client.update(message='NOK:Errno(4)')

    def _put(self, message):
        try:
            FileModel(
                name=message[1], checksum=message[2], client=self.model
            ).save()
            self.client.update(message='OK(2)')
        except:
            self.client.update(message='NOK:Errno(2)')

    def _lst(self, message):
        try:
            self.client.update(message='\n'.join(FileModel.objects.scalar('name')))
        except:
            self.client.update(message='NOK:Errno(3)')

    def _udp_res(self, message):
        pass



    def run(self):
        while self.running:
            message = self.client.sock.recv(self.server.BUFFSIZE)
            message = message.split(':')
            msg_req = message[0]
            if msg_req == 'REG':
                self._reg(message)
            if msg_req == 'GET':
                self._get(message)
            if msg_req == 'PUT':
                self._put(message)
            if msg_req == 'LST':
                self._lst(message)

            if msg_req is not None and msg_req != "":
                if msg_req not in ['REG', 'GET', 'PUT', 'LST']:
                    print 'here', msg_req, 'here'
                    # client.update(message='NOK:Errno(0)')


class ClientObject(object):

    def __init__(self, client_info):
        self.sock = client_info[0]
        self.address = client_info[1]

    def update(self, message):
        msg = '%s' % message
        self.sock.send(msg.encode())


class Server(object):

    def __init__(self, host, port):

        self.HOST = host
        self.PORT = port
        self.BUFFSIZE = 1024
        self.ADDRESS = (self.HOST, self.PORT)


        self.client_list = []
        self.running = True
        self.serverSock = socket.socket()
        self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSock.bind(self.ADDRESS)
        self.serverSock.listen(10)

        print("Waiting to connections...")

        while self.running:
            client_info = self.serverSock.accept()
            client_object = ClientObject(client_info)
            clthread = ClientThread(self, client_object)
            clthread.start()
            print("Client connected from {}.".format(client_info[1]))
            self.client_list.append(ClientObject(client_info))

        self.serverSock.close()


if __name__ == '__main__':
    connect('network')
    FileModel.objects.delete()
    ClientModel.objects.delete()
    Server(host='localhost', port=22222)
