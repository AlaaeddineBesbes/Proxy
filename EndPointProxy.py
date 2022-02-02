import socket
import sys
import _thread

def main():
    global listen_port, buffer_size, max_conn
    listen_port = 1010
    max_conn = 5
    buffer_size = 8192

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',listen_port))
        s.listen(max_conn)
        print('EndPointProxy started successfully on port {}'.format(listen_port))
    except Exception as e :
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr =s.accept()
            #http request from the startPointProxy
            data = conn.recv(buffer_size)
            print(data)
            #send the request to the webServer
            _thread.start_new_thread(conn_string, (conn, data, addr))

        except KeyboardInterrupt:
            s.close()
            print('SHutting down ..')
            sys.exit(1)
    
    s.close()

def conn_string(conn,data,addr):
    #getting the webserver and the port 
    try:
        
        first_line = data.decode('utf-8').split("\n")[0]
        url = first_line.split(" ")[1]
        
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos +3):]

        port_pos = temp.find(":")
        
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver=""
        port=-1
        
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos+1):][:webserver_pos-port_pos -1])
            webserver=temp[:port_pos]
        
        print(webserver)

        proxy_server(webserver, port, conn, data,addr)
    except Exception as e :
        print(e)

def proxy_server(webserver, port, conn,data,addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver,port))
        s.send(data)

        while True:
            reply = s.recv(buffer_size)
            
            if len(reply)>0:
                conn.send(reply)
                print('server reply ',reply.decode('utf-8'))
            else:
                break
        s.close
        conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit(1)



if __name__ == "__main__":
    main()
