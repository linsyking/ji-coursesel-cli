#!/usr/bin/env python3
'''
@Author: King
@Date: 2022-12-30 12:00:08
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

import requests
import time
import threading
from rich.progress import Progress, SpinnerColumn, TextColumn


class ElectSingle:
    def __init__(self, JSESSIONID, TURNID, COURSEID: list, thread_number=3, max_try=None, course_desc: list = None) -> None:
        '''
        COURSEID: list of the ElectTurnLessonTaskID of courses
        thread_number: thred number for each course
        max_try: max try times
        course_desc: list of course description
        '''
        self.ELECTTURNID = TURNID
        self.COURSEID = COURSEID
        self.course_desc = course_desc
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
        # print(
        #     f"init: electturnid: {self.ELECTTURNID}, courses: {self.COURSEID}, trymax: {self.trymax}")
        print(f"using {thread_number} thread(s) for each course")

    def sendreq(self, data, taskid):
        while(1):
            if(self.stop):
                self.progress.update(
                    self.tasks[taskid], description="[white]" + self.course_desc[taskid] + ": [red]Maximum try times reached")
                return
            ts = time.time()
            if self.trymax and self.reqall >= self.trymax:
                self.stop = 1
                self.progress.update(
                    self.tasks[taskid], description="[white]" + self.course_desc[taskid] + ": [red]Maximum try times reached")
                return
            realtime = int(round(ts * 1000))
            params = (
                ('_t', realtime),
            )
            response = requests.post('https://coursesel.umji.sjtu.edu.cn/tpm/doElect_ElectTurn.action',
                                     headers=self.headers, params=params, cookies=self.cookies, data=data)
            ret = response.content.decode(encoding='utf-8', errors='ignore')
            if(len(ret) > 1000):
                # print("error")
                self.progress.log("Got error response. It's very likely that you are using expired JSESSIONID.")
                self.progress.update(
                    self.tasks[taskid], advance=1, description="[white]" + self.course_desc[taskid] + ": [red]Failed")
                return
            if(str(ret).find("false") == -1):
                # print("success, congrats")
                self.progress.update(
                    self.tasks[taskid], advance=1, description="[white]" + self.course_desc[taskid] + ": [green]Success")
                return
            # self.progress.log(ret.strip())
            self.progress.update(self.tasks[taskid], advance=1)
            self.reqall += 1

    def run(self):
        s = []
        self.tasks = []
        for id, courseid in enumerate(self.COURSEID):
            data = f'jsonString=%7B%22electTurnId%22%3A%22{self.ELECTTURNID}%22%2C%22autoElect%22%3Atrue%2C%22lessonTasks%22%3A%5B%22{courseid}%22%5D%7D'
            for _ in range(self.Nu):
                s.append(threading.Thread(
                    target=self.sendreq, args=(data, id,)))

        for i in range(len(s)):
            s[i].start()

        # Record run time
        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description} (tried: {task.completed})"),
            transient=False
        ) as progress:
            self.progress = progress
            for i in range(len(self.COURSEID)):
                if self.course_desc:
                    desc = self.course_desc[i]
                else:
                    desc = self.COURSEID[i]
                desc = f"[white]{desc}: Electing..."
                task = progress.add_task(desc, total=None)
                self.tasks.append(task)

            for i in range(len(s)):
                s[i].join()

        # Print run time
        print(f"All tasks ended in {time.time() - start_time} seconds.")
