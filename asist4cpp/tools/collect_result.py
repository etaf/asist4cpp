#!/usr/bin/env python
# encoding: utf-8

######################################
# By ETAF
# 生成分数表，包含考生每一题的最高分,并检测对于每一题是否包含关键字。保存到文件 final_scores.txt final_scores.xls
# 将每位考生的每一题的最高分代码保存到code文件夹.
######################################

from asist4cpp.tools.student_model import  get_st_dict
from asist4cpp.tools.pat_crawler import PAT_crawler
import xlwt
import os
import string

def write_xls(save_dir, st_dict, problems):

    book = xlwt.Workbook(encoding = "utf-8")
    sheet1 = book.add_sheet("final_codes")
    items = ["normal id","name","teacher","random id",'total_score']+problems

    for i in range(len(items)):
        sheet1.write(0,i,items[i])
    row = 1

    for st in st_dict.values():
        sheet1.write(row,0,st.id)
        sheet1.write(row,1,st.name)
        sheet1.write(row,2,st.teacher_name)
        sheet1.write(row,3,st.rand_id)
        sheet1.write(row,4,st.score)
        i = 0
        col_start =5
        for problem_id in problems:
            if problem_id in st.submissions:
                sheet1.write(row,i+col_start,str(st.submissions[problem_id].score)+' (pass_filter='+str(st.submissions[problem_id].pass_filter)+")")
                sheet1.write(row+1,i+col_start,st.submissions[problem_id].code_url)
            else:
                sheet1.write(row,i+col_start,"0 (pass_filter=False)")
                sheet1.write(row+1,i+col_start,"No submitted code")
            i = i+1
        row = row+2

    save_path = os.path.join(save_dir,"final_scores.xls")
    if os.path.exists(save_path):
        os.remove(save_path)
    book.save(save_path)
    print "result have been writen to final_scores.xls"
def get_name_pwd_from_console():
    name = raw_input("please input the account: ")
    import getpass
    passwd = getpass.getpass('please input the password: ')
    return [name,passwd]

import shutil
def save_codes(crawler,st_dict,parent_path):
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    else:
        shutil.rmtree(parent_path)

        pre_str = '''
            <link href="http://emil.fzu.edu.cn/s/application-f75b4427de2ad51cdb4f1abe37abcb68.css" media="screen" rel="stylesheet" type="text/css" />
            <script src="http://emil.fzu.edu.cn/s/application-929ef7194c12152f6707bc1d9a3efde7.js" type="text/javascript"></script>
            '''

    for st in st_dict.values():
        st_path = os.path.join(parent_path,st.teacher_name, st.id+"_"+st.name)
        if not os.path.exists(st_path):
            os.makedirs(st_path)
        for submission in st.submissions.values():
            submission_path = os.path.join(st_path, submission.problem_id +".html")
            page_html = crawler.get_code_page(submission.code_url)
            fp = open(submission_path,'w')
            print submission_path
            fp.write(pre_str+page_html)
            fp.close()

def main():
    st_dict = get_st_dict("norm2rand.txt")
    tmp = get_name_pwd_from_console()

    crawler = PAT_crawler(tmp[0],tmp[1])

    while crawler.logined() == False:
        print "login error! try your account and password again!\n"
        tmp = get_name_pwd_from_console()
        crawler.login(tmp[0],tmp[1])

    st_dict = crawler.get_submissions(st_dict)
    keywords_set = [ ['cin','cout'],['class'],['friend','class'],['operator','class'],['template'],['cout'],['class','virtual'],['class','virtual'] ]

    problems = [str(x+1001) for x in range(8)]
    tmp = {}
    for i in range(len(problems)):
       tmp[problems[i]] = keywords_set[i]


    #save_codes(crawler,st_dict)
    #return
    keywords_set = tmp
    print keywords_set
    for key in st_dict:
        for problem_id in problems:
            if problem_id in st_dict[key].submissions:
                st_dict[key].score = st_dict[key].score + st_dict[key].submissions[problem_id].score
                if crawler.code_filter(st_dict[key].submissions[problem_id].code_url,keywords_set[problem_id]) == True:
                    st_dict[key].submissions[problem_id].pass_filter = True


    write_xls(st_dict)
    save_codes(crawler,st_dict)

def collect_result(file_path, save_dir, user_name, user_pwd, keywords_set, problems_num, submission_url):
    st_dict = get_st_dict(file_path)
    crawler = PAT_crawler(user_name,user_pwd, submission_url)
    print "crawler start"
    st_dict = crawler.get_submissions(st_dict)
    print "crawler finished"
    problems = [x for x in string.ascii_uppercase][0:problems_num]
    tmp = {}
    for i in xrange(problems_num):
       tmp[problems[i]] = keywords_set[i]
    keywords_set = tmp

    print keywords_set
    for key in st_dict:
        for problem_id in problems:
            if problem_id in st_dict[key].submissions:
                st_dict[key].score = st_dict[key].score + st_dict[key].submissions[problem_id].score
                if crawler.code_filter(st_dict[key].submissions[problem_id].code_url,keywords_set[problem_id]) == True:
                    st_dict[key].submissions[problem_id].pass_filter = True
                    print key, problem_id
    print "filter finished"

    write_xls(save_dir, st_dict, problems)
    print "write xls finished"
    save_codes(crawler,st_dict, os.path.join(save_dir,"code") )
    print "save_code finished"
if __name__ == '__main__':
    main()
