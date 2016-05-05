#coding:utf-8
import re
from bs4 import BeautifulSoup
import requests
import os
import sys
import getpass

s = requests.session()
headers_base = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'leetcode.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
        'Referer': 'https://leetcode.com/accounts/login/',
    }
login_data={}
code_lang = "cpp"

def bs(html_doc):
    page = BeautifulSoup(html_doc,"html.parser")
    prefix = 'https://leetcode.com'
    re = page.find_all(class_="ac")
    res ={}
    for item in re:
    	p = item.parent.parent
    	t = p.select('td')[2].select('a')[0]
    	questionName = t.string
    	questionUrl = prefix + t['href']
    	res[questionName] = questionUrl

    return res;

def generatefile(questionMap):
	if(os.path.exists('leetcode')==False):
		os.mkdir('leetcode')
	for k,v in questionMap.items():
		questionName = k.replace(' ','-')
		questionUrl = v
		f = open('leetcode/'+questionName+'.' + code_lang,'w')
		#print "line41" + str(f)
		#
		questionSubUrl = questionUrl + "submissions/"
		#questionSubUrl = questionSubUrl.replace(' ','-')
		#print questionSubUrl
		res = s.get(url=questionSubUrl,headers=headers_base)
		page = BeautifulSoup(res.content,"html.parser")
		ref = page.find(class_="status-accepted")
		#print re
		subUrl = 'https://leetcode.com' + ref['href']
		one = s.get(url=subUrl,headers=headers_base)
		html = one.content
		reg = r'submissionCode: \'(.*?)\''
		
		c = re.compile(reg)
		cc = re.findall(c,html)
		#content = cc[0].encode('utf-8')
		content = cc[0]
		#print content
		#print "line57\n"
		
		newcontent = uniToString(content)
		#print "line62" + newcontent
		f.write(newcontent)
		f.close()
		print questionName + " download successfully"
def uniToString(content):
	toCpp = {'\u000D':'\n','\u000A':'\n','\u003B':';','\u003C':'<','\u003E':'>','\u003D':'=','\u0026':'&','\u002D':'-','\u0022':'"','\u0009':'\t','\u0027':"'",'\u005C':'\\'}
	'''
	print toCpp
	print "line69\n"
	print content
	print "\nline71\n"
	'''
	for key in toCpp.keys():
		content = content.replace(key,toCpp[key])

	#print "line74" + content +'\n'
	return content

def login():
    url = "https://leetcode.com/accounts/login/"
    res = s.get(url=url,headers=headers_base)
    #print res.cookies
    login_data['csrfmiddlewaretoken']=res.cookies['csrftoken']
    print login_data
    res = s.post(url,headers = headers_base,data=login_data)
    #print res.status_code
    #print res.cookies
    return res.content
def mainpage():
    login()
    # res = s.get(url=url,headers=headers_base,cookies=login())
    # print res.text
    # write2file("hist.html",res.text)

if __name__ == '__main__':
	if(len(sys.argv)==1):
		login_data['login'] = "quitz@foxmail.com"
		login_data['password'] = "51323332"
	else:
		password = getpass.getpass()
		login_data['login'] = sys.argv[1]
		login_data['password'] = password

	generatefile(bs(login()))

	'''
	html = login()
	generatefile(bs(html))
	'''