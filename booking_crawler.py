import urllib.request

url = "http://www.booking.com/reviewlist.zh-cn.html?sid=da567f1d05a564c8d0b9deae82944d2c;dcid=1;cc1=tw;dist=1;pagename=the-treehouse;type=total&;offset=390;rows=10"
req = urllib.request.Request(url, headers = {"Referer": "http://www.booking.com", "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24" })
page = str(urllib.request.urlopen(url = req, timeout = 10).read().decode("utf-8"))
print(page)
