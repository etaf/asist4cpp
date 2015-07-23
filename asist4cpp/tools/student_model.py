#!/usr/bin/env python
# encoding: utf-8
from collections import OrderedDict
class Submission(object):
    def __init__(self,problem_id,user_id,score,code_url):
        self.problem_id = problem_id
        self.user_id = user_id
        self.score = score
        self.code_url = code_url
        self.pass_filter = False
    def __cmp__(self,other):
        if self.score == other.score:
            return 0
        elif self.score < other.score:
            return -1
        else:
            return 1

class cppStudent(object):
    def __init__(self, id, name="", teacher_name="", rand_id=""):
        self.id = id
        self.name = name
        self.teacher_name=teacher_name
        self.ips=[]
        self.last_ip = ""
        self.scores = []
        self.score = 0
        self.rand_id = rand_id
        self.rand_pwd = ""
        self.submissions={} #highest score submission for each problem: key=problem_id , value = Submission
    def __str__(self):
        return "%s\t%s\t%s\t%s" % (self.id,self.name,self.teacher_name,self.rand_id)

import sys

def get_st_list(filename):
    try:
        fp = open(filename,"r")
    except IOError:
        print filename + " file does not exist!\nPlease put the file in the current directory!"
        #raw_input("Press Enter to continue......")
        #sys.exit()
        return
    st_list = []
    for line in fp.readlines():
        items = line.split()
        if(len(items) == 0):
            continue
        elif(len(items) == 1):
            st = cppStudent(items[0])
        elif len(items) == 2:
            st = cppStudent(items[0],items[1])
        elif len(items) == 3:
            st = cppStudent(items[0],items[1],items[2])
        elif len(items) >= 4:
            st = cppStudent(items[0],items[1],items[2],items[3])
        st_list.append( st)
    fp.close()
    return st_list



def get_st_dict(filename):
    st_list = get_st_list(filename)
    st_dict = OrderedDict()
    for st in st_list:
        st_dict[st.id] = st
    return st_dict


