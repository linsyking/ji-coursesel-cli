from time import sleep
import requests
import threading
import json
from winsound import Beep

def sendreq(rdat):
    while(1):
        res = requests.get(f'https://dailyreport.sjtu.edu.cn/market/frontend/market/schedule/list?{rdat}',cookies={"JSESSIONID":"F802DE0D68EABFA59D65DCDCA5D99454", "dailyreport.sjtu": "ffffffff097e1f5245525d5f4f58455e445a4a4229a0"})
        kop = res.content.decode(encoding='utf-8',errors='ignore')
        kks = json.loads(kop)['entities']
        for one in kks:
            if(int(one['leftSeat'])!=0):
                Beep(1000,1000)
                if(rdat[10]=='Q'):
                    print('jiaochao')
                if(rdat[10]=='L'):
                    print('Losen')
                print(rdat['stateDate'],rdat['startTime'])
                break
            # print(one['count'])
        sleep(3)

def seq(ddts):
   for i in ddts:
       sendreq(i) 

sp=[]

for i in range(14,15):
    sp.append(f'lineType=XQJYCS&date=2022-04-{i}')
    sp.append(f'lineType=YLYLS&date=2022-04-{i}')

alth=[]

for i in range(len(sp)):
    alth.append(threading.Thread(target=sendreq,args=(sp[i],)))

for th in alth:
    th.start()

for th in alth:
    th.join()