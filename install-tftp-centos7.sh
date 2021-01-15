#!/bin/bash

# Cài đặt TFTP Server trên CentOS 7
yum install tftp tftp-server xinetd -y

# Khởi tạo user dành riêng cho thư mục chứa dữ liệu phục vụ dịch vụ TFTP Server
useradd --no-create-home -s /sbin/nologin tftp
mkdir -p /tftpdata
chmod 777 /tftpdata
chown tftp:tftp -R /tftpdata

# Cấu hình file dịch vụ TFTP
cat << EOF > /etc/xinetd.d/tftp
service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        server_args             = -c -v -u tftp -p -U 117 -s /tftpdata
        disable                 = disable
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
}
EOF

# Khởi động dịch vụ TFTP
cat << EOF > /etc/systemd/system/tftp.service
[Unit]
Description=Tftp Server
Requires=tftp.socket
Documentation=man:in.tftpd

[Service]
ExecStart=/usr/sbin/in.tftpd -c -v -u tftp -p -U 117 -s /tftpdata
StandardInput=socket

[Install]
Also=tftp.socket
EOF

systemctl daemon-reload

systemctl start xinetd
systemctl start tftp

systemctl enable xinetd
systemctl enable tftp

