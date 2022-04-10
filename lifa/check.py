from time import sleep
import requests
import threading
import json
from winsound import Beep

def sendreq(rdat):
    while(1):
        res = requests.post('https://sports.sjtu.edu.cn/manage/fieldDetail/queryFieldSituation',json=rdat,cookies={"JSESSIONID":"6d6435db-3b80-459a-af09-a4adacb1522a"})
        kop = res.content.decode(encoding='utf-8',errors='ignore')
        kks = json.loads(kop)['data'][0]['priceList']
        for one in kks:
            if(int(one['count'])!=0):
                Beep(1000,1000)
                if(rdat['fieldType']=='0a14f823-3ac7-48e8-9313-4d7545e6c430'):
                    print('2餐')
                if(rdat['fieldType']=='12add9f5-a3b3-4caf-a9ab-803867bac856'):
                    print('3餐')
                if(rdat['fieldType']=='5b7887ed-2525-4950-b490-8315919c6fb2'):
                    print('4餐')
                print(rdat['date'])
                break
            # print(one['count'])
        sleep(3)

def seq(ddts):
   for i in ddts:
       sendreq(i) 

sp=[]

for i in range(9,10):
    if(i==9):
        i='09'
    date=f'2022-04-{i}'
    sp.append({"fieldType":"0a14f823-3ac7-48e8-9313-4d7545e6c430","date":date})
    sp.append({"fieldType":"12add9f5-a3b3-4caf-a9ab-803867bac856","date":date})
    sp.append({"fieldType":"5b7887ed-2525-4950-b490-8315919c6fb2","date":date})

alth=[]

for i in range(len(sp)):
    alth.append(threading.Thread(target=sendreq,args=(sp[i],)))

for th in alth:
    th.start()

for th in alth:
    th.join()
