#! usr/bin/python
#coding=utf-8 
__author__ = 'liuliang'
import urllib2
import sys
import bs4
import MySQLdb

# 全宋词爬取链接数据库
class DbPoem:
    # douban
    def __init__(self, indexurl):
        self.indexurl = indexurl
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.typecode = sys.getfilesystemencoding()
    def getContent(self, url):
        try:
            request = urllib2.Request(url)
            content = urllib2.urlopen(request).read()
            return content
        except Exception, e:
            print "error:",e

    def getPoemList(self, url):
        # 获取首页内容
        content = self.getContent(url)
        soup = bs4.BeautifulSoup(content, "html.parser",  from_encoding="gb18030")
        # print content
        poemlist = soup.find_all("a")
        return poemlist

    def getPoemInfo(self, url):
        print url
        content = self.getContent(url)
        if(content):
            soup = bs4.BeautifulSoup(content, "html.parser",  from_encoding="gb18030")
            # 诗词内容
            cont = {"title":"", "content":""}
            cont['title'] = soup.find("title").get_text()
            cont["content"] = soup.find("div", id="cont").get_text()
            print cont["content"]
            return cont
    def writePoemBySql(self, cont):
        conn = MySQLdb.connect(host="localhost", port=3306, user='', passwd='', db='', charset="utf8")
        cur = conn.cursor()
        cur.execute("insert into poem(title,content) value(%s, %s)",[cont["title"].encode('utf-8'), cont["content"].encode('utf-8')])
        conn.commit()
        cur.close()
        conn.close()

indexurl = "http://wenxian.fanren8.com/11/9"
url = "http://wenxian.fanren8.com"
dbpoem = DbPoem(indexurl)
poemlist = dbpoem.getPoemList(indexurl)
length = len(poemlist)
x = 0;
for poem in poemlist:
    x = x+1
    if(x<=3):
        continue
    if(x>=length-3):
        continue
    cont = dbpoem.getPoemInfo(url+poem["href"])
    dbpoem.writePoemBySql(cont)






        





