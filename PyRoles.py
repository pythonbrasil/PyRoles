#importando o que precisa
from telebot import TeleBot
import flickrapi

#autenticando o flickr
api_key = u'...'
api_secret = u'...'
flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='delete')
 
 
# autenticando o bot
TOKEN = '...'
bot = TeleBot(TOKEN)

#passando o comando start e help para o bot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá, eu sou o PyRolês[14]! \nEu consigo fazer uploads de todas as fotos dos rolês que aconteceram para o <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a>. \nMas para isso acontecer, é necessário seguir algumas informações antes:\n\n▪️ É preciso que você envie por aqui a fotografia. Não envie como documento, eu só aceito 'ibagens'.  \n▪️ Não envie imagens de pessoas caso elas não queiram ou não saibam. Pergunte antes! 📵  \n▪️ Não envie nudes. 🔞  \n\nE lembre-se: \nPessoas >>> Tecnologia. \nUm ótimo evento para você! 💛💙", parse_mode="HTML", disable_web_page_preview=True)

#salvando a foto no sistema e fazendo o upload para o flickr 
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
 
bot.polling()
