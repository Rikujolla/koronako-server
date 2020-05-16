from socket import *
import struct
import sqlite3

def test_if_corona(_data):
	sql_conn = sqlite3.connect('../koronako-data/coronadata.db')
	c = sql_conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS covid
             (date text, devicepair text, user text, reliability text)''')
	days = []
	i = 0
	while i < len(_data):
		dev = (_data[i:i+17],)
		for row in c.execute('SELECT devicepair FROM covid WHERE devicepair = ?', dev):
       			days.append(row[0][:2])
		i = i + 17
	days.sort(key=None, reverse=True)
	sql_conn.close()
	if len(days) >0:
		print (days[0])
		return ("Exposure "+days[0])
	else:
		return ("No exposure")

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
	return ("Your covid data inserted")

# TCPSOCKET
host = "172.28.172.2"
port = 32661

s = socket(AF_INET, SOCK_STREAM)

print "Socket Made"

s.bind((host,port))

print "Socket Bound"

s.listen(5)

print "Listening for connections..."

conn, addr = s.accept()

print 'Connection address:', addr

while True:

    try:
        data = conn.recv(1024)

        if not data: break
	if data[:2] == '00':
		print (data[:2])
		conn.sendall(insert_corona_data(data))
	else:
		conn.sendall(test_if_corona(data))
	#test_if_corona(data)
        #print "Client data: "+data
	#conn.sendall("No exposure")
	#conn.sendall(test_if_corona(data))

    except socket.error:
        print "Error Occured."
        break


