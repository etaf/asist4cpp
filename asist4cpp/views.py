from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.
from django.http import HttpResponse
from django.core import serializers
from tools import norm2rand
import json
from asist4cpp.models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import logging
from django.conf import settings
logger = logging.getLogger('asist4cpp')
DEBUG = settings.DEBUG
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required(login_url='/asist4cpp/login/')
def index(request):
    return render_to_response('asist4cpp/index.html', {'st_list' : Student.objects.all() }, context_instance=RequestContext(request))
    #return render(request, 'asist4cpp/index.html')
def collect(request):
    return render(request,'asist4cpp/collect.html')

from django.http import StreamingHttpResponse
def file_iterator(file_name, chunk_size=512):
    try:
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    except IOError as e:
        logger.error(e)

@login_required(login_url='/asist4cpp/login/')
def download_norm2rand(request):
    if request.GET['type'] == '0':
        filename = 'norm2rand.xls'
    else:
        filename = 'norm2rand4import.xls'

    logger.info("try download " + filename +" " + get_client_ip(request))
    response = StreamingHttpResponse(file_iterator("media/"+ filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    logger.info("download successfully " + get_client_ip(request))
    return response


@login_required(login_url='/asist4cpp/login/')
def upload_student_list(request):
    logger.info("try upload " + request.FILES['file'].name + " " + get_client_ip(request))
    if not request.FILES['file'].name.endswith('.txt'):
        logger.info("upload failed " + request.FILES['file'].name + " " +get_client_ip(request))
        return HttpResponse(
            json.dumps({'success': False}),
            content_type="application/json"
        )
    handle_uploaded_file(request.FILES['file'])
    logger.info("upload successfully "+request.FILES['file'].name +" " + get_client_ip(request))
    return HttpResponse(
        json.dumps({'success': True}),
        content_type="application/json"
    )

def handle_uploaded_file(f):
    with open('./media/student_list.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required(login_url='/asist4cpp/login/')
def generate_norm2rand(request):
    norm2rand.main("./media/student_list.txt","./media" )
    save_st_list_to_db()
    return HttpResponse(
        json.dumps({'message':'Completed'}),
        content_type="application/json"
    )

def save_st_list_to_db():
    Student.objects.all().delete()
    try:
        fp = open("media/norm2rand.txt","r")
    except IOError as e:
        logger.error(e)
        return
    for line in fp.readlines():
        items = line.split()
        st = Student(st_num = items[0], name= items[1], teacher_name = items[2], rand_id = items[3], rand_pwd = items[4] )
        st.save()
    fp.close()


from tools.collect_result import collect_result
import re

@login_required(login_url='/asist4cpp/login/')
def start_collect(request):
    """ajax start collect """
    problem_num = int(request.POST['problem_num'])
    submission_url = request.POST['submission_url']
    keywords_set = []
    for i in xrange(problem_num):
        problem_id = "problem_%d" % i
        if problem_id in request.POST:
            keywords_set.append((request.POST[problem_id]).split())
        else:
            keywords_set.append([])
    submission_url_pattern = re.compile(r'http:\/\/emil\.fzu\.edu\.cn\/contests\/\d*\/submissions\/*')
    if not submission_url_pattern.match(submission_url):
        return HttpResponse(
            json.dumps({'success':False , 'message':'submission_url error!'}),
            content_type="application/json"
        )
    collect_result("./media/norm2rand.txt", "./media","admin", "nimda", keywords_set, problem_num, submission_url )
    return HttpResponse(
        json.dumps({'success' : True, 'message':'Completed! Please download the result file.'}),
        content_type="application/json"
    )

import os

@login_required(login_url='/asist4cpp/login/')
def download_result(request):
    filename = "final_result.7z"
    filepath = os.path.join("media",filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    os.system("7z a  "+filepath+" media/code media/final_scores.xls")
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    logger.info("download " + get_client_ip(request))
    return response



import psutil
def is_monitor_on(request):
    if DEBUG:
        print "checking monitor on/off"
    try:
        for proc in psutil.process_iter():
            cmd = proc.cmdline()
            if len(cmd)>2 and cmd[1] == "./asist4cpp/tools/monitor.py":
                if DEBUG:
                    print "on"
                return True
    except Exception, e:
        print e
        logger.error(str(e)+" "+ get_client_ip(request))
    if DEBUG:
        print "off"
    return False


def stop_monitor(request):
    logger.info("try stop " + get_client_ip(request))
    try:
        for proc in psutil.process_iter():
            cmd = proc.cmdline()
            #print cmd
            if len(cmd)>2 and cmd[1] == "./asist4cpp/tools/monitor.py":
                proc.terminate()
    except Exception, e:
        logger.error(str(e)+" "+ get_client_ip(request))

    logger.info("stop successfully " + get_client_ip(request))

import subprocess
def start_monitor(request):
    if DEBUG:
        print "starting monitor"
    if is_monitor_on(request):
        return True

    logger.info("try start " + get_client_ip(request))
    try:
        subprocess.Popen(["./asist4cpp/tools/monitor.py", "-u", request.session['username'], "-p", request.session['password']], close_fds = True )
    except Exception, e:
        print e
        logger.error(str(e)+" "+ get_client_ip(request))
        return False
    else:
        if DEBUG:
            print "started"
        logger.info("start successfully " + get_client_ip(request))
        return True

def clear_monitor(request):
    if is_monitor_on(request):
        return;
    logger.info("try clear " + get_client_ip(request))
    try:
        fp = open("./media/monitor_result.txt","w")
    except IOError:
        logger.error( "open monitor_result.txt error! " + get_client_ip(request))
        return
    fp.write("")
    fp.close()
    logger.info("clear successfully " + get_client_ip(request))
    return;

@login_required(login_url='/asist4cpp/login/')
def switch_monitor(request):
    if request.GET['switch'] == 'on':
        start_monitor(request)
    elif request.GET['switch'] == 'off':
        stop_monitor(request)
    elif request.GET['switch'] == 'clear':
        clear_monitor(request)
    return HttpResponse(
        json.dumps({'success': True}),
        content_type="application/json"
    )

def update_monitor_table(request):
    try:
        fp = open("./media/monitor_result.txt","r")
    except IOError:
        print "open monitor_result.txt error!"
        return
    data = {}
    data['data'] = fp.read()
    #data['data'] = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))+" : hello!"

    fp.close()
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )

@login_required(login_url='/asist4cpp/login/')
def monitor(request):
    state  = is_monitor_on(request)
    return render_to_response('asist4cpp/monitor.html', {'state' : state })


def my_login(request):
    if (not 'username' in request.POST) or (not  'password' in request.POST):
        return render(request, 'asist4cpp/login.html')
    username = request.POST['username']
    password = request.POST['password']
    request.session['username'] = username
    request.session['password'] = password
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return  HttpResponseRedirect('/asist4cpp')
    else:
        return render(request, 'asist4cpp/login.html')

def my_logout(request):
    logout(request)
    stop_monitor(request)
    return HttpResponseRedirect('/asist4cpp/login')

