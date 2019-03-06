import threading
import socket
import socketserver
import matplotlib.pyplot as plt
import numpy as np


#TODO: handle not cases
lock=threading.Lock()

data=''
points=[0,0,0]
qc=[0,0,0,0]
label=['getting data','getting data','getting data']
plt.ion()

def plotshow():
    global mpoints
    global points
    global label
    while True:
        color=['blue','blue','blue']
        color[points.index(max(points))]='green'
        plt.bar(x=[0,4,8],height=points,color=color,tick_label=label)
        plt.draw()
        plt.pause(0.0001)
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
            qc=[1,1,1,1]
            points=[0,0,0]
        conn.close()
    elif mode=="0" or mode=='1' or mode=='2' or mode=='3':
            print("Successfully connected to ["+mode+"] computer :",conn)
            while(qc[int(mode)]==0):
                    pass
            with lock:
                    qc[int(mode)]=0
            conn.sendall(data.encode())
            print("sent question to ["+mode+"] computer")
            while True:
              inpd=conn.recv(1).decode()
              if inpd=='Q':
                print("["+mode+"] computer work completed")
                conn.close()
                return
              elif inpd=="R":
                  inpfc=conn.recv(1024).decode()
                  with lock:
                     if(inpfc=='-'):
                       points[int(mode)-1]=-10
                     label[int(mode)-1]=inpfc
              elif inpd=="C":
                  continue
              else:
                   print("["+mode+"] computer ->",inpd)
                   if(qc[int(mode)]==1):
                       conn.close()
                       return
                   with lock:
                       if(qc[int(mode)]==1):
                          conn.close()
                          return
                       points[int(inpd)]+=1
                   
                
threading.Thread(target=plotshow,name='plotthread').start()
server = ThreadedTCPServer(('', 12345), ThreadedTCPRequestHandler)
with server:
    print("plot done and server started")
    server.serve_forever()
    server.shutdown()




