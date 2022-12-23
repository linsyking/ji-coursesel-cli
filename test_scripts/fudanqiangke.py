import requests
import time
import threading
ts=time.time()
realtime=int(round(ts * 1000))

headers = {
    'authority': 'xk.fudan.edu.cn',
    'sec-ch-ua': 'Microsoft',
    'accept': 'text/html, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
    'sec-ch-ua-platform': 'Windows',
    'origin': 'https://xk.fudan.edu.cn',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://xk.fudan.edu.cn/xk/stdElectCourse!defaultPage.action',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'JSESSIONID=10BA4AB5C29AF570048A287B03757478; NSC_Xfc-DpoufouTxjudi-443=ffffffff096ca61a45525d5f4f58455e445a4a423660; SVRNAME=xk81',
}

data = {
  'optype': 'true',
  'operator0': '683550:true:0'
}


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://xk.fudan.edu.cn/xk/stdElectCourse^!batchOperator.action?profileId=1606', headers=headers, data=data)
def sendreq():
    global reqall
    backup=''
    turn=0
    while(1):
        if(stop):
            print(reqall)
            return
        response = requests.post('https://xk.fudan.edu.cn/xk/stdElectCourse!batchOperator.action?profileId=1606', headers=headers, data=data)
        ret=response.content[0:30]
        if(backup!=response.content):
            turn+=1
            if(turn==2):
                print(response.content)
                return
        backup=response.content
        print(ret.decode(encoding='utf-8',errors='ignore').strip())
        reqall+=1

stop=0
reqall=0
Nu=20
s=[threading.Thread(target=sendreq) for i in range(Nu)]
for i in range(Nu):
   s[i].start()
#s[0].start()
#time.sleep(5)
stop=1
