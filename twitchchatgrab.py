###############################################################################################################################################################################
#                                                                      twitchchatgrab.py                                                                                      #
#                                                                   MESSAGE FROM: Kamrons.space                                                                               #
#               Hi! Quick note, If theres any issues running this script, delete all notes! I'm serious notes may break this script!                                          #
#               No you will not get actual explainations on how the code works (I honestly forgot, i made this so long ago.)                                                  #
#               Read the README if you are lost on what to do.                                                                                                                #
#                                                                And dont forget, Keep rocking on dudes.                                                                      #
#                                                          (also watch my streams on twitch at stringforworms)                                                                #
#                                                     (yes you will probably see this code live in action that way.)                                                          #
########################################################################## Change these pls ###################################################################################

#you're going to need a twitch auth token for the chat. learn more: https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'Nickname goes here'
token = 'OAuth goes here.'
channel = '#channelnamehere'

# you shouldn't need to change anything beyond this line. If you do, it's because you know what you're doing. 
###############################################################################################################################################################################

import socket
import logging
from emoji import demojize

print("running...")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

def main():
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')
            
            if resp.startswith('PING'):
                # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                logging.info(demojize(resp))

    except KeyboardInterrupt:
        sock.close()
        exit()

if __name__ == '__main__':
    main()