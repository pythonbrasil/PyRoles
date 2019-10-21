# @PyRoles
Este é um bot no Telegram que faz upload automático de todas as fotos dos rolês que rolaram durante a PyBR!

Como funciona:

1. Procure o @PyRolesbot na caixa de busca do Telegram.
2. Mande um start/help que ele vai mandar uma mensagem fofinha para você e vai ter passar algumas regras para o uso do bot. Vamos colocar elas aqui também para que tudo fique bem claro e o uso do bot seja saudável para todos:

▪️ O bot aceita apenas fotografias. Gifs e vídeos ainda não são suportados. 

▪️ A foto estava tremida? Você saiu de boca aberta comendo um dogão, mandou e se arrependeu? Bom, vai demorar um pouco, mas não se desespere! Envie um e-mail para pyroles@yahoo.com e vamos resolver isso. Ah, só pra lembrar: não tem nada demais uma foto assim, ia ser bem divertido ver.

▪️ Não envie imagens de pessoas caso elas não queiram ou não saibam. Vamos respeitar a vontade do amigo de não querer a sua foto pública.

▪️ Não envie nudes. Arrrr, vamos dizer que aqui não é o ambiente apropriado para você mostrar os seus dotes.  

▪️ Fotos com teor racista, homofóbico, violento, ou que infrinjam, de qualquer forma e maneira, o <a href='https://github.com/pythonbrasil/codigo-de-conduta'>Código de Conduta</a> do evento, serão excluídas, o usuário identificado e banido.

3. Enviou a foto? Recebeu outra mensagem fofinha? Pronto! Você já pode conferir ela e outras no <a href='https://www.flickr.com/photos/160228175@N08/'>álbum PyRolês</a> ! 

Mudanças no código, ideias mirabolantes e mais integrações são bem-vindas!

# Para instalar o bot

No Telegram:
1. Procurar pelo @BotFather.
2. Dar um /start e escrever /newbot no chat.
3. Dê um nome para o seu bot.
4. Crie o username dele.
5. Se tudo der certo ele vai te enviar um token. Esse monte de letrinhas é o que vai fazer o seu bot funcionar e receber atualizações. Guarde-o com carinho. Caso perca, é só mandar um /token e o @BotFather vai gerar um novo token de acesso para o seu bot.

No Flickr:

1. Faça o seu login no Flickr. 
2. No <a href='https://www.flickr.com/services/apps/create/'>site</a>, solicite a sua chave de API. Você terá em mãos agora a sua api_key e a sua api_secret. Eles são o que você precisa para fazer o upload para o álbum.

No código:
1. Faça o download.
2. Troque os espaços reservados para as suas tokens. 
3. Rode o programa.
4. Deve abrir uma janela para você dar a autorização da sua conta para o Flickr. Atenção para a opção de upload estar marcada. 

No bot:
1. Abra o seu bot.
2. Dê um /start.
3. Mande a fotografia. 
4. Vá ao seu álbum do Flickr e veja gente bonita! ❤️

## Estrutura

Atualmente o bot está rodando em um servidor temporário cedido pela APyB em um container docker

### Instalação

Docker +19.03
docker-compose +1.23.0

Configure o pyroles.conf com seus dados de API e execute:

```sh
docker-compose build
```

Depois, execute temporariamente um container para autorizar a app no flicker:

```sh
docker-compose run bot
```

Copie a URL exibida no terminal para seu navegador, autorize ela e copie o código dentro do container temporário.

Após a autorização, teste o seu bot e caso esteja funcionando, realize um commit local em sua imagem:

```
# caso você esteja rodando mais containers além deste, apenas use o nome do container atual
docker-compose commit $(docker ps -q) pyroles_bot:latest
```

E por último inicie o container desanexado

```
docker-compose up -d
```

# Créditos

@juditecypreste
@GabrielRF
@jgdsfilho

Ajude a manter o bot e aumente esta lista :)
