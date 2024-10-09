
from time import sleep
import socket
import json
from random import randint
BUFFER_SIZE = 1024

        
            

def send(ip,port,message):
    print ("connecting to server")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            print(ip,port)
            s.connect((ip,port))

            """except socket.error as err:
                print("socket.error : %s",12303002 % err)
                quit()"""

        
            s.send(json.dumps(message).encode())
            print ("--> sent data: " ,message)
            s.close()
            return
        except:
            print("connection failed trying again")
            sleep(randint(0,10))
            continue
def recive(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("listening on",ip,port)
    try:
        
        s.bind((ip,port))
        
        s.listen(1)
    except socket.error as err:
        print ("socket.error : %s" % err)
        s.close()
        quit()
                    
    c, addr = s.accept()
    print (c,'client connected to server: ' , addr)

    while True:
        print ("waiting for message from client")
        m_str = c.recv(BUFFER_SIZE).decode()
        print ("<-- received data:", m_str )

        try:
            m_json = json.loads(m_str)
            c.close()
            return m_json
        except ValueError:
            print ('    received data is no JSON, exiting ...')
            c.close()
        



            
            
           