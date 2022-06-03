# This Python file uses the following encoding: utf-8
import os
import requests
from pynput.keyboard import Listener, Key
import logging
from os.path import expanduser

TOKEN = ""
TXT_COD_PLAYER = expanduser("~") + os.sep + "txtCodPlayer.txt"
KEY_LOGS = expanduser("~") + "/key_log.txt"

logging.basicConfig(filename=KEY_LOGS, level=logging.DEBUG, format='%(asctime)s: %(message)s')

keys_detected = ''
lines = list()
content_dict = dict()

                            
def read_file():
    global file, lines, content_dict
    with open(TXT_COD_PLAYER) as file:
        lines = file.readlines()
        # Criando dict com key (código a receber) e value (código do conteúdo)
        for line in lines:
            content_dict[line.split(';')[0]] = line.split(';')[1].strip()


try:
    read_file()
except Exception as e:
    logging.warning("Error... {}".format(e))
    logging.info("Criando arquivo {}...".format(TXT_COD_PLAYER))
    with open(TXT_COD_PLAYER, 'w') as file:
        file.write("11;45\n")
    logging.info("Arquivo {} criado com sucesso!\n\t\t\tLembre de estabelecer os conteúdos que vão ser exibidos".format(
        TXT_COD_PLAYER))
    read_file()


def searchCode(keys_detected):
    # print(keys_detected, ' << Code Called')
    logging.info("Codigo >>> {0} <<< chamado".format(keys_detected))
    callURL(content_dict.get(keys_detected, False))


def callURL(media):
    if media:
        url = "http://127.0.0.1:48567/api/player/play"
        payload_one = "{\"mediaId\": \"" + media + "\", \"cutPlaylist\": true, \"ignoreSchedule\": true}"
        headers = {'Secret-Token': TOKEN, 'Content-Type': "application/json"}
        try:
            response = requests.request("POST", url, data=payload_one, headers=headers)
            if response.status_code == 200:
                logging.info("Conteudo >>> {0} <<< exibido com sucesso !!".format(media))
            elif response.status_code == 403:
                logging.info("Token incorreto, mude o token no arquivo {}".format(__file__))
            else:
                logging.info(
                    "Não foi possível executar o Conteúdo >> {0} <<<, revise os seguintes pontos:\n\t\t\t- Token.\n\t\t\t- Arquivo baixado.".format(
                        media))
        except Exception as e:
            logging.info(e)
    else:
        logging.info("Codigo >>> {0} <<<  nao existe, verifique o arquivo {1}".format(keys_detected, TXT_COD_PLAYER))


def on_press(key):
    global keys_detected
    if key == Key.enter:
        try:
            searchCode(keys_detected)
        except Exception as e:
            print('Error:', e)
        else:
            keys_detected = ''
    elif hasattr(key, 'char'):  # Write the character pressed if available
        # print("Key pressed: {0} {1}".format(key, key.char))
        keys_detected += str(key.char)  # add pressed character to line buffer
    else:
        pass
        # print('[' + key.name + ']')

# EVERYTHING STARTS HERE
with Listener(on_press=on_press) as listener:  # Setup the listener
    listener.join()  # Join the thread to the main thread
