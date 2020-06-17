from SocketServer import TCPServer, ThreadingMixIn, BaseRequestHandler
import SocketServer
import struct
import sqlite3
import datetime
import ssl

version = '0.1.0'
delete_timer = 5000.0
t1 = datetime.datetime.now()

def delete_old_data():
	sql_conn = sqlite3.connect('../koronako-data/coronadata.db')
	c = sql_conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS covid
             (date text, devicepair text, user text, reliability text)''')
	print "Old data deleted" + str(datetime.datetime.today().day)
	tday = datetime.datetime.today().day
	i=1
	while i<32:
		#Deleting old data from database
		if i<10:
			textday = ('0' + str(i),)
		else:
			textday = (str(i),)
		if i < (tday-25):
			c.execute('DELETE FROM covid WHERE substr(devicepair,1,2) = ?', textday);
		elif (i>tday and i < (tday +5)):
			c.execute('DELETE FROM covid WHERE substr(devicepair,1,2) = ?', textday);
		i = i + 1
	sql_conn.commit()
	sql_conn.close()


def test_if_corona(_data):
	sql_conn = sqlite3.connect('../koronako-data/coronadata.db')
	c = sql_conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS covid
             (date text, devicepair text, user text, reliability text)''')
	days = []
	i = 17
	while i < len(_data):
		dev = (_data[i:i+17],)
		for row in c.execute('SELECT devicepair FROM covid WHERE devicepair = ?', dev):
       			days.append(row[0][:2])
		i = i + 17
	days.sort(key=None, reverse=True)
	sql_conn.close()
	if len(days) >0:
		print (days[0])
		return ("EXPOSUREDD "+days[0])
	else:
		return ("NOEXPOSURE")

def insert_corona_data(_data):
	sql_conn = sqlite3.connect('../koronako-data/coronadata.db')
	c = sql_conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS covid
             (date text, devicepair text, user text, reliability text)''')
	i = 17
	while i < len(_data):
		dev = (_data[i:i+17],)
		c.execute("INSERT INTO covid VALUES (?,?,?,?)", (_data[i:i+2],_data[i:i+17],'tester', '01',))
		i = i + 17
	sql_conn.commit()
	sql_conn.close()
	return ("SENTCOVIDD Covid data inserted")
##
#Idea from https://docs.python.org/2/library/socketserver.html
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	global delete_timer
	global t1
	global version
	_vers = version[0:1] + ':' + version[2:3] + version[4:5]
        self.data = self.request.recv(4096).strip()
	print (self.data[:8])
        # Save infection data or test against saved data
	if self.data[:8] == '00:0'+_vers:
		print (self.data[:8]) + ' NEWDATA'
		self.request.sendall(insert_corona_data(self.data))
	elif self.data[:8] == '00:1' + _vers:
		print (self.data[:8]) + ' TEST' 
        	self.request.sendall(test_if_corona(self.data))
		if delete_timer > 3600.0:
			delete_old_data()
			t1 = datetime.datetime.now()
			delete_timer = (datetime.datetime.now()-t1).total_seconds()
			print delete_timer
		else:
			delete_timer = (datetime.datetime.now()-t1).total_seconds()
			print delete_timer
	else:	
		print (self.data[:8]) + ' ERROR'
        	self.request.sendall("ERRORERROR")
##
## 
# Server classes MySSL_TCPServer and  MySSL_ThreadingTCPServer modified from Stack overflows guestion answer from WarriorPaw, licenced under CC BY-SA 3.0 
# https://stackoverflow.com/questions/8582766/adding-ssl-support-to-socketserver
class MySSL_TCPServer(TCPServer):
    def __init__(self,
                 server_address,
                 RequestHandlerClass,
                 certfile,
                 keyfile,
                 cert_reqs=ssl.CERT_OPTIONAL,
                 ssl_version=ssl.PROTOCOL_TLSv1,
                 bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.certfile = certfile
        self.keyfile = keyfile
        self.cert_reqs = cert_reqs
        self.ssl_version = ssl_version

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 cert_reqs=self.cert_reqs,
                                 certfile = self.certfile,
                                 keyfile = self.keyfile,
                                 ssl_version = self.ssl_version)
        return connstream, fromaddr

class MySSL_ThreadingTCPServer(ThreadingMixIn, MySSL_TCPServer): pass
##
##

if __name__ == "__main__":
    HOST, PORT = "172.28.172.3", 4243
    #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    #server.serve_forever()
    MySSL_ThreadingTCPServer((HOST, PORT),MyTCPHandler,"../koronako-data/cert.pem","../koronako-data/keys.pem").serve_forever()

