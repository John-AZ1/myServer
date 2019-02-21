import socket
import time
import os
import errno
import signal
import re
from myRoster import index as maccas
from functools import wraps

class MyServer:
    def __init__(self, port=8080, queue_size=5):
        self.SERVER_ADDRESS = (self.HOST, self.PORT) = '', port
        self.REQUEST_QUEUE_SIZE = queue_size
        self.routes = []

    def _grim_reaper(self, signum, frame):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError:
                return

            if pid == 0: # No more zombies
                return

    def infoFromURL(self, url, data):
        for route in self.routes:
            match = re.compile(route[0]).fullmatch(url)
            if match:
                return(route[1](data, match.groupdict()))
        return("Oooof")

    def handle_request(self, client_connection):
        request = client_connection.recv(1024).decode('utf-8')
        try:
            data = request.split('\r\n\r\n')[1]
        except IndexError:
            data = ""
        http_ok = b"HTTP/1.1 200 OK\n\n"

        urlRaw, httpRaw = request.split("\r\n", 1)

        url = urlRaw.split(' ')[1]

        http_response = self.infoFromURL(url, data)

        client_connection.sendall(http_ok + bytes(http_response, 'utf-8'))

    def add_route(self, route, funct):
        self.routes.append([route, funct])

    def route(self, route):
        def decorator(funct):
            self.add_route(route, funct)
            
            @wraps(funct)
            def wrapped(*args):
                funct(*args)
            return(wrapped)
        return(decorator)

    def run(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(self.SERVER_ADDRESS)
        listen_socket.listen(self.REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port}'.format(port=self.PORT))

        signal.signal(signal.SIGCHLD, self._grim_reaper)

        while True:
            try:
                client_connection, client_address = listen_socket.accept()
            except IOError as e:
                code, msg = e.args
                # restart 'accept' if it was interrupted
                if code == errno.EINTR:
                    continue
                else:
                    raise

            pid = os.fork()
            if pid == 0:
                listen_socket.close()
                self.handle_request(client_connection)
                client_connection.close()
                os._exit(0)
            else:
                client_connection.close()

if __name__ == '__main__':
    server = MyServer()

    @server.route("/")
    def index(data, urldict):
        try:
            indexFile = open('./myRoster/index.html', 'r')
            content = indexFile.read()
            indexFile.close()
        except IOError:
            content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
        return(content)
            
    @server.route("/api/(?P<function>[^/]*)")
    def api(data, urldict):
        if urldict['function'] == 'getRosterHTML':
            info = ""
            try:
                username = eval(data)['Username']
                password = eval(data)['Password']

                maccas.getCookies(username, password)
                for shift in maccas.getRoster():
                    info += shift.html()
            except Exception as e:
                info = 'Error Occured: Believed cause incorrect data passed'
                print("Exception:", e)
   
            return(info)        
        else:
            return("No such function exists!")

    @server.route("/(?P<path>.*)")
    def index(data, urldict):
        try:
            indexFile = open('./myRoster/' + urldict['path'], 'r')
            content = indexFile.read()
            indexFile.close()
        except IOError:
            content = "<h1 style='font-family:helvetica'>404: File Not Found!</h1>"
        return(content)
            
    server.run()
