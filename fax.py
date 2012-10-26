#-*- coding: utf-8 -*-

from ftplib import FTP
import time
import os

# Задача:
# 	1) получить с помощью модема и сторонней программы факс в электронном виде и сохранить на локальном компьютере;
#	2) с помощью этого скрипта передать на удаленный ftp сервер полученные через факс файлы которые там отсутствуют;
#	3) на удаленной машине расшарить ftp папку с факс-файлами для всех пользователей.
# Ход выполнения скрипта:
# 	1) необходимо получить список локальных файлов;
# 	2) потом подключится к удаленному ftp серверу;
# 	3) далее перейти в директорию факса на сервере и получить список удаленных файлов;
# 	4) сравнить списки, и отсутствующие на сервере файлы залить туда;
# 	5) скрипт кидать в планировщик и выполнять каждые 3 минуты.

ftp_host = ""
ftp_login = ""
ftp_pass = ""

remote_fax_path = ""
local_fax_path = ""

log_filename = ""

def logging(line, log_filename):
	f = open(log_filename,'a')
	f.write(time.ctime() + "  ===  " + line + "\n")
	f.close()

def send_file(filename, ftp):
	f = open(filename, 'rb')
	ftp.storbinary('STOR '+filename, f)

#get contents from local directory
os.chdir(local_fax_path)
_local_files = os.listdir(local_fax_path)

#connect
try:
	ftp = FTP(ftp_host)
	ftp.login(ftp_login, ftp_pass)
	logging("Connected to " + ftp_host, log_filename)
except:
	ll = "Failed to connect to " + ftp_host
	print(ll)
	logging(ll, log_filename)

#get contents from a remote directory
ftp.cwd(remote_fax_path)
_remote_files = ftp.nlst()

#compare lists
files_to_push = []
for ff in _local_files:
	if ff not in _remote_files:
		files_to_push.append(ff)

#push files
for filename in files_to_push:
	if os.path.isfile(filename):
		if filename == "Thumbs.db":
			continue
		print(filename)
		send_file(filename, ftp)

logging("Pushed files: " + str(files_to_push) + " to "+ftp_host, log_filename)

ftp.quit()
print("done")
