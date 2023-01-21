import logging
import logging.handlers
import os
import re
import socket

from dotenv import load_dotenv


def main():
    load_dotenv()

    HOST = os.getenv('BOT_HOST')
    PORT = int(os.getenv('BOT_PORT'))
    NICK = os.getenv('BOT_NICK')
    TOKEN = os.getenv('BOT_TOKEN')
    CHANNELS = os.getenv('BOT_CHANNELS').split(',')

    logging.basicConfig(
        level=logging.DEBUG,format='%(asctime)s %(message)s', 
        datefmt='[%Y-%m-%d %H:%M:%S]',
        handlers=[logging.handlers.RotatingFileHandler('chat.log', maxBytes=100000000, encoding='utf-8')],
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    connect(HOST, PORT, NICK, TOKEN, sock)

    for channel in CHANNELS:
        join(sock, f'#{channel}')

    receive_data(sock)

def connect(HOST, PORT, NICK, TOKEN, sock):
    sock.connect((HOST, PORT))
    sock.send(('PASS oauth:' + TOKEN + '\r\n').encode('utf-8'))
    sock.send(('NICK ' + NICK +'\r\n').encode('utf-8'))

def join(sock, channel):
    sock.send(('JOIN '+ channel + '\r\n').encode('utf-8'))
    print(f'Joined channel {channel}')

def receive_data(sock):
    overflow = ''
    while True:
        raw_data = sock.recv(1024)
        data = raw_data.decode('utf-8', errors='ignore')
        parts, overflow = read_messages(data, overflow)
        
        for part in parts:
            handle_message(sock, part)
        
def handle_message(sock, msg):
    if msg[0:4] == 'PING':
        print(('### PONG'+ msg[4:] + '\r\n').encode('utf-8'))
        sock.send(('PONG'+ msg[4:] + '\r\n').encode('utf-8'))
        return

    irc_msg_parts = msg.split(' ', 3)
    
    if irc_msg_parts[1] == 'PRIVMSG':
        regex = r":([A-Za-z0-9_]*)!([A-Za-z0-9_]*)@(.*)"
        matches = re.findall(regex, irc_msg_parts[0])[0]
        nick = matches[0]
        user = matches[1]
        host = matches[2]
        channel = irc_msg_parts[2][1:]
        message = irc_msg_parts[3][1:]

        print(f'[{channel}] {user}: {message}')
        logging.info(f'[{channel}] {user}: {message}')

def read_messages(data, overflow):
    data = overflow + data
    messages = data.split('\r\n')
    overflow = messages.pop()

    return messages, overflow

def sendMessage(sock, channel, msg):
    ircmsg = 'PRIVMSG {channel} :{msg}\r\n'.format(channel=channel, msg=msg)
    print(ircmsg)
    sock.send(ircmsg.encode('utf-8'))

if __name__ == '__main__':
    main()
