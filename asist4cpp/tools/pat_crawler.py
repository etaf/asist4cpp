#!/usr/bin/env python
# encoding: utf-8

import urllib
import urllib2
import cookielib
import re
from BeautifulSoup import BeautifulSoup
from student_model import Submission
#from asist4cpp.tools.comment_remover import comment_remover
from comment_remover import comment_remover
class PAT_crawler(object):

    host = "http://emil.fzu.edu.cn/"
    login_url = host + "users/sign_in"
    users_url = host + "users/"
    user_lookup_url = host + "users/lookup/"
    #submission_url = host+"contests/109/submissions/"


    def __init__(self,name,passwd,submission_url):
        user_agent ='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'
        self.http_header =  {'User-Agent':user_agent}
        self.login(name,passwd)
        self.submission_url = submission_url

    def logined(self):
        return self._logined

    def login(self,name,passwd):
        cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        post_values = {'user[handle]': name,
            'user[password]': passwd
            }
        post_values = urllib.urlencode(post_values)
        req = urllib2.Request(self.login_url,post_values,self.http_header)
        page_html = self.opener.open(req).read()
        tokens = re.findall('(登出)',page_html,re.S)
        if len(tokens) == 0:
            self._logined = False
        else:
            self._logined = True
            self.csrf_token = self.get_csrf_token()

    def get_csrf_token(self):
        req = urllib2.Request(self.users_url)
        page = self.opener.open(req).read()
        tokens = re.findall('<input name="authenticity_token" type="hidden" value="(.*?)" />',page,re.S)
        return tokens[0]

    def get_current_ip(self,page_html):
        current_ip = re.findall('当前IP.*?<td>(.*?)<',page_html,re.S)
        if len(current_ip)<1:
            return ""
        return current_ip[0]

    def get_ip_by_name(self,name):
        values = {'authenticity_token':self.csrf_token,
               'handle':name}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.user_lookup_url,data)
        try:
            page = self.opener.open(req).read()
            ip = self.get_current_ip(page)
        except Exception as e:
            print e
            return ""

        #if ip == "":
            #print name+" not found a ip\n"
        return ip

    def get_submissions(self,st_dict):
        print "----get submission start---"
        print self.submission_url
        print "sts:", st_dict
        page_num = 0
        while True:
            page_num = page_num + 1
            req = urllib2.Request(self.submission_url+"?page="+str(page_num))
            page_html = self.opener.open(req).read()
            soup = BeautifulSoup(page_html)
            table = soup.find('table')
            trs = table.findAll('tr')
            cnt = 0
            for i in xrange(1,len(trs)):
                if len(trs[i].attrs)>0:
                    continue
                cnt= cnt+1
                tds = trs[i].findAll('td')
                score = re.findall(r'.*>(.*)</a.*',str(tds[2]),re.S)
                if len(score) != 1:
                    print "Error when crwalering score"
                else:
                    score = int(score[0])

                problem_id = re.findall(r'.*>(.*)</a.*',str(tds[3]),re.S)
                problem_id = problem_id[0]

                code_url = re.findall(r'href="/(.*)".*',str(tds[4]),re.S)
                code_url = self.host+code_url[0]

                user_id = re.findall(r'.*>(.*)</a',str(tds[7]),re.S)
                user_id = user_id[0]
                print user_id, problem_id, code_url
                if not user_id in st_dict:
                    print "error! %s can not found in dict" % user_id
                    continue
                if problem_id in st_dict[user_id].submissions:
                    if score > st_dict[user_id].submissions[problem_id].score:
                        st_dict[user_id].submissions[problem_id] = Submission(problem_id,user_id,score,code_url)
                else:
                    st_dict[user_id].submissions[problem_id] = Submission(problem_id,user_id,score,code_url)

            if cnt == 0:
                break
        return st_dict

    def get_real_id(self,user_url):
       req = urllib2.Request(user_url)
       page_html = self.opener.open(req).read()
       real_id = re.findall(r'.*用户名.*<td>(.*)</td>.*昵称.*签名.*',page_html,re.S)
       return real_id[0]

    def get_all_submissions(self,submission_url):
       page_num = 0
       codes = {}
       while True:
           page_num = page_num + 1
           req = urllib2.Request(submission_url+"?page="+str(page_num))
           page_html = self.opener.open(req).read()
           soup = BeautifulSoup(page_html)
           table = soup.find('table')
           trs = table.findAll('tr')
           cnt = 0
           for i in range(1,len(trs)):
               if len(trs[i].attrs)>0:
                   continue
               cnt= cnt+1
               tds = trs[i].findAll('td')
               score = re.findall(r'.*>(.*)</a.*',str(tds[2]),re.S)
               if len(score) != 1:
                   print "Error when crwalering score"
               else:
                   score = int(score[0])

               problem_id = re.findall(r'.*>(.*)</a.*',str(tds[3]),re.S)
               problem_id = problem_id[0]
               code_url = re.findall(r'href="/(.*)".*',str(tds[4]),re.S)
               code_url = self.host+code_url[0]
               user_url = re.findall(r'href="/(.*)".*',str(tds[7]),re.S)
               user_url = self.host+user_url[0]
               user_id = self.get_real_id(user_url)

               if not user_id in codes:
                   codes[user_id] = []
               codes[user_id].append(code_url)

           if cnt == 0:
               break
       return codes

    def code_filter(self,code_url,keywords):
        req = urllib2.Request(code_url)
        page_html = self.opener.open(req).read()
        soup = BeautifulSoup(page_html)
        content = str(soup.find(id='sourceCode'))
        content = comment_remover(content)
        for keyword in keywords:
            items =  re.findall(r'.*('+keyword+').*',content,re.S)
            if len(items) == 0:
                return False
        return True
    def get_code_page(self,code_url):
        req = urllib2.Request(code_url)
        page_html = self.opener.open(req).read()
        return page_html


