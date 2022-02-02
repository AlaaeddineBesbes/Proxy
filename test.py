import socket
import sys
import _thread


def main():
    global listen_port, buffer_size, max_conn
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

    conn,addr = s.accept()
    while True:
            try:
                data = conn. recv(buffer_size)
                print(data.decode('utf-8'))
                conn.send(data)
            except KeyboardInterrupt:
                s.close()
                print("\n[*] Shutting down...")
                sys.exit(1)

if __name__ == "__main__":
    main()
