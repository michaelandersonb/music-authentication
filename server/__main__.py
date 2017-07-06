import socket, ssl
import os
import bcrypt # uses pip version bcrypt 1.0.1
from contextlib import closing

# in actual implementation this would be stored in a users table
# this example is just a proof of concept and is simplified to 
# validate a single client

#password = b"G3A3B3C4D4E4F4G4A4B4"
password = b"C4G4F4E4D4C5G4F4E4D4C5G4F4E4F4D4"
salt = b'$2b$12$8X8Mqbv77l.AiIypivknZO'

# this and the salt are what should be stored in the DB. the password
# is included above only for this example
hashed_stored_password = bcrypt.hashpw(password, salt)

thisdir = os.path.dirname(__file__)
keyfile = os.path.join(thisdir, "private.pem")

debug = False

# open the socket and start listening. then when something is received validate it
with closing(socket.socket()) as serversocket:
    serversocket.bind(('', 8000))
    serversocket.listen(5)
    while True:
        newsocket, fromaddr = serversocket.accept()
        sslContext = ssl.wrap_socket(newsocket, 
                                     server_side=True, 
                                     certfile=os.path.join(thisdir, "server.crt"),
                                     keyfile=os.path.join(thisdir, "private.pem"), 
                                     ssl_version=ssl.PROTOCOL_SSLv23)
        with closing(sslContext):
            data = sslContext.read()
            
            # we expect the data to be in this format:
            # 'MBAUTH VERSION 002'
            # 'START'
            # < note 0 >
            # < note 1 >
            # ...
            # < note n >
            # 'END'
            notes = []
            lines = iter(data.splitlines())
            if lines.next() == "MBAUTH VERSION 002" and lines.next() == "START":
                protocolgood = True
                done = False
                for line in lines: # iterates over remaining lines
                    if line == b'END':
                        break
                    notes.append(line)
                pwd = bytes(b''.join(notes))
                if debug:
                    print pwd
                hashed_pwd = bcrypt.hashpw(pwd, salt)
            else:
                protocolgood = False
            # now compare the password and tell the client about the results
            if protocolgood and hashed_pwd == hashed_stored_password:
                sslContext.write("Authenticated successfully.")
            else:
                sslContext.write("Authentication failed!")

