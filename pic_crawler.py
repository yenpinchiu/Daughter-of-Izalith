import urllib.request,urllib.parse,random,time

url = 'ooo'

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
          'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
          (KHTML, like Gecko) Element Browser 5.0', \
          'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
          'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
          'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
          'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
          Version/6.0 Mobile/10A5355d Safari/8536.25', \
         'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
         Chrome/28.0.1468.0 Safari/537.36', \
         'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']


page_line = str(urllib.request.urlopen(url).read().decode("utf-8")).split('\n')


for line in page_line:
    if 'xxx' in line:
        pic_url = line.split('href=\"')[1].split('\">')[0]
        request = urllib.request.Request(pic_url)
        index = random.randint(0, 9)
        user_agent = user_agents[index]
        request.add_header('User-agent', user_agent)
        response = urllib.request.urlopen(request)
        html = response.read()
        f = open(pic_url.split('avmodel/')[1],'wb')
        f.write(html)
        f.close()
        print(pic_url)
        time.sleep(2)
