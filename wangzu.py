# coding=utf-8
import requests
import time
ts = time.time()
realtime = int(round(ts * 1000))

cookies = {
    'JSESSIONID': '22A55C48F573607E39173FE44B9F47FF'
}

ELECTTURNID = 'D83A10A9-0913-4061-AF5C-48EF250B41FA'

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


def addcourse(lesson):
    global mydata
    mydata.append(
        f'jsonString=%7B%22electTurnId%22%3A%22{ELECTTURNID}%22%2C%22autoElect%22%3Atrue%2C%22lessonTasks%22%3A%5B%22{lesson}%22%5D%7D')


mydata = []

addcourse('46B3DFD9-E2BD-4172-916B-5DCA09CA94A4')
while(1):
    response = requests.post('https://coursesel.umji.sjtu.edu.cn/tpm/doElect_ElectTurn.action',
                             headers=headers, params=params, cookies=cookies, data=mydata[0])
    ret = response.content.decode(encoding='utf-8', errors='ignore')
    print(ret.strip())
    if(str(ret).find("false") == -1):
        print("选课成功!")
        break
