# koronako-server
Server for harbour-koronako app

DESCRIPTION

koronako-server has two different operations. Either it replies to clients if exposured or not or saves the infection data. The sever is a simple python coded commandline application. Tho code is in the folder koronako-server and the data is in the folder koronako-data.

INSTALLATION AND USE

-copy binaries to some folder xxx in your computer by:
-create data folder ./koronako-data
-cd to folder

git clone https://github.com/Rikujolla/koronako-server.git
mkdir koronako-data
cd koronako-server

-setup right IP-addresses and ports by editing, same information you set on your phone:

     gedit koronako-server.py

start the server by typing:

     python koronako-server.py

server can be interrupted by Ctrl-C

