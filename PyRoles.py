# importando o que precisa
from telebot import TeleBot
import flickrapi
import configparser
import os

# importando configuracoes
config = configparser.ConfigParser()
config.sections()
config.read('pyroles.conf')

# autenticando o flickr
api_key = config['FLICKR']['API_KEY']
api_secret = config['FLICKR']['API_SECRET']
flickr = flickrapi.FlickrAPI(api_key, api_secret)

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
    bot.reply_to(message, "Olá, eu sou o PyRolês[14]! \nEu consigo fazer uploads de todas as fotos dos rolês que aconteceram para o <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a>.\nMas para isso acontecer, é necessário ter em mente algumas regras:\n▪️ O bot aceita apenas fotografias. Gifs e vídeos ainda não são suportados. Ah! E não adianta enviar a foto como documento também, eu só aceito 'ibagens'.\n▪️ Não envie imagens de pessoas caso elas não queiram ou não saibam. Vamos respeitar a vontade do amigo de não querer a sua foto pública.📵\n▪️ Não envie nudes. Arrrr, vamos dizer que aqui não é o ambiente apropriado para você mostrar os seus dotes. \n▪️ Fotos com teor racista, homofóbico, violento, ou que infrinjam, de qualquer forma e maneira, o <a href='https://github.com/pythonbrasil/codigo-de-conduta'>Código de Conduta</a> do evento, serão excluídas, o usuário identificado e banido.\n▪️E lembre-se: \n\nPessoas >>> Tecnologia. \nUm ótimo evento para você!💛💙", parse_mode="HTML", disable_web_page_preview=True)

# salvando a foto no sistema e fazendo o upload para o flickr 
@bot.message_handler(content_types=['photo'])
def get_doc(message):
    raw = message.photo[-1].file_id
    path = raw+".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "A sua fotografia agora faz parte do <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a> ! \nObrigada por fazer essa comunidade ser tão maravilhosa!💛💙", parse_mode="HTML", disable_web_page_preview=True)
    flickr.upload(filename=path, title='PyBR14', description='Python Brasil [14]')

# apaga a foto do servidor 
    os.remove(path)
 
bot.polling()
