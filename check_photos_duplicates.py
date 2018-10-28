import requests, json
import hashlib
USER = '160228175%40N08'
URL_BASE = 'https://api.flickr.com/services/rest/'
API_KEY = '0983c88c41789586c759c117c1defdf7'
METHOD ='flickr.people.getPublicPhotos'
FORMAT = 'json&nojsoncallback=1'
url = URL_BASE + '?method='+ METHOD +'&api_key='+ API_KEY +'&user_id='+ USER +'&format='+FORMAT


def getPhoto(id_person):

    url = URL_BASE + '?method='+ METHOD +'&api_key='+ API_KEY +'&user_id='+ id_person + '&per_page=500' +'&format='+FORMAT
    retorno = requests.get(url)
    comments = json.loads(retorno.content)
    photos_id = [ x['id'] for x in comments['photos']['photo'] ]
    return photos_id

def hashTablePhotos(photos_id):
    photo_dict = {}
    for photo in photos_id:
        url = URL_BASE + '?method=flickr.photos.getSizes&api_key='+API_KEY+'&photo_id='+str(photo)+'&format='+ FORMAT
        urlImagem = requests.get(url)
        idJson = json.loads(urlImagem.content)
        imagem = requests.get(idJson['sizes']['size'][-1]['source'])
        photo_dict[str(photo)] = hashlib.md5(imagem.content).hexdigest()
    return photo_dict

def saveDict(photo_dict):
    with open('hash_table.txt', 'a') as file:
        file.write(photo_dict)


photos = getPhoto('160228175%40N08')
hash_table = hashTablePhotos(photos)
saveDict(json.dumps(hash_table))



