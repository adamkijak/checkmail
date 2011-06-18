#!/usr/bin/pythonn
# -*- coding: UTF-8 -*-
from poplib import POP3_SSL
from email.header import decode_header
from re import findall,sub
from pickle import dumps,loads

USER = ''
PASSWORD = ''
HOST = ''

class Checkmail:

	def __init__(self,user,password,hostname,port=995):
		try:
			self._client = POP3_SSL(hostname,port)
			self._client.user(user)
			self._client.pass_(password)
		except Exception, e:
			print e	
		self.msgs = set([])

	def print_msg(self,msg_num):

		def header_decode(coded_header):
			header = coded_header	
			parts = findall('=\?.*\?=',header)
			for c in parts:
				decoded_header = decode_header(c)[0]
				header = sub('=\?.*\?=',decoded_header[0],header)
				header = unicode(header,decoded_header[1])
			return header
			
		msg = self._client.top(msg_num,0)[1]
		msg_date, msg_from, msg_subject = ('','','')
		for line in msg:
			if line.startswith('From:'):
				msg_from = header_decode(line)
			elif line.startswith('Subject:'):
				msg_subject = header_decode(line)
			elif line.startswith('Date:'):
				msg_date = line
		print '%s\n%s\n%s\n' % (msg_from,msg_subject,msg_date,)


	def check(self):
		uidl = self._client.uidl()
		msgs = map(lambda x: x.split(' ')[1], uidl[1])
		new_msgs = []
		msg_num = 1
		for uid in msgs:
			if not uid in self.msgs:
				new_msgs.append(msg_num)
			msg_num += 1
		self.msgs = set(msgs)
		for msg_num in new_msgs:
			self.print_msg(msg_num)

if  __name__ == '__main__':
	import sys
	import os
	reload(sys)
	sys.setdefaultencoding('utf-8')

	def save(data):
		file = open(os.path.abspath( __file__ ),'r')
		content = file.readlines()
		file.close()
		file = open(os.path.abspath( __file__ ),'w')
		in_data = False
		for line in content:
			if line.startswith('\tDATA = \'\'\''): 
				in_data=True
				file.write(line)
				file.write(data)
				file.write('\n\t\'\'\'\n')
			elif line.startswith('\t\'\'\''): 
				in_data=False
			elif in_data:
				pass
			else:
				file.write(line)
		file.close()
		
	def load():
		file = open(os.path.abspath( __file__ ),'r')
		content = file.readlines()
		file.close()
		data = ''
		in_data = False
		for line in content:
			if line.startswith('\tDATA = \'\'\''): 
				in_data=True
			elif in_data:
				data += line
			elif line.startswith('\t\'\'\''): 
				in_data=False
		return data
				
	checkmail = Checkmail(USER,PASSWORD,HOST)
	msgs = load().strip()[:-3]
	if msgs:
		checkmail.msgs = loads(msgs)
	checkmail.check()
	save(dumps(checkmail.msgs,0))
	DATA = '''
	'''
