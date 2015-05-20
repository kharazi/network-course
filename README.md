# Network Programming Project
-----------------
**Vahid Kharazi - 90521139**

It's a course-project of Network Course to code socket and in this document I'll explain my code structure and answer project questions.
 
### How to Install?
I strongly recommend that you install project and all its dependencies in a way that does not interfere with the rest of your Python installation. This is accomplished by the creation of a virtual environment, or "virtualenv".

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r reqirements.pip
    
Install Mongodb with your packagemanager and run it.

### How to Run?
For running server, you can do it:
    
    python server.py
    
After running server, you can run client any number that you want.

    python client.py
    
### Protocol

I have used a customized application layer protocol:

|Request|Response(on success)|Response(on failure)|Description
|:---:|:----:|:---:|:---:|
|**REG**| OK(1)|NOK:Errno(1)| Register a new client
|**PUT**| OK(2) | NOK:Errno(2) | Upload a new file
|**GET**| Data(IP&Port of client to create a UDP connection)  | NOK:Errno(4) | Download a file
|**LST**| Data(List of files)  | NOK:Errno(3) | Get list of files
|**UDP_SEND**| OK(5) | -| To send file by UDP connection| 
|**UDP_RECV**| Data(Generated Port and IP of client)| -| To recv file by UDP connection 

**Note:** for bad request return `NOK:Errno(0)`
### Code Document

#####`model.py`:
    
* **FileModel(mongoengine.Document):** A mongodb document to store files metadata, like name, client and sha1 checksum

* **ClientModel(mongoengine.Document):** A mongodb document to store clients data

#####`server.py`:
    
* **ClientObject(object):** A class to store client data and send response. it's help to encapsulation.

* **ClientThread(threading.Thread):** Create a new thread for each new client
* **Server(object):** A class that listen to new request and create ClientObject for each

#####`client.py`:

* In this file we have two function that run simultaneously. one for getting command from users and second for listen to server.



### Project Questions

1. Port is os dependent. in this protocol, we generate port number in server and declare it to clients. It's fundamental problem, but if we reserve a range of ports, it's work perfect and less dependent on network.
2. For each connection, we create a new thread. as you know reading files from many location is not a truble, so now it's ok! But to sure enough we can impelement a mechanism like BitTorrent.
3. We can use checksum for each part or packet and resend request damped parts.
