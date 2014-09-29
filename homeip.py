#!/usr/bin/env python

import urllib2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
import os

fromaddr = "xxxxx.com"
toaddr = "xxxxxx.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Pi IP Update"
ip = ""
while ip == "":
	try:
		ip = urllib2.urlopen('http://ip.42.pl/raw').read()
	except urllib2.URLError as err:
		ip = ""
		time.sleep(30)
body = "Hello from your Pi! \n My public IP is: " + ip
msg.attach(MIMEText(body, 'plain'))

while True:
	if os.path.exists('/usr/local/bin/pivpn/PiVPN.log'):
		log = open('/usr/local/bin/pivpn/PiVPN.log', 'r+').readline()
	else:
		log = "No PiVPN.log"
	print("log: " + log + " ip: " + ip)
	if ip != log:
		try:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login("EmailAddressxxxxxx.com", "Passwordxxxxxx")
			text = msg.as_string()
			server.sendmail(fromaddr, toaddr, text)
		except Exception:
			ip = "Couldn't send email!"
		log = open('/usr/local/bin/pivpn/PiVPN.log', 'w+')
		log.write(ip)
		log.close()
		print("Changed IP address in PiVPN.log!")
	else:
		print("Did not update PiVPN.log!")	
	curTime = time.clock()
	time.sleep(curTime + 3600)
