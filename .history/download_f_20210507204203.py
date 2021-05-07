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
import time
from scrapy.http import HtmlResponse
# from google_drive_downloader import GoogleDriveDownloader as gdd


def get_link(url,date):
    
    response = requests.get(url)
    # with open('ff.html','w') as dp:
    #     dp.write(response.text)
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')

    # re = response.xpath(f'//*[@id="post-810"]/div/p/span/text()').extract()
    # print(re)
    # for i in range(1,15):
    #     try:
    #         re = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
    #         print(re)
    #         print(i)
    #     except:
    #         pass
        

    # link = response.xpath('//*[@id="post-810"]/div/p[13]/a/@href').extract()[0]
    # text = response.xpath('//*[@id="post-810"]/div/p[13]/text()').extract()[0]
    link = None
    for i in range(16,1,-1):
        try:
            text = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
            if date.strip().lower() in text.strip().lower():
                link = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/a/@href').extract()[0]
                print(link)
                break

        except Exception as e:
            print(e)

    if link is not None:
        f_link = link

        # response = requests.get(link)
        # # with open('ff.html','w') as dp:
        # #     dp.write(response.text)
        # response = HtmlResponse(url = link,body=response.text,encoding='utf-8')
        # f_link = response.xpath('//*[@id="iframe"]/@src').extract()[0]
        return f_link
    else:
        return 0
        # print(link)

    
    # return f_link
def get_link_1(url,date):

    headers = {
    'authority': 'www.careerswave.in',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
    'cookie': '__cfduid=ddad7bc73ee68465f10dda5074ac376681620399407; _ga=GA1.2.1463876823.1620399410; _gid=GA1.2.595933664.1620399410; __gads=ID=1c58b14dcb2ca70f-221950eedcc70072:T=1620399410:RT=1620399410:S=ALNI_MaMYuwfcNzd8kjYfGxMZHlBiXNc1Q',
}

    response = requests.get(url)
    with open('ff1.html','w') as dp:
        dp.write(response.text)
    
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')

    # re = response.xpath(f'//*[@id="post-810"]/div/p/span/text()').extract()
    # print(re)
    # for i in range(1,15):
    #     try:
    #         re = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
    #         print(re)
    #         print(i)
    #     except:
    #         pass
        

    # link = response.xpath('//*[@id="post-810"]/div/p[13]/a/@href').extract()[0]
    # text = response.xpath('//*[@id="post-810"]/div/p[13]/text()').extract()[0]
    link = None
    for i in range(16,1,-1):
        try:
            text = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/text()').extract()[0]
            if date.strip().lower() in text.strip().lower():
                link = response.xpath(f'//*[@id="post-810"]/div/p[{i}]/span/a/@href').extract()[0]
                print(link)
                break

        except Exception as e:
            print(e)

    if link is not None:

        response = requests.get(link)
        with open('ff.html','w') as dp:
            dp.write(response.text)
        response = HtmlResponse(url = link,body=response.text,encoding='utf-8')
        f_link = response.xpath('//*[@id="iframe"]/@src').extract()[0]
        return f_link
    else:
        return 0



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
def download_pdf():
    print("Checking paper availability..")
    url = "https://dailyepaper.in/indian-express-epaper/"
    url1 = "https://www.careerswave.in/the-indian-express-newspaper-download/"
    date = datetime.datetime.today().strftime('%d %b %Y')
    tdate = datetime.datetime.today().strftime('%d-%m-%Y')
    ydate = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    # date = "16 Apr 2021"
    # tdate = "16-04-2021"
    # url = get_link(url,date)
    url = get_link(url,date)
    if url !=0:
        # print("Paper found , downloading..")

        # print("downloading paper..."+"Newspaper_"+tdate+".pdf")
        # if not os.path.exists("Newspaper_"+tdate+".pdf"):
        #     try:
        #         os.remove('Newspaper_'+ydate+".pdf")
        #         print("Newspaper deleted of date: "+ydate)
        #     except:
        #         pass

    
        ############################DOWNLOAD###################################################
        # r = requests.get(url) 
        # with open("Newspaper_"+tdate+".pdf",'wb') as f: 


        #     f.write(r.content) 
        # print("sending email..."+" Newspaper_"+tdate+".pdf")
        
        ################################################################################

        send_mail("thecolossus018@gmail.com",["kumarisuruchi707@gmail.com","rsumit123@gmail.com","rpuja132@gmail.com","gogetmayank23@gmail.com"],date+" Indian Express","Greetings from Sumit's Bot , Find today's Indian Express paper here ==> ")
        send_mail("thecolossus018@gmail.com",["praachi.nk@gmail.com"],date+" Indian Express","Greetings from Sumit's Bot , Find today's Indian Express paper here ==>  "+url)
        return 1
    else:
        
        return 0

downloaded = 0
 
while downloaded == 0:
    downloaded = download_pdf()
    print("Paper not available yet, Trying again after 120 secs")
    time.sleep(150)
    


