# -*- coding: utf-8 -*-
#
# TagProtect plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 PtitBigorneau - www.ptitbigorneau.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.5'

import b3
import b3.plugin
import b3.events
from b3 import clients
from b3.functions import getCmd

import threading, thread, time

class TagprotectPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _clanname = "None"
    _clanexacttag = None
    _clansecondtag = None
    _clanapprotag = None
    _banactived = False
    _pluginactived = False
	
    def onLoadConfig(self):

        self._clanname = self.getSetting('settings', 'clanname', b3.STRING, self._clanname)
        self._clanexacttag = self.getSetting('settings', 'clanexacttag', b3.STRING, self._clanexacttag)
        self._clansecondtag = self.getSetting('settings', 'clansecondtag', b3.STRING, self._clansecondtag)
        self._clanapprotag = self.getSetting('settings', 'clanapprotag', b3.STRING, self._clanapprotag)
        self._banactived = self.getSetting('settings', 'banactived', b3.BOOLEAN, self._banactived)
        self._pluginactived = self.getSetting('settings', 'pluginactived', b3.BOOLEAN, self._pluginactived)

    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False
			
        if not self._clanexacttag:
            self.error('Clan Exact Tag is None')
            return False
        
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = getCmd(self, cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        self.registerEvent('EVT_CLIENT_AUTH', self.onClientAuth)
        self.registerEvent('EVT_CLIENT_NAME_CHANGE', self.onClientAuth)

    def onClientAuth(self, event):
	
        if not self._pluginactived:
           
            self.debug('TagProtect %s'%(self._pluginactived))
            return False

        client = event.client
        self.debug('TagProtect client : %s'%(client.name))

        if client.maxLevel == 100:
            self.debug('TagProtect superadmin : %s'%(client.name))
            return False

        cnamemin = client.name.lower()
        exacttagmin = self._clanexacttag.lower()

        if self._clansecondtag:
        
            secondtagmin = self._clansecondtag.lower()
			
        else:
		
            secondtagmin = None

        if self._clanapprotag:
		
            approtagmin = self._clanapprotag.lower()

        else:
		
            approtagmin = None
		
        self.debug('%s - %s - %s'%(exacttagmin, secondtagmin, approtagmin))
                
        if cnamemin.count(exacttagmin) > 0:
    
            cursor = self.console.storage.query("""
            SELECT *
            FROM tagprotect n 
            WHERE n.client_id = %s
            """ % (client.id))
        
            if cursor.rowcount == 0:
                
                tag = self._clanexacttag
                thread.start_new_thread(self.bantag, (client, event, tag))
                
            else:
                        
                thread.start_new_thread(self.wait, (10,))
                client.message('Hi ! ^1%s^7 member'%(self._clanexacttag))
                        
            cursor.close()
                
        elif secondtagmin and cnamemin.count(secondtagmin) > 0:
                
            cursor = self.console.storage.query("""
            SELECT *
            FROM tagprotect n 
            WHERE n.client_id = %s
            """ % (client.id))
        
            if cursor.rowcount == 0:
                
                tag = self._clansecondtag
                thread.start_new_thread(self.bantag, (client, event, tag))
               
            else:
                        
                thread.start_new_thread(self.wait, (10,))
                client.message('Hi ! ^1%s^7 member'%(self._clansecondtag))

            cursor.close()            

        elif approtagmin and cnamemin.count(approtagmin) > 0:

            cnamenotag = cnamemin.split(approtagmin)
            debcnamenotag = cnamenotag[0]
            fincnamenotag = cnamenotag[1]

            if (debcnamenotag[-1:] not in "abcdefghijklmnopqrstuvwxyz") or (fincnamenotag[:1] not in "abcdefghijklmnopqrstuvwxyz") or (cnamemin.find(approtagmin)==0):
               
                cursor = self.console.storage.query("""
                SELECT *
                FROM tagprotect n 
                WHERE n.client_id = %s
                """ % (client.id))
        
                if cursor.rowcount == 0:
                
                    thread.start_new_thread(self.kicktag, (client, event, approtagmin))
               
                else:
                        
                    thread.start_new_thread(self.wait, (10,))
                    client.message('Hi ! ^1%s^7 member'%(self._clanexacttag))
					
                cursor.close()
				
        else:
            
            return False

    def kicktag(self, client, event, approtagmin):
        
        time.sleep(20)
        client.message('^1%s^7 is the tag of the clan ^1%s^7'%(self._clanexacttag, self._clanname))
        time.sleep(2)       
        client.message('You are not a member of the clan ^1%s^7'%(self._clanname))
        time.sleep(2) 
        client.message('^1%s^7 in your nickname is not authorized'%(approtagmin))
        client.message('You will be ^1kicked')
        time.sleep(10)
        client.kick("%s TagProtect"%(self._clanexacttag),  None)
        
    def bantag(self, client, event, tag):
                
        time.sleep(20)
        client.message('^1%s^7 and ^1%s^7 are the tag of the clan ^1%s^7'%(self._clanexacttag, self._clansecondtag, self._clanname))
        time.sleep(2)       
        client.message('If you are a member of ^1%s^7 clan ! Contact administrator !'%(self._clanname))
        time.sleep(2) 
        client.message('^1%s^7 in your nickname is not authorized'%(tag))
			
        if self._banactived:
            client.message('You will be ^1banned')
            time.sleep(10)			
            client.ban("%s TagProtect"%(tag), None)
        else:
            client.message('You will be ^1kicked')
            time.sleep(10)
            client.kick("%s TagProtect"%(tag),  None)

    def cmd_addct(self, data, client, cmd=None):
        """\
        - Add member clan or team
        """

        if data:
            input = self._adminPlugin.parseUserCmd(data)
        else:
            client.message('!addct <name or id>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM tagprotect n 
            WHERE n.client_id = '%s'
            """ % (sclient.id))

            if cursor.rowcount > 0:
  
                client.message('%s is already registered' %(sclient.exactName))
                cursor.close()
                
                return False
            
            cursor.close()
            
            cursor = self.console.storage.query("""
            INSERT INTO tagprotect
            VALUES (%s)
            """ % (sclient.id))

            cursor.close()
            
            client.message('%s is now registered' %(sclient.exactName))
       
        else:
            return False

    def cmd_listmemberclan(self, data, client, cmd=None):
        """\
        - Member clan or team list 
        """
        
        thread.start_new_thread(self.listmemberclan, (data, client))
        
    def listmemberclan(self, data, client):
            
        cursor = self.console.storage.query("""
        SELECT *
        FROM tagprotect
        ORDER BY client_id
        """)
        
        c = 1
        
        if cursor.EOF:
          
            client.message('No member in the list')
            cursor.close()            
            return False
        
        while not cursor.EOF:
            sr = cursor.getRow()
            cid = sr['client_id']
            scid= '@'+str(cid)
            sclient = self._adminPlugin.findClientPrompt(scid, client)
            client.message('^2%s^7 - id : ^2@%s^7 - level : (^1%s^7)' % (sclient.exactName, cid, sclient.maxLevel))
            cursor.moveNext()
            c += 1
            
        cursor.close()
        
    def cmd_delct(self, data, client, cmd=None):
        
        """\
        Delete member clan or team
        """
        
        if data:
        
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!delct <name or id>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
        
            cursor = self.console.storage.query("""
            SELECT n.client_id
            FROM tagprotect n 
            WHERE n.client_id = '%s'
            """ % (sclient.id))
        
            if cursor.rowcount == 0:
                
                client.message("%s ^7is not in the the list of members"%(sclient.exactName))
                
                return False
            
            cursor.close()
        
            cursor = self.console.storage.query("""
            DELETE FROM tagprotect
            WHERE client_id = '%s'
            """ % (sclient.id))
            cursor.close()
            
            client.message("%s ^7has been eliminated from the list of members"%(sclient.exactName))
            
        else:
            return False

    def cmd_tagprotect(self, data, client, cmd=None):
        
        """\
        activate / deactivate tagprotect 
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._pluginactived:

                client.message('^3Tagprotect ^2activated^7')

            else:

                client.message('^3Tagprotect ^1deactivated^7')

            if self._banactived:

                client.message('^3Ban ^2activated^7')

            else:

                client.message('^3Ban ^1deactivated^7')

            client.message('!tagprotect <on / off> <ban yes / ban no> ')
            return
      
        
        if input[0] == 'on':

            if not self._pluginactived:

                self._pluginactived = True
                message = '^3Tagprotect ^2activated^7'
                modif = "pluginactived: on\n"
                settingname = "pluginactived:"

            else:

                client.message('^3Tagprotect is already ^2activated^7') 

                return False

        if input[0] == 'off':

            if self._pluginactived:

                self._pluginactived = False
                message = '^3Tagprotect ^1deactivated^7'
                modif = "pluginactived: off\n"
                settingname = "pluginactived:"

            else:
                
                client.message('Tagprotect is already ^1disabled^7')                

                return False

        if input[0] == 'ban':

            if input[1] == 'yes':

                if not self._banactived:

                    self._banactived = True
                    message = '^3Ban ^2activated^7'
                    modif = "banactived: yes\n"
                    settingname = "banactived:"

                else:

                    client.message('^3Ban is already ^2activated^7') 

                    return False

            elif input[1] == 'no':
                
                if self._banactived:

                    self._banactived = False
                    message = '^3Ban ^1disabled^7'
                    modif = "banactived: no\n"
                    settingname = "banactived:"

                else:

                    client.message('^3Ban is already ^1disabled^7') 

                    return False
            else:

                client.message('!tagprotect <ban yes / ban no> ')
                return        

        client.message('tagprotect %s'%(message))

        fichier = self.config.fileName

        tagprotectini = open(fichier, "r")
        
        contenu = tagprotectini.readlines()

        tagprotectini.close()

        newcontenu = ""

        for ligne in contenu:

            if settingname in ligne:

                ligne = modif

            newcontenu = "%s%s"%(newcontenu, ligne)        

        tagprotectiniw = open(fichier, "w")
        tagprotectiniw.write(newcontenu)
        tagprotectiniw.close()

    def wait(self, temps):

        time.sleep(temps)
        return
