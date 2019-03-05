import socket
#from threading import Thread
import requests
from bs4 import BeautifulSoup
import re
#TODO:define ip of the main comp
ip='127.0.0.1'
port=12345

def parse_result(html,soc):
   soup=BeautifulSoup(html,'html.parser')
   
question=""
answers=['','','']
multi=[0,0,0]
while True:
   s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   s.connect((ip,port))
   question=""
   answers=['','','']
   multi=[0,0,0]
   try:
           s.sendall("1".encode())
           ind=s.recv(1024)
           ind=ind.decode(encoding='utf-8')
           ind=ind.split("5662")
           question=ind[0]
           for x in range(3):
               answers[x]=ind[x+1]
           print("Got a question from main server\n"+question,answers[0],answers[1],answers[2])
           search = " "+question +" \""+ answers[0]+"\""
           print(search)
           r = requests.get("https://www.google.com/search", params={'q':search})
           print(answers[0])
           
           s.sendall("R".encode())
           soup=BeautifulSoup(r.text,'html.parser')
           res=soup.find("div", {"id": "topstuff"})
           if "No results found for" in res.get_text():
              s.sendall("-".encode())
              print("No results found......")
           else:   
              res = soup.find("div", {"id": "resultStats"})
              print(res)
              s.sendall(res.get_text().encode())
                    
           parse_result(r.texr,s)
           s.sendall("Q".encode())
   except Exception as e:
        print(">>>>>>connection retrying new QUESTION "+str(e))
   s.close()





