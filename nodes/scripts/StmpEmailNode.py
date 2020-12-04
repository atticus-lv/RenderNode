import smtplib
from email.mime.text import MIMEText
from email.header import Header

import bpy

class SSM_OT_SendEmail(Operator):
    bl_idname = "ssm.send_email"
    bl_label = "Bug Reports to Author"

    smtp_server: StringProperty(
        name="SMTP Server",
        description="Something Like 'smtp.qq.com' or 'smtp.gmail.com'",
        default="")

    smtp_pass: StringProperty(
        name="SMTP Password",
        description="The SMTP Password for your receiver email", )

    content: StringProperty(
        name="Content", default="Write you want to reamain yourself")
    subject: StringProperty(
        name="Subject", default="Write your subject here")

    name: StringProperty(name="Name", default="")
    email: StringProperty(
        name="Name",
        description="Your sender email as well as your receiver email")

    def __init__(self):
        self.mail_host = self.smtp_server
        self.mail_pass = self.smtp_pass
        self.sender = self.email
        self.receivers = self.email

    def finish(self):
        self.name = ""
        self.subject = ""
        self.content = ""
        self.email = ""

    def send(self):
        message = MIMEText(self.content, 'plain', 'utf-8')

        message['From'] = Header(f"{self.name}<{self.email}>", 'utf-8')
        message['To'] = Header(f"Atticus<{self.sender}>", 'utf-8')

        subject = self.subject  # 发送的主题，可自由填写
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            return True
        except smtplib.SMTPException as e:
            print(f"Mail sent failed!!! \n{e}")
            return False

    def execute(self, context):
        if self.send():
            self.report({"INFO"}, "你的邮件已经被成功发送!" if CN_ON() else "Mail sent successfully!")
            self.finish()
        else:
            self.report({"INFO"}, "邮件发送失败!" if CN_ON() else "Mail sent failed!")
        return {'FINISHED'}