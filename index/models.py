from django.db import models


# Create your models here.

class Target(models.Model):
    id = models.AutoField(primary_key=True)
    target_name = models.CharField(max_length=255)
    main_host = models.CharField(max_length=255)
    remark = models.CharField(max_length=255)
    uptime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)


class Subdomain(models.Model):
    id = models.AutoField(primary_key=True)
    target_id = models.IntegerField()
    first_domain = models.CharField(max_length=67)
    sub_domain = models.CharField(max_length=67, unique=True)
    ip = models.CharField(max_length=20)
    ip_addr = models.CharField(max_length=100)
    remark = models.CharField(max_length=255)


class Ipinfo(models.Model):
    id = models.AutoField(primary_key=True)
    target_id = models.IntegerField()
    ip = models.CharField(max_length=20)
    host_state = models.CharField(max_length=5)
    port = models.IntegerField()
    protocol = models.CharField(max_length=10)
    port_state = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=100)


# C段目标表
class CTarget(models.Model):
    id = models.AutoField(primary_key=True)
    target_name = models.CharField(max_length=255)
    c_ip = models.CharField(max_length=20)
    remark = models.CharField(max_length=255)
    uptime = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

# C段IP 域名对应表
class CIpDomain(models.Model):
    id = models.AutoField(primary_key=True)
    target_id = models.IntegerField()
    ip = models.CharField(max_length=20)
    domain = models.CharField(max_length=67)
    remark = models.CharField(max_length=255)