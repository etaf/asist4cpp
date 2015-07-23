#!/usr/bin/env python
# encoding: utf-8

import string
import random
import xlwt
from student_model import get_st_list
import os
def get_rand_id(single_set,rand_str):
    
    #rand_id = 'cpp'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    rand_id = 'cpp'+''.join(random.choice(rand_str) for _ in range(8))
    while single_set.has_key(rand_id) :
        rand_id = 'cpp'+''.join(random.choice(rand_str) for _ in range(8))
    single_set[rand_id] = 1
    return rand_id

def get_rand_pwd(rand_str):
    return ''.join(random.choice(rand_str)for _ in range(6))

def write_xls(st_list, save_dir):

    book = xlwt.Workbook(encoding = "utf-8")
    sheet1 = book.add_sheet("norm2rand")

    items = ["学号","姓名","老师","帐号","密码"]

    for i in range(len(items)):
        sheet1.write(0,i,items[i])
    row = 1
    for st in st_list:
        sheet1.write(row,0,st.id)
        sheet1.write(row,1,st.name)
        sheet1.write(row,2,st.teacher_name)
        sheet1.write(row,3,st.rand_id)
        sheet1.write(row,4,st.rand_pwd)
        row+=1

    book.save(os.path.join(save_dir, "norm2rand.xls"))

    book = xlwt.Workbook(encoding = "utf-8")
    sheet1 = book.add_sheet("norm2rand4import")
    row = 0
    for st in st_list:
        sheet1.write(row,0,st.rand_id)
        sheet1.write(row,1,st.id)
        sheet1.write(row,2,st.rand_pwd)
        row+=1
    book.save(os.path.join(save_dir, "norm2rand4import.xls"))

def write_txt(st_list, save_dir):
    fp = open(os.path.join(save_dir, "norm2rand.txt"),'w')
    for st in st_list:
        fp.write("%s\t%s\t%s\t%s\t%s\n" %(st.id,st.name,st.teacher_name,st.rand_id,st.rand_pwd))
    fp.close()


def test_self(st_list):
    single_set = {}
    flag = True
    for st in st_list:
        if single_set.has_key(st.rand_id):
            print "Error : rand id not unique!"
            flag = False
            break;
        else:
            single_set[st.rand_id] = 1
    if flag:
        print "test self : OK!"

def main(input_filename, save_dir):
    st_list = get_st_list(input_filename)
    single_set = {}
    rand_str = "abcdefghijkmnpqrstwxy23456789"
    for i in range(len(st_list)):
        st_list[i].rand_id = get_rand_id(single_set,rand_str)
        st_list[i].rand_pwd = get_rand_pwd(rand_str)

    write_xls(st_list, save_dir)
    write_txt(st_list, save_dir)
if __name__ == '__main__':
    main("../../media/student_list.txt","../../media/")

