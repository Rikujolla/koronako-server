import SocketServer
import struct
import sqlite3

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

#https://docs.python.org/2/library/socketserver.html
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(4096).strip()
        # Save infection data or test against saved data
	if self.data[:4] == '00:0':
		print (self.data[:4])
		self.request.sendall(insert_corona_data(self.data))
	elif self.data[:4] == '00:1':
		print (self.data[:4])
        	self.request.sendall(test_if_corona(self.data))
	else:	
		print (self.data[:4])
        	self.request.sendall("ERRORERROR")

if __name__ == "__main__":
    HOST, PORT = "172.28.172.2", 32661
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
