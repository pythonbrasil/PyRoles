# importando o que precisa
import time
from telebot import TeleBot
import flickrapi
import configparser
import os
import json
import hashlib

# importando configuracoes
config = configparser.ConfigParser()
config.sections()
config.read('pyroles.conf')

# autenticando o flickr
api_key = config['FLICKR']['API_KEY']
api_secret = config['FLICKR']['API_SECRET']
flickr = flickrapi.FlickrAPI(api_key, api_secret)
evento = config ['ALBUM']['ULTIMO_EVENTO']

if not flickr.token_valid(perms='delete'):
    flickr.get_request_token(oauth_callback='oob')
    authorize_url = flickr.auth_url(perms='delete')
    print(authorize_url)
    verifier = str(input('Verifier code: '))
    flickr.get_access_token(verifier)

# autenticando o bot
TOKEN = config['TGBOT']['TOKEN']
bot = TeleBot(TOKEN)

#passando o comando start e help para o bot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    message_return= "Olá, eu sou o {0}!\nEu consigo fazer uploads de todas as fotos dos rolês que aconteceram para o <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a>.\nMas para isso acontecer, é necessário ter em mente algumas regras:\n▪️ O bot aceita apenas fotografias. Gifs e vídeos ainda não são suportados. Ah! E não adianta enviar a foto como documento também, eu só aceito 'ibagens'.\n▪️ Não envie imagens de pessoas caso elas não queiram ou não saibam. Vamos respeitar a vontade do amigo de não querer a sua foto pública.📵\n▪️ Não envie nudes. Arrrr, vamos dizer que aqui não é o ambiente apropriado para você mostrar os seus dotes. \n▪️ Fotos com teor racista, homofóbico, violento, ou que infrinjam, de qualquer forma e maneira, o <a href='https://github.com/pythonbrasil/codigo-de-conduta'>Código de Conduta</a> do evento, serão excluídas, o usuário identificado e banido.\n▪️E lembre-se: \n\nPessoas >>> Tecnologia. \nUm ótimo evento para você!💛💙".format(evento)
    bot.reply_to(message,message_return , parse_mode="HTML", disable_web_page_preview=True)

def checkDuplicate(photo):

    with open('hash_table.txt', 'r') as file:
        data = file.read()

    with open(str(photo), 'rb') as file:
        data_foto = file.read()

    hashPhoto = hashlib.md5(data_foto).hexdigest() 
    hashTable = json.loads(data)



    if (hashPhoto in hashTable.values()):
        return True
    
    else:
        
        hashTable[hashPhoto] = hashPhoto
        with open('hash_table.txt', 'w') as file:
            file.write(json.dumps(hashTable))
        
        return False


# salvando a foto no sistema e fazendo o upload para o flickr 
@bot.message_handler(content_types=['photo'])
def get_doc(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    raw = message.photo[-1].file_id
    path = raw+".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)

    if (not checkDuplicate(path)):
        bot.reply_to(message, "A sua fotografia agora faz parte do <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a> ! \nObrigada por fazer essa comunidade ser tão maravilhosa!💛💙", parse_mode="HTML", disable_web_page_preview=True)
        flickr.upload(filename=path, title='PyBR14', description='Python Brasil [14]')
    else:
        bot.reply_to(message, "Foto duplicada.")


# apaga a foto do servidor 
    os.remove(path)
 
bot.polling()

