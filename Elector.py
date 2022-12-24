#!/usr/bin/env python3
'''
@Author: King
@Date: 2022-12-23 23:49:52
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

import json

# Selector class


class JIEelector:
    def __init__(self, jsessionid: str) -> None:
        '''
        Set headers and cookies by jsessionid
        '''
        self.cookies = {
            'JSESSIONID': jsessionid
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

    def get_elect_turns(self):
        '''
        Get elect turns
        '''
        import requests
        response = requests.get('https://coursesel.umji.sjtu.edu.cn/tpm/findStudentElectTurns_ElectTurn.action',
                               headers=self.headers, cookies=self.cookies)

        all_turns = json.loads(response.text)

        if len(all_turns) == 0:
            print('No elect turn found.')
            exit(0)
        turn = all_turns[0]
        print(f"选课：{turn['electTurnName']}，模式：{turn['electModeName']}，开始时间：{turn['beginTime']}")
        return turn["electTurnId"]

    def get_all_courses(self, electurnid: str):
        '''
        Get all courses in a turn
        '''
        from prettytable import PrettyTable
        import requests

        response = json.loads(requests.get(f'https://coursesel.umji.sjtu.edu.cn/tpm/findLessonTasks_ElectTurn.action?jsonString=%7B%22isToTheTime%22%3Afalse%2C%22electTurnId%22%3A%22{electurnid}%22%2C%22loadCourseGroup%22%3Atrue%2C%22loadElectTurn%22%3Atrue%2C%22loadCourseType%22%3Atrue%2C%22loadCourseTypeCredit%22%3Atrue%2C%22loadElectTurnResult%22%3Atrue%2C%22loadStudentLessonTask%22%3Atrue%2C%22loadPrerequisiteCourse%22%3Atrue%2C%22lessonCalendarWeek%22%3Afalse%2C%22loadLessonCalendarConflict%22%3Afalse%2C%22loadTermCredit%22%3Atrue%2C%22loadLessonTask%22%3Atrue%2C%22loadDropApprove%22%3Atrue%2C%22loadElectApprove%22%3Atrue%7D', headers=self.headers, cookies=self.cookies).text)

        mdata = response['data']['lessonTasks']
        table = PrettyTable(['ID', '课程名称', '授课老师', '课程代码', '已报名人数'])

        for id, lesson in enumerate(mdata):
            cname = lesson['courseName']
            lclasscode = lesson['lessonClassCode']
            maxnum = lesson['maxNum']
            detail = lesson['lessonClassName']
            hasstu = lesson['studiedStudentNum']
            if 'lessonTaskTeam' in lesson:
                teacher = lesson['lessonTaskTeam']
            else:
                teacher = '未知'
            table.add_row([id, f'{detail}/{cname}', teacher,
                          lclasscode, f"{hasstu}/{maxnum}"])
        print(table)
        selected = input('请输入要选择的课程ID，用逗号隔开: ').split(',')
        table.clear_rows()

        if len(selected) == 0:
            print('未选择任何课程')
            return

        # Confirm

        print('您选择了以下课程：')

        selected_courses = [mdata[int(i)] for i in selected]

        for id, lesson in enumerate(selected_courses):
            cname = lesson['courseName']
            lclasscode = lesson['lessonClassCode']
            maxnum = lesson['maxNum']
            detail = lesson['lessonClassName']
            hasstu = lesson['studiedStudentNum']
            if 'lessonTaskTeam' in lesson:
                teacher = lesson['lessonTaskTeam']
            else:
                teacher = '未知'
            if lesson['electTurnId'] != electurnid:
                print('选课轮次不符合')
                return
            if 'electTurnLessonTaskId' not in lesson:
                print('该课程不可选')
                return
            table.add_row([id, f'{detail}/{cname}', teacher,
                          lclasscode, f"{hasstu}/{maxnum}"])
        print(table)

        # Export

        obj = {
            "jsessionID": self.cookies['JSESSIONID'],
            "electTurnId": electurnid,
            "courses": selected_courses
        }

        with open('.coursesel', 'w') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
        
        print('已保存到 .coursesel 文件')

    def run(self):
        '''
        Init
        '''
        turn = self.get_elect_turns()

        self.get_all_courses(turn)
