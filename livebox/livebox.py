#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

import getpass

# Livebox.login()              Authentification session utilisateur
# Livebox.logout()             Fermeture session
# Livebox.listTrunks()         Information téléphonie IP
# Livebox.getIPTVStatus()      Etat IP TV
# Livebox.getDSLStats()        Stats DSL (Erreurs)
# Livebox.getMIBs()            Information lien dsl
# Livebox.getWifiMIBs()        Information Wifi
# Livebox.getWANStatus()       Etat de la connexion WAN
# Livebox.reboot()             Redémarrage la livebox
# Livebox.setwifi(mode)        Active/désactive le Wifi
# Livebox.filtreMAC(flag)      Active/Désactive filtrage MAC address
# Livebox.getWificomStatus()   Information Wifi public Orange



class Livebox:

	def __init__(self,url_prefix='https://livebox'):
		self._url_prefix = url_prefix



	def login(self):
	
		password=getpass.getpass()
	
		url_login = "%s/authenticate?username=admin&password=%s" % (self._url_prefix,password)
	
		values = {'username' : 'admin',
	          	'password' : password }
	
		data = urllib.urlencode(values)
		req = urllib2.Request(url_login, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		
		datas = json.loads(the_page)
		
		self._cookies=response.info()['Set-Cookie'].split(';')[0]
		self._contextID = datas['data']['contextID']
	

	def _sysbus(self,question):
		return self._request("%s/sysbus/%s" % (self._url_prefix,question)
			, '{"parameters":{}}' )

	def _ws(self, params):
		return self._request("%s/ws" % (self._url_prefix)
			, params , 'application/x-sah-event-2-call+json; charset=UTF-8')

	def _request(self,url, params, content_type='application/json'):
	

		print '#--------------------------------------------------------------------'
		print "%s ( %s )" % (url,params)
		print '#--------------------------------------------------------------------'

			
		req = urllib2.Request(url, params)
		req.add_header('Cookie', self._cookies)
		req.add_header('X-Context', self._contextID)
		req.add_header('X-Sah-Request-Type', 'idle')
		req.add_header('Content-Type', content_type)
		req.add_header('X-Requested-With', 'XMLHttpRequest')
	
		response = urllib2.urlopen(req)
		the_page = response.read()
	
		return json.loads(the_page)



	def logout(self):
        	urllib2.urlopen("%s/logout" % (self._url_prefix))
		return ''

	def list_trunks(self):
		'''Information téléphonie IP'''
		return self._sysbus('VoiceService/VoiceApplication:listTrunks')

	def ip_tv_status(self):
	      	'''Etat IP TV'''
		return self._sysbus('NMC/OrangeTV:getIPTVStatus')

	def dsl_stats(self):
	        '''Stats DSL (Erreurs)'''
		pass

	def mibs(self):
		'''Information lien dsl'''
		pass

	def wifi_com_status(self):
		'''Information Wifi public Orange)'''
		return self._sysbus('Wificom:getStatus')

	def wiwi_mibs(self):
		'''Information Wifi'''
		pass

	def wan_status(self):
		'''Etat de la connexion WAN'''
		return self._sysbus('NMC:getWANStatus')

	def reboot(self):
		'''Redémarrage la livebox'''
		pass

	def wifi(self,mode):
		'''Active/désactive le Wifi'''
		pass

	def filtre_mac(self,flag):
		'''Active/Désactive filtrage MAC address'''
		pass

	def connectivity_enable_notifications(self):
		return self._sysbus('sah/hgw/models/Connectivity:enableNotifications')



	def ws_channel_id(self):
		j = self._ws('{"events":[{"handler":"sah.hgw.models"}]}')
		return j['channelid']

	def ws_get_devices(self, channel_id):
		j = self._ws('{"events":[{"handler":"sah.hgw.models"}],"channelid":%s}' % channel_id)
		return j


if __name__ == '__main__':
	lb = Livebox()
	lb.login()
	#lb.sysbus('DeviceInfo?_restDepth=-1', c, C)
	#print lb._sysbus('')
	print lb.wan_status()
	print lb.list_trunks()
	print lb.ip_tv_status()
	print lb.dsl_stats()
	print lb.mibs()
	print lb.wifi_com_status()
	print lb.wiwi_mibs()
	# print lb.wifi(mode)
	# print lb.filtre_mac(flag)
	# print lb.reboot()
	lb.connectivity_enable_notifications()
	print lb.ws_get_devices(lb.ws_channel_id())

	print lb._sysbus('')
	print lb.logout()






