#-*- coding: utf-8 -*-
import os, smtplib, time, datetime, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

gmail_user = "z331k7@gmail.com"
gmail_pwd = "tjdgus123" 
def send_gmail(to, subject, message, attach):
    msg = MIMEMultipart('alternative')
    msg['From'] = "alarm"
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText('<div>'+message+'</div>', 'html'))

    #이하 주석처리된 부분이 메일 첨부파일 발송을 위한 부분입니다. 첨부파일이 필요하시면 수정해서 쓰세요.
    #part=MIMEBase('application','octet-stream')
    #part.set_payload(open(attach, 'rb').read())
    #Encoders.encode_base64(part)
    #part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
    #msg.attach(part)

    mailServer=smtplib.SMTP("smtp.gmail.com",587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user,gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()
	

def mainLoop(): 
    #attach_file="send_mail.py"  <--------- 첨부파일 없으면 그대로 주석처리.
    message = sys.argv[1] if len(sys.argv)>1 else "sadfsdfasefwe ppppfsd fsdf aspdfjpaspjdpf ja"
    title= sys.argv[2] if len(sys.argv)>2 else "메일제목을 쓰2세요."
    destination = "chejun99@gmail.com"
    print "[" + str(datetime.datetime.now()) + "] Sending mail to " + destination + "..."
    print "message : " + message
    print "title : " + title
    send_gmail(destination, title, message, "")
    print "[" + str(datetime.datetime.now()) + "] Complete..."


if __name__ == "__main__":
    mainLoop()