import socket
import requests
from bs4 import BeautifulSoup
import re
import nltk
lemma = nltk.wordnet.WordNetLemmatizer()
#TODO:define ip of the main comp
ip='127.0.0.1'
port=12345  
question=""
answers=['','','']
multi=[0,0,0]


def wparse_result(link,soc):
   pass

def gparse_result(bsoup,soc):
   result_blocks=bsoup.find_all('div',attrs={'class':'g'})
   wlinks=[]
   bdata=[]
   print('finding')
   if len(result_blocks)>5:
      result_blocks=result_blocks[:5]
   for result in result_blocks:
        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        soc.sendall("C".encode())
        if link and title and description:
                wlinks.append(link['href'])
                title=title.get_text()
                bdata=[lemma.lemmatize(b.string.lower()) for b in description.find_all('b') if b.string!="..."]
                bdata=set(bdata)
                decp=re.sub(r'[^a-zA-Z0-9\.]+',' ',description.get_text()).split("...")               
                print("Title:",title)
                print("bdata:",bdata)
                print("desciption",decp)
                
                
                
                
   if len(wlinks)>3:             
       wlinks=wlinks[:3]        
   for x in wlinks:
         soc.sendall("C".encode())
         if x!="#":
              wparse_result(x,soc)
        

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

        search = "\""+ answers[0]+"\" "+question 
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
        print("completed>>>>")
     except IOError as e:
          print(">>>>>>connection retrying new QUESTION "+str(e))
     s.close()





