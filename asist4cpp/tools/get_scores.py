#!/usr/bin/env python
# encoding: utf-8
import sys
from student_model import get_st_list
from collections import OrderedDict
import string
import xlwt

def get_st_dict(st_list):
    st_dict = OrderedDict()
    for st in st_list:
        st_dict[st.rand_id] = st
        #st_dict[st.id] = st
    return st_dict
def get_scores(filename,st_dict):
    try:
        fp = open(filename,"r")
    except IOError:
        print filename + " not exit!"
        sys.exit()
    problem_num = 0
    for line in fp.readlines():
        items = line.split()
        rand_id = items[1]
        if not rand_id in st_dict:
            print "Error: rand_id "+rand_id+" from "+filename+" does not exist!"
            print items
            sys.exit()
        st_dict[rand_id].score = items[2]
        scores = []
        for i in range(3,len(items)):
            if items[i][0] == '(':
                scores[len(scores)-1]= ' '.join([scores[len(scores)-1],items[i]])
            else:
                scores.append(items[i])
        if problem_num == 0:
            problem_num = len(scores)
        else:
            if problem_num != len(scores):
                print "Error problem_num not unique!"
                sys.exit()
        st_dict[rand_id].scores = scores

    for key in st_dict:
        if len(st_dict[key].scores) == 0:
            st_dict[key].scores = ['-' for x in range(problem_num)]
            st_dict[key].score = 0

    return st_dict

def write_xls(st_dict):

    book = xlwt.Workbook(encoding = "utf-8")
    sheet1 = book.add_sheet("final_scores")
    problem_num = len(st_dict.values()[0].scores)
    items = ["normal id","name","teacher","random id","total score"]+[string.ascii_uppercase[x] for x in range(problem_num)]

    for i in range(len(items)):
        sheet1.write(0,i,items[i])
    row = 1

    for st in st_dict.values():
        sheet1.write(row,0,st.id)
        sheet1.write(row,1,st.name)
        sheet1.write(row,2,st.teacher_name)
        sheet1.write(row,3,st.rand_id)
        sheet1.write(row,4,st.score)
        for i in range(problem_num):
            sheet1.write(row,i+5,st.scores[i])

        row+=1
    book.save("final_scores.xls")
    print "result have been writen to final_scores.xls"


def main():

    st_list =  get_st_list('final_norm2rand.txt')
    st_dict = get_st_dict(st_list)
    st_dict = get_scores("scores.txt",st_dict)
    write_xls(st_dict)
if __name__ == '__main__':
    main()
