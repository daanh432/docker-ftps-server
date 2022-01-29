import os, random, string

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer


length = 8
chars = string.ascii_letters + string.digits
random.seed = (os.urandom(1024))


FTP_ROOT = '/home'
USER = os.getenv('USER', 'user')
PASSWORD = os.getenv('PASSWORD', ''.join(random.choice(chars) for i in range(length)))
HOST =  os.getenv('HOST','0.0.0.0')
PORT = 21
PASSIVE_PORTS = '3000-3010'
ANONYMOUS = os.getenv('ANONYMOUS', False)
MASQUERADE_ADDRESS = os.getenv('MASQUERADE_ADDRESS', None)

CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "cert.pem"))

KEYFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "key.pem"))

def main():
    user_dir = os.path.join(FTP_ROOT, USER)
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)
    authorizer = DummyAuthorizer()
    authorizer.add_user(USER, PASSWORD, user_dir, perm="elradfmw")
    if ANONYMOUS:
        authorizer.add_anonymous("/ftp_root/nobody")
       
    handler = TLS_FTPHandler
    handler.certfile = CERTFILE
    handler.keyfile = KEYFILE
    handler.authorizer = authorizer
    handler.permit_foreign_addresses = True

    if MASQUERADE_ADDRESS:
        handler.masquerade_address = MASQUERADE_ADDRESS
    
    passive_ports = map(int, PASSIVE_PORTS.split('-'))
    handler.passive_ports = range(passive_ports[0], passive_ports[1])

    print('**********************************************************')
    print('*                                                        *')
    print('*                Docker image: daanh432                  *')
    print('*    https://github.com/daanh432/docker-ftps-server      *')
    print('*                                                        *')
    print('**********************************************************')
    print('SERVER SETTINGS')
    print('---------------')
    print "FTP Allow Ananymous: ",ANONYMOUS
    print "FTP Masquerade Address: ",MASQUERADE_ADDRESS
    print "FTP User: ",USER
    print "FTP Password: ",PASSWORD
    print "FTP Max Connections: ",os.getenv('MAX_CONS', 10)
    print "FTP Max Connections Per IP: ",os.getenv('MAX_CONS_PER_IP', 5)
    server = FTPServer((HOST, PORT), handler)
    server.max_cons = os.getenv('MAX_CONS', 10)
    server.max_cons_per_ip = os.getenv('MAX_CONS_PER_IP', 5)
    server.serve_forever()
    
if __name__ == '__main__':
    main()
