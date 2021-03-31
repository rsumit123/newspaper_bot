import datetime
import requests 
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os
from scrapy.http import HtmlResponse
# from google_drive_downloader import GoogleDriveDownloader as gdd


def get_link(url,date):
    
    response = requests.get(url)
    with open('ff.html','w') as dp:
        dp.write(response.text)
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')

    re = response.xpath(f'//*[@id="post-810"]/div/p/span/text()').extract()
    print(re)
    for i in range(1,15):
        try:
            re = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
            print(re)
            print(i)
        
        

    # link = response.xpath('//*[@id="post-810"]/div/p[13]/a/@href').extract()[0]
    # text = response.xpath('//*[@id="post-810"]/div/p[13]/text()').extract()[0]
    link = None
    for i in range(16,5,-1):
        try:
            text = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/text()').extract()[0]
            if date.strip().lower() in text.strip().lower():
                link = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/a/@href').extract()[0]
                # print(link)
                break

        except Exception as e:
            print(e)

    if link is not None:

        response = requests.get(link)
        # with open('ff.html','w') as dp:
        #     dp.write(response.text)
        response = HtmlResponse(url = link,body=response.text,encoding='utf-8')
        f_link = response.xpath('//*[@id="iframe"]/@src').extract()[0]
        return f_link
    else:
        return 0
        # print(link)

    
    # return f_link
    

def send_mail(send_from, send_to, subject, message, files=[],
              server="smtp.gmail.com", port=587, username='thecolossus018', password='8877041257',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
##############################Downloading PDF###########################################3
url = "https://dailyepaper.in/indian-express-epaper/"
date = datetime.datetime.today().strftime('%d %b %Y')
tdate = datetime.datetime.today().strftime('%d-%m-%Y')
ydate = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')
# date = "15 Feb 2021"
# tdate = "15-02-2021"
url = get_link(url,date)
if url !=0:

    print("downloading paper..."+"Newspaper_"+tdate+".pdf")
    if not os.path.exists("Newspaper_"+tdate+".pdf"):
        try:
            os.remove('Newspaper_'+ydate+".pdf")
            print("Newspaper deleted of date: "+ydate)
        except:
            pass

 
    ############################DOWNLOAD###################################################
    r = requests.get(url) 
    with open("Newspaper_"+tdate+".pdf",'wb') as f: 


        f.write(r.content) 
    print("sending email..."+" Newspaper_"+tdate+".pdf")
    ################################################################################

    send_mail("thecolossus018@gmail.com",["rsumit123@gmail.com","rpuja132@gmail.com","gogetmayank23@gmail.com"],date+" Indian Express","Greetings from Sumit's Bot , Find today's Indian Express paper in attachment",files = ["Newspaper_"+tdate+".pdf"])
else:
    print("Paper not available yet")