import socket
from threading import Thread
#define ip of the main comp
ip='127.0.0.1'
port=12345

#lock=threading.Lock()
question=""
answers=['','','']
while True:
   s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   s.connect((ip,port))
   while True:
          try:   
                 s.sendall("2".encode())
                 ind=s.recv(1024)
                 ind=ind.decode(encoding='utf-8')
                 ind=ind.split("5662")
                 question=ind[0]
                 for x in range(3):
                     answers[x]=ind[x+1]
                 print("Got a question from main server\n"+question,answers[0],answers[1],answers[2])
                 s.sendall("1".encode())
                 s.sendall("2".encode())
                 
  
    
          except Exception as e:
              print(">>>>>>connection retrying new QUESTION "+str(e))
   s.close()
        
        
        
    
    
