#coding=utf-8
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
import difflib


#163邮箱服务器地址
mail_host = 'smtp.163.com'  
#163用户名
mail_user = 'yydbxx99@163.com'  
#密码(部分邮箱为授权码) 
mail_pass = 'expo2010'   
#邮件发送方邮箱地址
sender = 'yydbxx99@163.com'  
#邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['linsy_king@sjtu.edu.cn','heyinong@sjtu.edu.cn']

#设置email信息
#邮件内容设置
fisrttime=True

def sendemail(str):
    message = MIMEText(str+'\n\n提示：本内容是自动生成的','plain','utf-8')
    #邮件主题       
    message['Subject'] = '选课变化通知' 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = 'linsy_king@sjtu.edu.cn,heyinong@sjtu.edu.cn'
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
        exit(0)

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


savedata=''
d=difflib.Differ()

while (1):
    res=requests.get('https://coursesel.umji.sjtu.edu.cn/tpm/findLessonTasks_ElectTurn.action?jsonString=%7B%22isToTheTime%22%3Atrue%2C%22electTurnId%22%3A%2223E9FE37-6EDB-4C22-ADA8-BF397210419E%22%2C%22loadCourseGroup%22%3Atrue%2C%22loadElectTurn%22%3Atrue%2C%22loadCourseType%22%3Atrue%2C%22loadCourseTypeCredit%22%3Atrue%2C%22loadElectTurnResult%22%3Atrue%2C%22loadStudentLessonTask%22%3Atrue%2C%22loadPrerequisiteCourse%22%3Atrue%2C%22lessonCalendarWeek%22%3Afalse%2C%22loadLessonCalendarConflict%22%3Afalse%2C%22loadTermCredit%22%3Atrue%2C%22loadLessonTask%22%3Atrue%2C%22loadDropApprove%22%3Atrue%2C%22loadElectApprove%22%3Atrue%7D',headers=headers, cookies=cookies).content.decode(encoding='utf-8',errors='ignore')
    mdata=json.loads(res)
    mdata=mdata['data']['lessonTasks']
    ori=[]
    for lesson in mdata:
        cname=lesson['courseName']
        maxnum=lesson['maxNum']
        detail=lesson['lessonClassName']
        hasstu=lesson['studiedStudentNum']
        ori.append(f'{cname} {detail}: 当前{hasstu}/{maxnum}')        
    ori.sort()
    ori='\n'.join(ori)
    if ori!=savedata and not fisrttime:
        diff=d.compare(ori.splitlines(),savedata.splitlines())
        changes = [l for l in diff if l.startswith('+ ') or l.startswith('- ')]
        concat='\n'.join(changes)
        sendemail(concat)
    savedata=ori
    fisrttime=False
    time.sleep(10)
        