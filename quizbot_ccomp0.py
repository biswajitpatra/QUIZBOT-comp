import colorama
import re
import os
import time
import crayons
from nltk.corpus import stopwords
import pytesseract
import requests
import pyautogui
import json as m_json
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance
import argparse
colorama.init()
major=[0,0,0,0]

mystopword={".","(",")"}
stopwords={"which","where","when","is","does","these","the"}

def findregex(resultin):
    resultin=resultin.split()
    for xr in resultin:
        if re.search(xr,answers[0], re.IGNORECASE):
            gotit[0]+=1
        elif re.search(xr,answers[1], re.IGNORECASE):
            gotit[1]+=1   
        elif re.search(xr,answers[2], re.IGNORECASE):
            gotit[2]+=1
def parse_results(html, keyword,ans):
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find("div", {"id": "resultStats"})
    print(res)
    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    print("finding")
    for result in result_block:

        link = result.find('a', href=True)
        
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        #data=[b.string for b in soup.findall('b')]
        #print(data)
        if link and title and description:
            link = link['href']
            title = title.get_text()
            #print(description)
            descriptions = description.get_text()
            if link != '#' and rank < 3:
                #found_results.append({'keyword': keyword,'rank': rank, '\ntitle': title, '\ndescription': description})
                found_results.append(descriptions)
                #found_results.append(" ".join(filter(lambda w: not w in stopwords,descriptions.split())))
                print(crayons.white(title))
                data=[b.string for b in description.find_all('b') if b.string!="..."]
                major[ans]+=len(data)
                print(crayons.red(data,bold=True)) 
                rank += 1
    return found_results


question = "Which of these is known as sleeping policeman of roads"#"The guinea pig is native to which continent?"
answersen = ["Traffic lights", "Speed Bumps", "Zebra crossing"]
answers=[]

question=question.replace("?","")
question=question.lower()
for a in answersen:
    xtemp=a.replace("." ," ")
    xtemp=xtemp.lower()
    answers+=[xtemp]
question=question.replace("Which","")
question=question.replace("What","") 
for i, a in enumerate(answers):
    answers[i] = a.replace("?", "ti")

print("\n\n{}\n\n{}\n\n".format(
    crayons.green(question),
    crayons.red(", ".join(answers))
))
question=" ".join(filter(lambda w: not w in stopwords,question.split()))
#question = question.split(' ', 1)[1]
#question = question[:-1] 
#question = question.replace(" ", "\" \"")
print("\n\n{}\n\n{}\n\n".format(
    crayons.green(question),
    crayons.red(", ".join(answers))
))
maxi=[0,0,0]
'''
query = urllib.urlencode ( { 'q' : search } )
response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
json = m_json.loads ( response )
results = json [ 'responseData' ] [ 'results' ]
for result in results:
  title = result['title']
  url = result['url']   # was URL in the original and that threw a name error exception
  print ( title + '; ' + url )
'''  
gotit=[0,0,0]
search = ""+question +" (("+ answers[1] +") | ("+answers[0]+") | ("+answers[2]+"))"
print(search)
r = requests.get("https://www.google.com/search", params={'q':search})
results = parse_results(r.text,search,3)
for result in results:
    '''
     if re.match("("+answers[0]+")"+"("+answers[1]+")"+"("+answers[2]+")", result, re.IGNORECASE) :
       gotit[1]+=1
     if re.search(answers[2], result, re.IGNORECASE):
       gotit[2]+=1
     if re.search(answers[0], result, re.IGNORECASE):
       gotit[0]+=1'''
    result=re.sub("\.|\)|\(","",result)
    findregex(result)
    print(crayons.green(result))
'''if gotit[0]==gotit[1]==gotit[2]:
 print(crayons.magenta("INValid"))
else: 
 mn,idx = max( (gotit[i],i) for i in range(3) )
 print(crayons.magenta("answer is in Interference APPROACH : "+answers[idx],bold=True)) 
 '''    
search = " "+question +" \""+ answers[0]+"\""#+" -\""+answers[1]+"\" -\""+answers[2]+"\""
print(search)      
r = requests.get("https://www.google.com/search", params={'q':search})
#soup = BeautifulSoup(r.text, "html.parser")
#res = soup.find("div", {"id": "resultStats"})
print (answers[0])
results = parse_results(r.text,search,0)
for result in results:
     if answers[1] in result:
       maxi[1]+=1
     if answers[2] in result:
       maxi[2]+=1  
     print(crayons.cyan(result))  
#name_box = soup.find('div', attrs={'id': 'topstuff'})
#print(name_box)
#print(res)    
#hmax[0]=int(res.text.replace(",", "").split()[1])
#print (hmax[0])

search = ""+question +" \""+ answers[1]+"\""#+" -\""+answers[0]+"\" -\""+answers[2]+"\""
print(search)
r = requests.get("https://www.google.com/search", params={'q':search})
#soup = BeautifulSoup(r.text, "html.parser")
#res = soup.find("div", {"id": "resultStats"})
print (answers[1])
results = parse_results(r.text,search,1)
for result in results:
     if answers[0] in result:
       maxi[0]+=1
     if answers[2] in result:
       maxi[2]+=1
     print(crayons.yellow(result))
#name_box = soup.find('div', attrs={'id': 'topstuff'})
#print(name_box)
#print(res)
#hmax[1]=int(res.text.replace(",", "").split()[1])
#print (hmax[1])

search = ""+question +" \""+ answers[2] +"\""#+" -\""+answers[0]+"\" -\""+answers[1]+"\""
print(search)
r = requests.get("https://www.google.com/search", params={'q':search})
#print(r)
#soup = BeautifulSoup(r.text, "html.parser")
#res = soup.find("div", attrs ={"id": "resultStats"})
print(answers[2])
results = parse_results(r.text,search,2)
for result in results:
     if answers[0] in result:
       maxi[0]+=1
     if answers[1] in result:
       maxi[1]+=1
     print(crayons.green(result))
#print(res)
#name_box = soup.find('div', attrs={'id': 'topstuff'})
#print(name_box) 
#hmax[2]=int(res.text.replace(",", "").split()[1])
#print (hmax[2])
print(maxi)
#mn,idx = max( (hmax[i],i) for i in range(len(hmax)) )
#print(crayons.green(answers[idx]))
major[3]=0
mn,idx = max( (major[i],i) for i in range(4) )
print(crayons.magenta("answer is in READ APPROACH : "+answers[idx],bold=True))
if maxi[0]==maxi[1]==maxi[2]:
 print(crayons.magenta("INValid"))
else: 
 mn,idx = max( (maxi[i],i) for i in range(3) )
 print(crayons.magenta("answer is in Interference APPROACH : "+answers[idx],bold=True))
if gotit[0]==gotit[1]==gotit[2]:
 print(crayons.magenta("INValid"))
else: 
 mn,idx = max( (gotit[i],i) for i in range(3) )
 print(crayons.magenta("answer is in normal APPROACH : "+answers[idx],bold=True))
print("gotit",gotit)
input("Continue?")
time.sleep(0.1)
os.system("cls")
