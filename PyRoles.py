"""PyRoles."""
import json
import hashlib
from configparser import ConfigParser
from os import remove
from flickrapi import FlickrAPI
from telebot import TeleBot

config = ConfigParser()
config.sections()
config.read('pyroles.conf')

# autenticando o flickr
api_key = config['FLICKR']['API_KEY']
api_secret = config['FLICKR']['API_SECRET']
flickr = FlickrAPI(api_key, api_secret)

if not flickr.token_valid(perms='delete'):
    flickr.get_request_token(oauth_callback='oob')
    authorize_url = flickr.auth_url(perms='delete')
    print(authorize_url)
    verifier = str(input('Verifier code: '))
    flickr.get_access_token(verifier)

# autenticando o bot
TOKEN = config['TGBOT']['TOKEN']
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Mensagem de inicialização do bot."""
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(
        message,
        "Olá, eu sou o PyRolês[14]! \nEu consigo fazer uploads de todas as fotos dos rolês que aconteceram para o <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a>.\nMas para isso acontecer, é necessário ter em mente algumas regras:\n▪️ O bot aceita apenas fotografias. Gifs e vídeos ainda não são suportados. Ah! E não adianta enviar a foto como documento também, eu só aceito 'ibagens'.\n▪️ Não envie imagens de pessoas caso elas não queiram ou não saibam. Vamos respeitar a vontade do amigo de não querer a sua foto pública.📵\n▪️ Não envie nudes. Arrrr, vamos dizer que aqui não é o ambiente apropriado para você mostrar os seus dotes. \n▪️ Fotos com teor racista, homofóbico, violento, ou que infrinjam, de qualquer forma e maneira, o <a href='https://github.com/pythonbrasil/codigo-de-conduta'>Código de Conduta</a> do evento, serão excluídas, o usuário identificado e banido.\n▪️E lembre-se: \n\nPessoas >>> Tecnologia. \nUm ótimo evento para você!💛💙",  # NOQA
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


def check_duplicate(photo):
    """Checa se a imagem é duplicada baseada no arquivo `hash_table.txt`."""
    with open('hash_table.txt', 'r') as file:
        data = file.read()

    with open(str(photo), 'rb') as file:
        data_foto = file.read()

    hash_photo = hashlib.md5(data_foto).hexdigest()
    hash_table = json.loads(data)

    if hash_photo in hash_table.values():
        return True

    else:
        hash_table[hash_photo] = hash_photo
        with open('hash_table.txt', 'w') as file:
            file.write(json.dumps(hash_table))
        return False


@bot.message_handler(content_types=['photo'])
def get_doc(message):
    """Salva a foto no sistema e faz upload da mesma para o flickr.

    TODO: separar essa função em duas para evitar side effects
        em relação ao get do bot e ao upload.
    """
    bot.send_chat_action(message.chat.id, 'upload_photo')
    raw = message.photo[-1].file_id
    path = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)

    if not check_duplicate(path):
        bot.reply_to(
            message,
            "A sua fotografia agora faz parte do <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a> ! \nObrigada por fazer essa comunidade ser tão maravilhosa!💛💙",  # NOQA
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        flickr.upload(
            filename=path,
            title='PyBR14',
            description='Python Brasil [14]'
        )
    else:
        bot.reply_to(message, "Foto duplicada.")

    remove(path)  # apaga a foto do servidor


bot.polling()
