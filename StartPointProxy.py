import socket
import sys
import _thread
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

endPointPP=1010
localHost='127.0.0.1'
keyPair = RSA.generate(3072)
proxyKey=None
encryptor = None
decryptor=None
def main():
    global listen_port, buffer_size, max_conn
    
    global decryptor
    global encryptor
    try:
        listen_port = int(input("Enter a listening port :"))
    except KeyboardInterrupt:
        sys.exit(0)
    
    max_conn = 5
    buffer_size = 8192

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',listen_port))
        s.listen(max_conn)
        print('Server started successfully')
    except Exception as e :
        print(e)
        sys.exit(2)

    _thread.start_new_thread(exchangePublicKey,())
    encryptor=PKCS1_OAEP.new(proxyKey)
    decryptor = PKCS1_OAEP.new(keyPair)

    while True:
        try:
            connToBrowser, addr =s.accept()
            #http request from the browser 
            data = encryptor.encrypt(connToBrowser.recv(buffer_size))
            print(data.decode('utf-8'))
            #creat a new thread to send the request to the webserver

            _thread.start_new_thread(conn_string, (connToBrowser, data))
        except KeyboardInterrupt:
            s.close()
            print('SHutting down ..')
            sys.exit(1)
    
    s.close()

def conn_string(conn,data):
    #getting the webserver and the port 
    try:
        endPointProxy(conn, data)
    except Exception as e :
        print(e)

def endPointProxy(conn,data):
   
    try:
        interProxyConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interProxyConnection.connect((localHost,endPointPP))
        interProxyConnection.send(data)
        while True:
            reply = decryptor.decrypt(interProxyConnection.recv(buffer_size))
            if len(reply)>0:
                conn.send(decryptor.decrypt(reply))
            else:
                break
        interProxyConnection.close()
        conn.close()
    except socket.error:
        interProxyConnection.close()
        conn.close()
        sys.exit(1)


def exchangePublicKey():
    global proxyKey
    interProxyConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    interProxyConnection.connect((localHost,endPointPP))
    interProxyConnection.send(keyPair.publickey().exportKey(format='PEM', passphrase=None, pkcs=1))
    proxyKey=RSA.importKey(interProxyConnection.recv(buffer_size), passphrase=None)




if __name__ == "__main__":
    main()
