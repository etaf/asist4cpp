#!/usr/bin/env python
# encoding: utf-8
import time
#from asist4cpp.tools import student_model
#from asist4cpp.tools.pat_crawler import PAT_crawler
#from asist4cpp.models import BadStudent
#from asist4cpp.models import BadIP
import student_model
from pat_crawler import PAT_crawler
import sys
import argparse
from signal import *

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/lxa/www/asist/log/monitor.log',
                    filemode='a')

monitor_logger = logging.getLogger('monitor')
def args_process():
    parser = argparse.ArgumentParser(prog="",description="A tool for cppLecture by ETAF")
    parser.add_argument("-u",action = 'store', dest = 'username', required=True)
    parser.add_argument("-p",action = 'store', dest = 'password', required=True)
    return parser.parse_args()

def try_exit(signum, frame):
    monitor_logger.info("received signal:" + str(signum))
    print "Received signal: %d, Bye Bye ~~" % signum
    sys.exit(0)

def main():
    #for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    #for sig in ( SIGINT, SIGTERM):
        #signal(sig, try_exit)
    signal(SIGTERM, try_exit)
    args = args_process()
    st_list = student_model.get_st_list("./media/norm2rand.txt")
    crawler = PAT_crawler(args.username, args.password, "")
    try:
        fp = open("./media/monitor_result.txt","a+")
    except IOError:
        monitor_logger.error("Error open result.txts error!")
        print "Error open result.txts error!"

    print "===start testing,see the result in console or result.txt ======================\n"
    monitor_logger.info("start monitoring")
    ip2ids = {}
    try:
        while True:
#            print "hello"
            #fp.write("hello~ now: "+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))+"<br>")
            #fp.flush()
            #time.sleep(1)
            #continue
            for i in range(len(st_list)):
                current_ip = crawler.get_ip_by_name(st_list[i].rand_id)
                if current_ip == "":
                    #never logined
                    continue
                #login
                if ip2ids.has_key(current_ip) == False:
                    ip2ids[current_ip] = []
                if ip2ids[current_ip].count(st_list[i])==0:
                    ip2ids[current_ip].append(st_list[i])
                    #if current_ip!="127.0.0.1" and len(ip2ids[current_ip]) > 1:
                    if len(ip2ids[current_ip]) > 1:
                        content = "<div class='panel panel-warning'> <div class='panel-heading'> <h4 class='panel-title'>"
                        content = content + "%s: one ip with multiple students" % time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                        content = content + " </h4> </div> <div class='panel-body'>"
                        content = content + "ip: %s<br>" % current_ip
                        content = content + '<br>'.join(str(tst) for tst in ip2ids[current_ip])
                        content = content + " </div> </div> </div>"
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

                        content = "<div class='panel panel-danger'> <div class='panel-heading'> <h4 class='panel-title'>"
                        content = content + "%s: one stduent with multiple ip" % time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                        content = content + " </h4> </div> <div class='panel-body'>"
                        content = content + str(st_list[i])+":<br>"
                        content = content + "previous logined ip:<br>"+'<br>'.join(st_list[i].ips)
                        content = content + '<br>current logined_ip:'+current_ip
                        content = content + " </div> </div> </div>"
                        fp.write(content)
                        fp.flush()
                st_list[i].last_ip = current_ip
            time.sleep(1)
    except Exception as e:
          print e
          monitor_logger.error(str(e))
    finally:
        fp.close()
        monitor_logger.info("stop monitoring")
        print "Good Bye!"


if __name__ == '__main__':
    main()

