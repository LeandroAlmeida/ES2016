import pickle
from github import Github
from os import system
import json 
from unicodedata import normalize
from operator import itemgetter
import datetime
import time

ACCESS_TOKEN = '558df36855f81934d8930b21e292b017c82d140e'
client = Github(ACCESS_TOKEN, per_page=100)
import sys
try:
    arq = file('states.json')
    states=json.load(arq)
    arq.close() 
except IOError:
    print "Saindo..."
    sys.exit(0)

#Passo 1 Todos os usuarios brasileiros

system("cls")
#print client.get_rate_limit().raw_data["resources"]["core"]["remaining"]
listSearch=["created:<=2009-01-01%20location:Brasil", 
            "created:2009-01-02..2010-01-01%20location:Brasil",
            "created:2010-01-02..2010-06-01%20location:Brasil",
            "created:2010-06-02..2011-01-01%20location:Brasil",
            "created:2011-01-02..2011-06-01%20location:Brasil",
            "created:2011-06-02..2011-09-01%20location:Brasil",
            "created:2011-09-02..2012-01-01%20location:Brasil",
            "created:2012-01-02..2012-03-01%20location:Brasil",
            "created:2012-03-02..2012-06-01%20location:Brasil",
            "created:2012-06-02..2012-09-01%20location:Brasil",
            "created:2012-09-02..2013-01-01%20location:Brasil",
            "created:2013-01-02..2013-03-01%20location:Brasil",
            "created:2013-03-02..2013-06-01%20location:Brasil",
            "created:2013-06-02..2013-09-01%20location:Brasil",
            "created:2013-09-02..2014-01-01%20location:Brasil",
            "created:2014-01-02..2014-03-01%20location:Brasil",
            "created:2014-03-02..2014-06-01%20location:Brasil",
            "created:2014-06-02..2014-09-01%20location:Brasil",
            "created:2014-09-02..2014-11-02%20location:Brasil"]
            
listUser=[]
listErro=[]
print "Carregando..."

while True:
    for search in listSearch:
        try:
            users=[s for s in client.legacy_search_users(search)]
            listUser.extend(users) 
        except Exception, e: #ssl.SSLError TimeOut
            print "Error: ", search," tipo: ",e
            listErro.append(search)
    if len(listErro)>0:
        print "Re-buscando: ",len(listErro)
        listSearch=listErro
        listErro=[]
    else:
        break       
dicUser={}
print "Quantidade de usuarios com brasil na localizacao: ", len(listUser)
for user in listUser:
    dicUser.update({user.login:user})
print "Quantidade de usuarios com brasil na localizacao sem repeticao: ", len(dicUser)
print
listSearch=["created:<=2009-01-01%20location:Brazil", 
            "created:2009-01-02..2010-01-01%20location:Brazil",
            "created:2010-01-02..2010-06-01%20location:Brazil",
            "created:2010-06-02..2010-09-01%20location:Brazil",
            "created:2010-09-02..2011-01-01%20location:Brazil",
            "created:2011-01-02..2011-03-01%20location:Brazil",
            "created:2011-03-02..2011-06-01%20location:Brazil",
            "created:2011-06-02..2011-09-01%20location:Brazil",
            "created:2011-09-02..2012-01-01%20location:Brazil",
            "created:2012-01-02..2012-03-01%20location:Brazil",
            "created:2012-03-02..2012-06-01%20location:Brazil",
            "created:2012-06-02..2012-09-01%20location:Brazil",
            "created:2012-09-02..2013-01-01%20location:Brazil",
            "created:2013-01-02..2013-03-01%20location:Brazil",
            "created:2013-03-02..2013-06-01%20location:Brazil",
            "created:2013-06-02..2013-09-01%20location:Brazil",
            "created:2013-09-02..2013-11-01%20location:Brazil",
            "created:2013-11-02..2014-01-01%20location:Brazil",
            "created:2014-01-02..2014-03-01%20location:Brazil",
            "created:2014-03-02..2014-05-01%20location:Brazil",
            "created:2014-05-02..2014-07-01%20location:Brazil",
            "created:2014-07-02..2014-10-01%20location:Brazil",
            "created:2014-10-02..2014-11-02%20location:Brazil"
            ]
listUser2=[]
listErro=[]
print "Carregando..."

while True:
    for search in listSearch:
        try:
            users=[s for s in client.legacy_search_users(search)]
            listUser2.extend(users) 
        except Exception, e: #ssl.SSLError TimeOut
            print "Error: ", search," tipo: ",e
            listErro.append(search)
    if len(listErro)>0:
        print "Re-buscando: ",len(listErro)
        listSearch=listErro
        listErro=[]
    else:
        break

print "Quantidade de usuarios com brazil na localizacao: ", len(listUser2)
dicUser2={}
for user in listUser2:
    dicUser2.update({user.login:user})
print "Quantidade de usuarios com brazil na localizacao sem repeticao: ", len(dicUser2)


dicUser.update(dicUser2)

print "Total de usuarios Brasileiros: ", len(dicUser)
#passo 2 usuarios válidos
listUsersBrasilValid=[]
cont=0
erro=0
listUser=dicUser.values()
#print client.get_rate_limit().raw_data["resources"]["core"]["remaining"]
contBrazil=0
while True:
    for user in listUser:
        aux=user.location
        aux=normalize('NFKD', aux).encode('ASCII','ignore')
        aux=aux.upper()
        aux=" "+aux+" "
        aux=aux.replace(" BRASIL "," BRAZIL ")
        aux=aux.replace("    "," ")
        aux=aux.replace("   "," ")
        aux=aux.replace("  "," ")
        if aux == " BRAZIL ":
            contBrazil+=1
        if aux != " BRAZIL ":
            try:
                if cont>4400:
                    if int(client.get_rate_limit().raw_data["resources"]["core"]["remaining"])<4400:
                        temp=int(client.get_rate_limit().raw_data["resources"]["core"]["reset"])-int(time.time())
                        cont=0            
                        if temp>0:        
                            print "Waiting ", temp," s."  
                            time.sleep(temp+1)
                cont+=1
                events=[i for i in user.get_public_events()]
                if len(events)!=0:
                    for event in events:
                        if event.created_at.date()>datetime.date(2014,8,2):                           
                            if event.type=="PullRequestEvent":
                                if event.payload["action"]=="opened":
                                    listUsersBrasilValid.append(user)
                                    break
                            elif event.type=="IssuesEvent":
                                if event.payload["action"]=="opened":
                                    listUsersBrasilValid.append(user)
                                    break
                            elif event.type=="PushEvent":
                                listUsersBrasilValid.append(user)
                                break
                        else:
                            break
              
            except Exception, e:
                print user.login," ",e
                listErro.append(user)
    if len(listErro)!=0 and erro<5:
        listUser=listErro
        listErro=[]
        erro+=1
    else:
        break 

print "Total de usuarios com apenas Brasil ou Brazil na localizacao,", contBrazil
print
print "Total de usuarios brasileiros com conta ativa: ",len(listUsersBrasilValid)

#passo 3 
dicStates={}
dicReg={}
NoLoc=[]
listUser=[]
for i in listUsersBrasilValid:
    aux=i.location
    cont=0
    aux=normalize('NFKD', aux).encode('ASCII','ignore')
    aux=aux.upper()
    aux=aux.replace(")"," ")
    aux=aux.replace("("," ")
    aux=aux.replace(","," ")
    aux=aux.replace(".","")
    aux=aux.replace("-"," ")
    aux=aux.replace("|"," ")
    aux=aux.replace("/"," ")
    aux=aux.replace("\\"," ")
    aux=aux.replace(">"," ")
    aux=aux.replace("<"," ")
    aux=aux.replace("?"," ")
    aux=" "+aux+" "
    aux=aux.replace(" BRASIL "," BRAZIL ")
    aux=aux.replace("    "," ")
    aux=aux.replace("   "," ")
    aux=aux.replace("  "," ")
    if aux != " BRAZIL ":
        
        for j in states:
            if (" "+j["NAME"]+" " in aux) or (" "+j["ABBREVIATION"]+" " in aux) or (" "+j["CAPITAL"]+" " in aux):
                if dicStates.has_key(j["NAME"]):
                    dicStates.update({j["NAME"]:dicStates[j["NAME"]]+1})
                else:
                    dicStates.update({j["NAME"]:1})
                if dicReg.has_key(j["REGION"]):
                    dicReg.update({j["REGION"]:dicReg[j["REGION"]]+1})
                else:
                    dicReg.update({j["REGION"]:1})
                listUser.append(i)#User Brazil
                cont=1
                break
        if cont==0:
            NoLoc.append(i)
    else:
        NoLoc.append(i)        

print "Total de usuarios localizados(Estado ou Capital): ", len(listUser)
print
aux=sorted(dicStates.items(), key=itemgetter(1), reverse=True)
for i in aux:
    print i[0], "--> ", i[1]
print
arq = open('backupTopStates.json','w')
arq.write(json.dumps(aux))
arq.close() 

aux=sorted(dicReg.items(), key=itemgetter(1), reverse=True)
for i in aux:
    print i[0], "--> ", i[1]
print
arq = open('backupTopReg.json','w')
arq.write(json.dumps(aux))
arq.close() 


arq = open('backupUsersValidBrasil.txt','wb')
pickle.dump(listUser,arq)
arq.close() 


"""
from collections import Counter
temp=[e.location for e in NoLoc]
for i in Counter(temp).most_common():
    print i[0]," ",i[1]
"""

print "Ok"