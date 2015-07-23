from django.db import models

# Create your models here.

class Student(models.Model):
    st_num = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    teacher_name = models.CharField(max_length = 20)
    rand_id = models.CharField(max_length = 20)
    rand_pwd = models.CharField(max_length = 20)

class BadStudent(models.Model):
    st_num = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    teacher_name = models.CharField(max_length = 20)
    rand_id = models.CharField(max_length = 20)
    last_ip = models.CharField(max_length = 40)
    current_ip = models.CharField(max_length = 40)

class BadIP(models.Model):
    ip = models.CharField(max_length = 40)
    pre_st_num = models.CharField(max_length = 20)
    current_st_num = models.CharField(max_length = 20)
    pre_name = models.CharField(max_length = 20)
    current_name = models.CharField(max_length = 20)
