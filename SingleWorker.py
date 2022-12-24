# coding=utf-8
import requests
import time
import threading


class ElectSingle:
    def __init__(self, JSESSIONID, TURNID, COURSEID: list, thread_number=10, max_try=None) -> None:
        '''
        COURSEID: list,所有课程
        thread_number: 对每个课程分配的线程个数
        '''
        self.ELECTTURNID = TURNID
        self.COURSEID = COURSEID
        self.trymax = max_try
        self.stop = 0
        self.reqall = 0
        self.Nu = thread_number
        self.cookies = {
            'JSESSIONID': JSESSIONID
        }
        self.headers = {
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
        print(f"init: electturnid: {self.ELECTTURNID}, courses: {self.COURSEID}")
        print(f"using {thread_number} threads for each course")

    def sendreq(self, data):
        while(1):
            if(self.stop):
                # print(self.reqall)
                return
            ts = time.time()
            if self.trymax and self.reqall >= self.trymax:
                self.stop = 1
                # print(ts-self.start_time)
            realtime = int(round(ts * 1000))
            params = (
                ('_t', realtime),
            )
            response = requests.post('https://coursesel.umji.sjtu.edu.cn/tpm/doElect_ElectTurn.action',
                                     headers=self.headers, params=params, cookies=self.cookies, data=data)
            ret = response.content.decode(encoding='utf-8', errors='ignore')
            if(len(ret) > 1000):
                print("error")
                exit()
            if(str(ret).find("false") == -1):
                print("success, congrats")
                self.stop = 1
                return
            print(ret.strip())
            self.reqall += 1

    def run(self):
        s = []
        for i in self.COURSEID:
            data = f'jsonString=%7B%22electTurnId%22%3A%22{self.ELECTTURNID}%22%2C%22autoElect%22%3Atrue%2C%22lessonTasks%22%3A%5B%22{i}%22%5D%7D'
            for _ in range(self.Nu):
                s.append(threading.Thread(target=self.sendreq, args=(data,)))
        for i in range(len(s)):
            s[i].start()
        self.start_time = time.time()
        for i in range(len(s)):
            s[i].join()
        print("end")


if __name__ == '__main__':
    mel = ElectSingle('822F840D86C7C8BAC7D03DB88CB05571',
                      'D953358F-8716-46EA-A3F7-A7D7AACA1057', ['404FC4DB-2004-4CE9-8D1E-5AF0534FCB53'], 5)
    '''
    示例说明：第一个参数是Jsesseion id.注意要运行脚本前十分钟内获取最好，以免运行时失效。
    第二个参数是Electurn ID
    第三个参数是Course ElectTurnLessonTaskID的List
    第四个参数可选，表示对每个课程分配多少的线程
    '''
    mel.run()