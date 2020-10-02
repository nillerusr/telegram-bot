# -*- coding: utf-8 -*-
import requests,json,time,random,os,traceback,sys
from utils import *

main_funcs=['call', 'send', 'GetLP', 'ListenLP']
class vkmain:
	def __init__(self, token, id, is_group = False):
		self.token = token
		self.is_grp = is_group
		self.lp = None
		self.id = id

	def call(self, method, d={}, **args):
		param = {'v':'5.91','access_token':self.token}
		param.update(d)
		param.update(args)
		ret = requests.post('https://api.vk.com/method/'+method, data=param)
		return D(ret.json())

	def send(self, text, snd, fwd=0, attach=None, is_group=1):
		ln=len(text)
		if ln > 4096:
			mess=[]
			for i in range(int(ln/4096)+1):
				time.sleep(1)
				self.call('messages.send',peer_id=snd,message=text[i*4096:(i+1)*4096],random_id=random.randint(0,2**10))
			return True
		else: return self.call('messages.send',peer_id=snd,message=text,attachment=attach,random_id=random.randint(0,2**10))

	def GetLP( self ):
		try:
			if self.is_grp: self.lp = self.call('groups.getLongPollServer',v=5.84,lp_version=3,group_id=160560933)['response']
			else: self.lp = self.call('messages.getLongPollServer',v=5.84,lp_version=3)['response']
		except KeyError:
			print( self.lp['error']['error_msg'] )
			self.GetLP()
		except Exception:
			self.GetLP()

	def ListenLP( self ):
		try:
			ret=[]
			if self.is_grp:
				sv='%s?act=a_check&key=%s&ts=%s&wait=25&mode=2&version=3'%(self.lp['server'],self.lp['key'],self.lp['ts'])
				response = requests.post(sv).json()
				self.lp['ts']=response['ts']
				for result in response['updates']:
					if result['type'] == 'message_new' or result['type'] == 'message_edit':
						ret.append(result['object'])
			else:
				sv='http://%s?act=a_check&key=%s&ts=%s&wait=25&mode=2&version=3'%(self.lp['server'],self.lp['key'],self.lp['ts'])
				response = requests.post(sv).json()
				self.lp['ts']=response['ts']
				for result in response['updates']:
					ret.append(result)
			return retp

		except KeyboardInterrupt:
			exit('KeyboardInterrupt')
		except:
			#traceback.print_exc()
			self.GetLP( )
			return self.ListenLP( )

class VKApi:
	class _submethod:
		def __init__(self, vk , name):
			self._name = name
			self._vk = vk
		def __getattr__(self,name):
			def call(d = {},**args):
				d.update(args)
				return self._vk.call(self._name+'.'+name, d)
			return call
	def __init__(self, token, id=0, is_group = False):
		self._vk=vkmain( token, id, is_group )
	def __getattr__(self, name):
		if name in main_funcs:
			return getattr( self._vk, name)
		return self._submethod(self._vk, name)
