from urllib.parse import unquote
import requests, re

match_gtag = re.compile(r'<a [^>]*>')
match_gurl = re.compile(r'imgurl=(.*?)&imgrefurl')
HEADERS_GOOGLE = {'User-Agent':'LG8700/1.0 UP.Browser/6.2.3.9 (GUI) MMP/2.0'}

def search_images( query ):
	page=requests.get('https://www.google.com/search',{'q':query,'source':'lnms','tbm':'isch'},headers=HEADERS_GOOGLE).text
	tags = match_gtag.findall(page)
	images=[]
	for i in tags:
		url=i.replace('&amp;','&')
		f=match_gurl.findall(url)
		try:
			images.append(unquote(f[0]))
		except:
			continue
	return images
