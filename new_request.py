import requests
from scrapy.http import HtmlResponse

def get_link():
    headers = {
        'authority': 'iasbano.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'referer': 'https://www.google.com/',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
        'cookie': 'PHPSESSID=d970c547db1be950aee16c9af6199ef4; _ga=GA1.2.706512715.1612284912; _gid=GA1.2.1930882388.1612284912; __gads=ID=06c316b8dde33f3c-2233b2cfe8c5006a:T=1612284911:RT=1612284911:S=ALNI_Mb7vUOJGddWGzIqz7RtHbocZAdGMw',
    }
    url = "https://iasbano.com/indian-express-upsc.php"
    response = requests.get(url,headers=headers,verify=False)
    response = HtmlResponse(url = url,body=response.text,encoding='utf-8')
    # /html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/a
    link = response.xpath("/html/body/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/a/@href").extract()
    return link
# with open('iasbano.html','w') as fp:
#     fp.write(response.text)

print(get_link())