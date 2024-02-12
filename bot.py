import re
import time
###############################################################################################################################################################################
#                                                                               Bot.py                                                                                        #
#                                                                   MESSAGE FROM: Kamrons.space                                                                               #
#               Hi! thank you for downloading my scripts! I've explained everything below! Please dont try selling this script to people! That would be really lame of you.   #
#               No you will not get actual explainations on how the code works (I honestly forgot, i made this so long ago.)                                                  #
#               Read the README if you are lost on what to do.                                                                                                                #
#                                                                And dont forget, Keep rocking on dudes.                                                                      #
#                                                          (also watch my streams ft. josie on stringforworms)                                                                #
#                                                                                                                                                                             #
########################################################################## Change these pls ###################################################################################

# your C.AI token goes here, for more info on the whole module visit: https://pypi.org/project/characterai/
Client_token = "Put char_token here!"

# The character ID goes here. this github wiki is for something different but still is useful. https://github.com/drizzle-mizzle/Character-Engine-Discord/wiki/Important-Notes-and-Additional-Guides#get-character-id
character_token = "Put any character ID here!"

# this is the default badword list (Pulled from: https://www.cs.cmu.edu/~biglou/resources/bad-words.txt)
# if you have your own, you can change that here. feel free to also change the words in the list. 
# This section will prevent messages with these words going to the bot, but also keep the bot from saying them.
# Never forget, the "who did kanye west say was in paris?" incident that led to the creation of this.   ._.

WordFile = "BADWORDS.txt"

# You reaaaalllyyy dont want every message to be responded to. So you have a code word.
# set up the code word! For example mine is josie (the AI i have livestream for me occasionally.)

codeword = "Code word here"

########################################################################## Definitions block ###################################################################################

#This loads the badword file in.

def Load_Badwords(file_path):
    blocked_words = []
    with open(file_path, 'r') as file:
        print("Bad words loaded.")
        for line in file:
            blocked_words.append(line.strip())
    return blocked_words

#checks for bad words. 

def prof_checker(text, BADWORDS):
    print(text)
    to_check = text.lower()
    if not to_check.strip().split():
        return None
    for word in to_check.strip().split():
        if word.lower() in set(BADWORDS):
            return None
    print("")
    print("no bad words found")
    print("")
    return to_check

#this reads the message sent by the other python file.

def parse_chat_message(line):
    pattern = r'^(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}) - :(\w+)!.+? PRIVMSG #\w+ :(.+)$'

    print(line)

    match = re.match(pattern, line)
    if match:
        timestamp = match.group(1)
        username = match.group(2)
        message = match.group(3)
        print('it worked')
        return timestamp, username, message
    else:
        print(" ")
        print("- - - - -")
        print("no MSG")
        print("- - - - -")
        print(" ")
        return None, None, None


# Example usage (these are what the other code sends to the chat.log file)
#line = "2023-08-24_18:13:08 - username!username@username.tmi.twitch.tv PRIVMSG #chatname :message here"


#This monitors if the messages are empty.

def monitor_chat_log():
    with open('chat.log', 'r', encoding='utf-8') as chat_file:
        lines = chat_file.readlines()
    processed_indices = []

    for index, line in enumerate(lines):
        timestamp, username, message = parse_chat_message(line)
        print("Timestamp:", timestamp)
        print("Username:", username)
        print("Message:", message)


            #this deems if the message is worth responding to! If the codeword variable isnt working, replace codeword here with your word 
            # example if message is not None and "josie" in message.lower():

        if message is not None and codeword in message.lower():
            message = prof_checker(message, BADWORDS)
            message = "{" + username + "} " + "said: " + message 
            print("Sending ", " * ", message," * ", "now!")
            processed_indices.append(index)
            new_lines = [line for index, line in enumerate(lines) if index not in processed_indices]
            new_content = ''.join(new_lines)
            
            with open('chat.log', 'w', encoding='utf-8') as chat_file:
                chat_file.writelines(new_lines)
            return(message)
        #This line below deletes the any non-codeword relevant messages because of that 0. 
        if timestamp is None or "0" in timestamp:  
            processed_indices.append(index)
            print("Status: read. Message:", message)
            continue


# THE CHAT MUST STAY EMPTY AFTER EVERY MESSAGE OR ELSE THE WHOLE DAMN THING BREAKS!!!!
 
    new_lines = [line for index, line in enumerate(lines) if index not in processed_indices]

    new_content = ''.join(new_lines)

    
    with open('chat.log', 'w', encoding='utf-8') as chat_file:
        chat_file.writelines(new_lines)

    time.sleep(1)
                


################################################################  C.AI generation and TTS section  #############################################################################
from characterai import PyCAI

import pyttsx3

###### you can change the voice here. more info at: https://pypi.org/project/pyttsx3/#############

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate', 210)
print("Starting voice systems")
engine.say("Powered on!")
engine.runAndWait()
print("...........")
print("Voice loaded....")
print("...........")
print("system boot.... OK")
print(" ")
print("- - - - -")
print(" ")
######################################################################  Below is C.Ai stuff ####################################################################################

# if you want to change things for the C.Ai module, here's the code that handles it.
client = PyCAI(Client_token)

char = character_token

chat = client.chat.get_chat(char)

participants = chat['participants']

if not participants[0]['is_human']:
    tgt = participants[0]['user']['username']
else:
    tgt = participants[1]['user']['username']

##################################################################### the loops.... ################################################################################################
print("monitor is ONLINE")
print(" ")
print("- - - - -")
print(" ")

#this just feeds the info to all of the other moving parts. If you feel like changing something, be careful. 

BADWORDS = Load_Badwords(WordFile)

while True:
    message = monitor_chat_log()
    if message == None:
        continue
    else:
        print(message)
        data = client.chat.send_message(
            chat['external_id'], tgt, message
        )
        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        print(f"{name}: {text}")
        print("")
        check = prof_checker(text, BADWORDS)
        print(check)
        print(" ")
        print("- - - - -")
        print(" ")

        if check == None:
            print("error")
            continue

        else:
            words = str(text)
            engine.say(words)
            engine.runAndWait()

    

