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
# import json


# 163邮箱服务器地址
mail_host = 'smtp.163.com'
# 163用户名
mail_user = 'yydbxx99@163.com'
# 密码(部分邮箱为授权码)
mail_pass = 'expo2010'
# 邮件发送方邮箱地址
sender = 'yydbxx99@163.com'
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['linsy_king@sjtu.edu.cn','duanlingbosjtu@sjtu.edu.cn']

# 设置email信息
# 邮件内容设置
fisrttime = True


def sendemail(str):
    message = MIMEText(str+'\n\n提示：本内容是自动生成的', 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '选课通知'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = 'linsy_king@sjtu.edu.cn,duanlingbosjtu@sjtu.edu.cn'
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


class electsingle:
    def __init__(self, JSESSIONID, TURNID, COURSEID) -> None:
        self.ELECTTURNID = TURNID
        self.JSESSIONID = JSESSIONID
        self.COURSEID = COURSEID
        self.trynum = 0
        self.curerr = ''

    def run(self):
        cookies = {
            'JSESSIONID': self.JSESSIONID
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

        curdata = f'jsonString=%7B%22electTurnId%22%3A%22{self.ELECTTURNID}%22%2C%22autoElect%22%3Atrue%2C%22lessonTasks%22%3A%5B%22{self.COURSEID}%22%5D%7D'
        while(1):
            ts = time.time()
            realtime = int(round(ts * 1000))
            params = (
                ('_t', realtime),
            )
            self.trynum += 1
            try:
                response = requests.post('https://coursesel.umji.sjtu.edu.cn/tpm/doElect_ElectTurn.action',
                                            headers=headers, params=params, cookies=cookies, data=curdata, timeout=3)
            except:
                print("timeout")
                continue
            ret = response.content.decode(encoding='utf-8', errors='ignore')
            print(ret.strip())
            if(len(ret) > 1000):
                sendemail("账号过期，请重新设置JSESSIONID！")
                exit(0)
            if(str(ret).find("false") == -1):
                print("选课成功!")
                sendemail("选课成功，恭喜!")
                break
            self.curerr = str(ret)
            if(self.trynum % 300 == 0 or self.trynum == 1):
                self.sendreport()

    def sendreport(self):
        if self.trynum == 1:
            totrain = f'开始尝试...初次输出为：\n{self.curerr}'
        else:
            totrain = f'尝试5分钟，目前尝试第{self.trynum}次选课失败，继续尝试\n最近一次错误输出为：\n{self.curerr}'
        sendemail(totrain)


if __name__ == '__main__':
    qk = electsingle('ABE8B07F7B391C30003109016EAB1B2C',
                     '209E229F-7BC8-448F-A9D2-8DAAE2D89357', 'C9821C55-2950-459A-8DB9-454588C22F7B')
    qk.trynum=90001
    qk.run()
