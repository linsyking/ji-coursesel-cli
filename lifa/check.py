from time import sleep
import requests
import threading
import json
from winsound import Beep

def sendreq(rdat):
    while(1):
        res = requests.get(f'https://dailyreport.sjtu.edu.cn/haircut/frontend/bus/schedule/list?{rdat}',cookies={"JSESSIONID":"***", "dailyreport.sjtu": "***"})
        kop = res.content.decode(encoding='utf-8',errors='ignore')
        kks = json.loads(kop)['entities']
        print(rdat[10])
        for one in kks:
            if(int(one['leftSeat'])!=0):
                Beep(1000,1000)
                if(rdat[10]=='W'):
                    print('2餐')
                if(rdat[10]=='H'):
                    print('3餐')
                if(rdat[10]=='O'):
                    print('4餐')
                print(rdat['stateDate'],rdat['startTime'])
                break
            # print(one['count'])
        sleep(3)

def seq(ddts):
   for i in ddts:
       sendreq(i) 

sp=[]

for i in range(11,12):
    sp.append(f'lineType=TWO&date=2022-04-{i}')
    sp.append(f'lineType=THIRD&date=2022-04-{i}')
    sp.append(f'lineType=FOURTH&date=2022-04-{i}')

alth=[]

for i in range(len(sp)):
    alth.append(threading.Thread(target=sendreq,args=(sp[i],)))

for th in alth:
    th.start()

for th in alth:
    th.join()
