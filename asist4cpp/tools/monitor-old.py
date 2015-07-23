#!/usr/bin/env python
# encoding: utf-8
import time
import sys
import student_model
from pat_crawler import PAT_crawler
import argparse

def args_process():
#args process
    parser = argparse.ArgumentParser(prog="",description="A tool for cppLecture by ETAF")
    parser.add_argument("-f",action = 'store',dest = 'student_list_file',help='student_list_file',default = 'student_list.txt')
    return parser.parse_args()

def get_name_pwd_from_console():
    name = raw_input("please input the account: ")
    import getpass
    passwd = getpass.getpass('please input the password: ')
    return [name,passwd]
def main():

    EncodeType = sys.getfilesystemencoding()
    args = args_process()
    st_list = student_model.get_st_list(args.student_list_file)

    tmp = get_name_pwd_from_console()
    crawler = PAT_crawler(tmp[0],tmp[1])

    while crawler.logined() == False:
        print "login error! try your account and password again!\n"
        tmp = get_name_pwd_from_console()
        crawler.login(tmp[0],tmp[1])
    try:
        fp = open("result.txt","a+")
    except IOError:
        print "Error open result.txts error!"
        raw_input("Press Enter to continue......")
        sys.exit()
    print "===start testing,see the result in console or result.txt ======================\n"
    ip2ids = {}
    while True:
        try:
            for i in range(len(st_list)):
                current_ip = crawler.get_ip_by_name(st_list[i].id)
                if current_ip == "":
                    #never logined
                    continue

                #login
                if ip2ids.has_key(current_ip) == False:
                    ip2ids[current_ip] = []
                if ip2ids[current_ip].count(st_list[i])==0:
                    ip2ids[current_ip].append(st_list[i])
                    if current_ip!="127.0.0.1" and len(ip2ids[current_ip]) > 1:
                        content = "\n%s:---------one ip with multiple id ---------\n" % time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                        content = content + "ip:%s\n" % current_ip
                        content = content + "logined students:\n"+'\n'.join(str(tst) for tst in ip2ids[current_ip])
                        print content.decode('utf-8').encode(EncodeType)
                        fp.write(content)
                        fp.flush()

                llen = len(st_list[i].ips)
                if llen == 0:
                    st_list[i].ips.append(current_ip)
                else:
                    if st_list[i].last_ip != current_ip:
                        #different login ip detected
                        #print last ip and current ip
                        #print current ip has logined whos
                        #print this id has logined which ips
                        if st_list[i].ips.count(current_ip)==0:
                            st_list[i].ips.append( current_ip)
                        content = "\n%s:---------one id with multiple ip ---------\n" % time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                        content = content + str(st_list[i])+":\n"
                        content = content + "logined ip:\n"+'\n'.join(st_list[i].ips)
                        content = content + '\ncurrent_ip:'+current_ip
                        print content.decode('utf-8').encode(EncodeType)
                        fp.write(content)
                        fp.flush()
                st_list[i].last_ip = current_ip
        except KeyboardInterrupt:
            print "exting..."
            fp.close()
            print "bye"
            raw_input("Press Enter to continue......")
            sys.exit()

def start_monitor(st_list_filepath,user_name,user_pwd):
    st_list = student_model.get_st_list(st_list_filepath)
    crawler = PAT_crawler(user_name, user_pwd, "")

    try:
        fp = open("media/monitor_result.txt","a+")
    except IOError:
        print "Error open result.txts error!"

    print "===start testing,see the result in console or result.txt ======================\n"
    ip2ids = {}
    while True:
        try:
            for i in range(len(st_list)):
                current_ip = crawler.get_ip_by_name(st_list[i].id)
                if current_ip == "":
                    #never logined
                    continue

                #login
                if ip2ids.has_key(current_ip) == False:
                    ip2ids[current_ip] = []
                if ip2ids[current_ip].count(st_list[i])==0:
                    ip2ids[current_ip].append(st_list[i])
                    if current_ip!="127.0.0.1" and len(ip2ids[current_ip]) > 1:
                        content = "\n%s:---------one ip with multiple id ---------\n" % time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                        content = content + "ip:%s\n" % current_ip
                        content = content + "logined students:\n"+'\n'.join(str(tst) for tst in ip2ids[current_ip])
                        print content.decode('utf-8').encode(EncodeType)
                        fp.write(content)
                        fp.flush()

                llen = len(st_list[i].ips)
                if llen == 0:
                    st_list[i].ips.append(current_ip)
                else:
                    if st_list[i].last_ip != current_ip:
                        #different login ip detected
                        #print last ip and current ip
                        #print current ip has logined whos
                        #print this id has logined which ips
                        if st_list[i].ips.count(current_ip)==0:
                            st_list[i].ips.append( current_ip)
                        content = "\n%s:---------one id with multiple ip ---------\n" % time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                        content = content + str(st_list[i])+":\n"
                        content = content + "logined ip:\n"+'\n'.join(st_list[i].ips)
                        content = content + '\ncurrent_ip:'+current_ip
                        print content.decode('utf-8').encode(EncodeType)
                        fp.write(content)
                        fp.flush()
                st_list[i].last_ip = current_ip
        except KeyboardInterrupt:
            print "exting..."
            fp.close()
            print "bye"
            raw_input("Press Enter to continue......")
            sys.exit()


if __name__ == '__main__':
    main()

