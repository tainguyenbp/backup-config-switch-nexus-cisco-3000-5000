import csv
import os
import paramiko
from datetime import datetime
from netmiko import ConnectHandler

def server_tftp():

    ip_server = "192.168.115.103"
    return ip_server

def get_ymd_currently():

    ymd = datetime.now()
    Ymd = ymd.strftime("%Y%m%d")
    return Ymd

def get_hms_currently():

    hms = datetime.now()
    HMS = hms.strftime("%H%M%S")
    return HMS

def get_hostname_device_via_netmiko():

    with open('server.csv', 'r') as open_file_csv:
        read_file_csv = csv.reader(open_file_csv, delimiter=',')

        next(open_file_csv)  # skip row header csv

        for row in read_file_csv:
            host = row[0]
            port = row[3]
            user = row[1]
            password = row[2]
    open_file_csv.close()

    cisco_nexus_5000 = {
        #"device_type": "autodetect",
        'device_type': 'cisco_ios',
        'ip': host,
        'username': user,
        'password': password,
        'port': port,
        'secret': 'secret default',
        'verbose': False,
    }

    net_connect = ConnectHandler(**cisco_nexus_5000)
    find_hostname = net_connect.find_prompt()
    hostname = find_hostname.replace("#","")
    return hostname
    net_connect.disconnect()

def copy_running_config():

    year_month_day = get_ymd_currently()
    hour_munites_second = get_hms_currently()

    return ('copy running-config ' + 'tftp://'+server_tftp()+'/'+get_hostname_device_via_netmiko()+'-running-config-'+year_month_day+'-'+hour_munites_second+' vrf default')

def copy_startup_config():
     year_month_day = get_ymd_currently()
     hour_munites_second = get_hms_currently()

     return ('copy startup-config ' + 'tftp://'+server_tftp()+'/'+get_hostname_device_via_netmiko()+'-startup-config-'+year_month_day+'-'+hour_munites_second+' vrf default')

def ssh_connect_backup_config_via_paramiko(host, port, user, password):

    try:
        ssh = paramiko.SSHClient()
        print('Start connect ssh to client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=user, password=password)

    # Backup running config

        copy_running_config_tftp = copy_running_config()
        print("Backup startup config to tftp server "+server_tftp()+" is starting ......")
        stidin,stdout,stderr = ssh.exec_command(copy_running_config_tftp)
    # In ra log vua thuc thi duoc tu cau lenh khi goi ham exec_command
        for line in iter(stdout.readline, ""):
            print(line, end="")

    # Backup startup config

        copy_startup_config_tftp = copy_startup_config()
        print("Backup running config to tftp server "+server_tftp()+" is starting ......")
        stidin,stdout,stderr = ssh.exec_command(copy_startup_config_tftp)
    # In ra log vua thuc thi duoc tu cau lenh khi goi ham exec_command
        for line in iter(stdout.readline, ""):
            print(line, end="")

        stidin.close()
        ssh.close()

    except Exception as e:
        print('Establish connection SSH to client failed !!!')
        print(e)


if __name__ == '__main__':

    if os.path.isfile('server.csv'):

        with open('server.csv', 'r') as open_file_csv:

            read_file_csv = csv.reader(open_file_csv, delimiter=',')

            next(open_file_csv)  # skip row header csv

            for row in read_file_csv:
                print('===================================================================================')
                host = row[0]
                print('Ip Switch:', host)
                port = row[3]
                print('Port Connect:', port)
                user = row[1]
                print('Username:', user)
                password = row[2]
                print('Password: secret')

                ssh_connect_backup_config_via_paramiko(host, port, user, password)
        open_file_csv.close()
    else:
        print('File server.csv not exists !!! ')