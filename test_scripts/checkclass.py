#coding=utf-8
'''
@Author: King
@Date: 2022-01-12 10:06:07
@Email: 13321998692@163.com
@Url: http://www.yydbxx.cn
'''
import requests
import json
import logging
import difflib
cookies = {
    'JSESSIONID': '67C6F57D78F54774DC634D3104799FEC'
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
while (1):
    res=requests.get('https://coursesel.umji.sjtu.edu.cn/tpm/findLessonTasks_ElectTurn.action?jsonString=%7B%22isToTheTime%22%3Atrue%2C%22electTurnId%22%3A%22A9E7F742-68FC-4E69-BBE3-E7B599C8FBE9%22%2C%22loadCourseGroup%22%3Atrue%2C%22loadElectTurn%22%3Atrue%2C%22loadCourseType%22%3Atrue%2C%22loadCourseTypeCredit%22%3Atrue%2C%22loadElectTurnResult%22%3Atrue%2C%22loadStudentLessonTask%22%3Atrue%2C%22loadPrerequisiteCourse%22%3Atrue%2C%22lessonCalendarWeek%22%3Afalse%2C%22loadLessonCalendarConflict%22%3Afalse%2C%22loadTermCredit%22%3Atrue%2C%22loadLessonTask%22%3Atrue%2C%22loadDropApprove%22%3Atrue%2C%22loadElectApprove%22%3Atrue%7D',headers=headers, cookies=cookies).content.decode(encoding='utf-8',errors='ignore')
    mdata=json.loads(res)
    mdata=mdata['data']['lessonTasks']
    for lesson in mdata:
        if(lesson['lessonClassCode'] == 'TH000SP2022-3'):
            cname=lesson['courseName']
            maxnum=lesson['maxNum']
            detail=lesson['lessonClassName']
            hasstu=lesson['studiedStudentNum']
            ori=cname+str(maxnum)+' '+str(hasstu)+' '+detail
            if(int(hasstu)<int(maxnum)):
                print('有英语课空闲：',ori)
        