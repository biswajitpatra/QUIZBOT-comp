import socket
#from threading import Thread
import requests
from bs4 import BeautifulSoup
import re
#TODO:define ip of the main comp
ip='127.0.0.1'
port=12345

def wparse_result(link,soc):
   pass

def gparse_result(bsoup,soc):
   result_blocks=bsoup.find_all('div',attrs={'class':'g'})
   wlinks=[]
   bdata=[]
   print('finding')
   for result in result_blocks:
        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        if link and title and description:
                wlinks.append(link['href'])
                title=title.get_text()
                decp=description.get_text()
                bdata=[b.string() for b in decp.find_all('b') if b.string!="..."]
                decp=decp.split[" ... "]
                
        
        
   
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
              gparse_result(soup,s)      
           
           s.sendall("Q".encode())
   except Exception as e:
        print(">>>>>>connection retrying new QUESTION "+str(e))
   s.close()





