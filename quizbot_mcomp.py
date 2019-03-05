import threading
import socket
import socketserver
import matplotlib.pyplot as plt
import numpy as np

lock=threading.Lock()

#question=""
#answers=['','','']
data=''
points=[0,0,0]
qc=[0,0,0]
plt.ion()

def plotshow():
    global mpoints
    global points
    while True:
        color=['blue','blue','blue']
        color[points.index(max(points))]='green'
        plt.bar(x=[0,2,4],height=points,color=color)
        plt.draw()
        plt.pause(1)
        plt.clf()


        
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        initcmd = self.request.recv(1)
        print(initcmd)
        print("NO OF THREADS:",threading.active_count())
        for thread in threading.enumerate():
            print(thread.name)
        sortingcomputer(self.request, initcmd.decode('utf-8'))
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def sortingcomputer(conn,mode):
    global question
    global answers
    global data
    global qc
    global points
    print("mode="+mode)
    if mode=='M':
        print("Successfully connected with MOBILE :",conn)
        data=conn.recv(1024).decode(encoding='utf-8')
        print("data from mobile:"+data)
        with lock:
            qc=[1,1,1]          
        conn.close()
    elif mode=="2":
        print("Successfully connected to 2nd computer :",conn)
        while True:
            while(qc[0]==0):
                    pass
            with lock:
                    qc[0]=0
                    points=[0,0,0]
            conn.sendall(data.encode())
            print("sent question to 2nd computer")
            while True:
              inpd=conn.recv(1).decode(encoding='utf-8')
              if inpd=='Q':
                print("2nd computer work completed")
                conn.close()
                return
              else:
                   print("2nd computer ->",inpd)
                   with lock:
                        points[int(inpd)]+=1
                   if(qc[0]==1):
                       conn.close()
                       return
                   
                
threading.Thread(target=plotshow,name='plotthread').start()
server = ThreadedTCPServer(('', 12345), ThreadedTCPRequestHandler)
with server:
    print("plot done and server started")
    server.serve_forever()
    server.shutdown()




