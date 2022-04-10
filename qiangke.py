#coding=utf-8
import requests
import time
from winsound import Beep
import threading
ts=time.time()
realtime=int(round(ts * 1000))

cookies = {
    'JSESSIONID': 'B3F1543888FF8E9F91E213F9065A58F9'
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-CSRF-TOKEN': 'ab3849d5-4aa0-471c-86eb-adfc0916af73',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://coursesel.umji.sjtu.edu.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://coursesel.umji.sjtu.edu.cn/welcome.action',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('_t', realtime),
)

def sendreq(data):
    global reqall,stop
    while(1):
        if(stop):
            print(reqall)
            return
        response = requests.post('https://coursesel.umji.sjtu.edu.cn/tpm/doElect_ElectTurn.action', headers=headers, params=params, cookies=cookies, data=data)
        ret=response.content
        if(len(ret)>1000):
            print("error")
            exit()
        if(str(ret).find("false")==-1):
            print("选课成功！")
            stop=1
            Beep(1500,2000)
            exit()
        print(ret.decode(encoding='utf-8',errors='ignore').strip())
        reqall+=1

mydata='jsonString=%7B%22electTurnId%22%3A%2223E9FE37-6EDB-4C22-ADA8-BF397210419E%22%2C%22autoElect%22%3Atrue%2C%22lessonTasks%22%3A%5B%22C9A064EB-B610-0001-62FD-1210D45066F0%22%5D%7D'
#sendreq(mydata)
stop=0
reqall=0
Nu=20
s=[threading.Thread(target=sendreq,args=(mydata,)) for i in range(Nu)]
for i in range(Nu):
    s[i].start()
#s[0].start()