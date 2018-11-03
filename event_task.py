#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/25 13:36
# @Author  : Fred Yang
# @File    : timed_task.py
# @Role    : 定时任务


from settings import EMAIL_INFO
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from database import db_session
from models import EventReminder


def send_mail(content, email):
    '''定义发送邮件'''
    # mail_to_list = ['xxx@xxxx.com', 'xxxx@qq.com']
    mail_to_list = [email]
    mail_host = EMAIL_INFO['host']
    mail_user = EMAIL_INFO['user']
    mail_password = EMAIL_INFO['password']
    subject = "%s: OpenDevOps平台事件提醒" % (time.ctime())
    msg = MIMEText(content, _subtype="html", _charset="gb2312")
    msg['Subject'] = subject
    msg['From'] = mail_user
    msg["To"] = ','.join(mail_to_list)

    try:
        mail = smtplib.SMTP()
        mail.connect(mail_host)
        mail.login(mail_user, mail_password)
        mail.sendmail(mail_user, mail_to_list, msg.as_string())
        mail.close()
        return True
    except (Exception,) as e:
        print(e)

def check_reminder_event():
    """
    用途：
        检查哪些事件需要进行邮件提醒
    逻辑：
        这里逻辑简单说明下如下：
        01. 先获取到所有事件的到期时间
        02. 获取所有事件中每条事件都需要提前多少天进行提醒
        03. 计算从哪天开始进行提醒（过期时间 - 提前提醒天数 = 开始提醒的日期）
        04. 计算出来的·开始提醒日期· <= 现在时间 都进行报警
    :return:
    """
    for event in db_session.query(EventReminder).all():
        print(event.name)
        now_time = datetime.datetime.now()  # 现在时间
        # 获取当天时间进行对比，是否触发报警机制（过期时间---提前时间 <= 现在时间  报警）
        start_reminder_time = event.expire_at - datetime.timedelta(days=int(event.advance_at))
        if start_reminder_time <= now_time:
            content = """
                    <!DOCTYPE html><html>
                    <head lang="en">
                    <meta charset="UTF-8">
                    <title></title>
                    <style type="text/css">
                        p {
                            width: 100%;
                            margin: 30px 0 30px 0;
                            height: 30px;
                            line-height: 30px;
                            text-align: center;

                        }
                        table {
                            width: 100%;
                            text-align: center;
                            border-collapse: collapse;
                        }

                        tr.desc {
                            background-color: gray;
                            height: 30px;
                        }
                        tr.desc td {
                            border-color: #ffffff;
                        }
                        td {
                            height: 30px;
                            border: 1px solid gray;
                        }
                    </style>
                    </head>
                    <body>"""

            content += """
                    <table>
                    <p>AiOps 事件提醒 </p>
                    <tr class='desc'>
                    <td>事件名称</td>
                    <td>事件内容</td>
                    <td>过期时间</td>
    
                    </tr>"""

            content += """
                    <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                     </tr>""".format(event.name, event.content, event.expire_at)
            content += """
                     </table>
                     </body>
                     </html>"""
            send_mail(content, event.email)

def exec_task():
    sched = BlockingScheduler()
    #sched.add_job(check_reminder_event, 'interval', seconds=30)   #每30s
    sched.add_job(check_reminder_event, 'interval', hours=1)    #每小时
    sched.start()

if __name__ == '__main__':
    exec_task()
