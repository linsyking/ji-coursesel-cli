# coding=utf-8
'''
@Author: King
@Date: 2022-01-12 10:06:07
@Email: 13321998692@163.com
@Url: http://www.yydbxx.cn
'''
import requests
import time

import smtplib
from email.mime.text import MIMEText
import json

# 163邮箱服务器地址
mail_host = 'smtp.163.com'
# 163用户名
mail_user = 'yydbxx99@163.com'
# 密码(部分邮箱为授权码)
mail_pass = 'expo2010'
# 邮件发送方邮箱地址
sender = 'yydbxx99@163.com'
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['linsy_king@sjtu.edu.cn']

# 设置email信息
# 邮件内容设置
fisrttime = True


def sendemail(str):
    message = MIMEText(str+'\n\n提示：本内容是自动生成的', 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '选课变化通知'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = 'linsy_king@sjtu.edu.cn'
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误
        exit(0)


cookies = {
    'JSESSIONID': 'DAAD90AF0C2EA7629D0AD09B277A36A1'
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

carelesson = ['ECE2150JFA2022-1']

electurnid = "D953358F-8716-46EA-A3F7-A7D7AACA1057"

while (1):
    res = requests.get(f'https://coursesel.umji.sjtu.edu.cn/tpm/findLessonTasks_ElectTurn.action?jsonString=%7B%22isToTheTime%22%3Atrue%2C%22electTurnId%22%3A%22{electurnid}%22%2C%22loadCourseGroup%22%3Atrue%2C%22loadElectTurn%22%3Atrue%2C%22loadCourseType%22%3Atrue%2C%22loadCourseTypeCredit%22%3Atrue%2C%22loadElectTurnResult%22%3Atrue%2C%22loadStudentLessonTask%22%3Atrue%2C%22loadPrerequisiteCourse%22%3Atrue%2C%22lessonCalendarWeek%22%3Afalse%2C%22loadLessonCalendarConflict%22%3Afalse%2C%22loadTermCredit%22%3Atrue%2C%22loadLessonTask%22%3Atrue%2C%22loadDropApprove%22%3Atrue%2C%22loadElectApprove%22%3Atrue%7D', headers=headers, cookies=cookies).content.decode(encoding='utf-8', errors='ignore')
    mdata = json.loads(res)
    mdata = mdata['data']['lessonTasks']
    ori = []
    for lesson in mdata:
        if(lesson['lessonClassCode'] in carelesson):
            cname = lesson['courseName']
            maxnum = lesson['maxNum']
            detail = lesson['lessonClassName']
            hasstu = lesson['studiedStudentNum']
            ori = f'{detail}：共{maxnum}名额，当前{hasstu}学生'
            if(int(hasstu) > 100):
                sendemail(ori)
                exit(0)
    time.sleep(5)
