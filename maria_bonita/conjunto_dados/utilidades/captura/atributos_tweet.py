import tweepy as tw
import utilidades.tratamento_erros as te
import demoji
# demoji.download_codes()


#CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.conjunto_dados.simulacao.captura.atributos_tweet.'
URL_RAIZ = 'https://twitter.com/'
SEP_DEMOJI = '§'


def __selecionar_chave_valor(lista_origem:list, chaves:list):
  """Função privada que, no tweet, acessa diferentes estruturas de dados e retorna somente aqueles selecionados.

  :param lista_origem: estrutura de dados de que os dados selecionados serão removidos
  :param chaves: dados selecionados
  :return: uma lista de dicionário(s), com somente os dados selecionados
  """
  try:
    lista_retorno = []
    for dicionario in lista_origem:
      dic_retorno = {}
      for chave, valor in dicionario.items():
        if chave in chaves: dic_retorno[chave] = valor
      lista_retorno.append(dic_retorno)
    return lista_retorno

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__selecionar_chave_valor')


def tweet_url(status:tw.Status):
  """Função para elaborar o endereço web do tweet.

  :param status: a publicação sendo capturada na streaming
  :return: string do url da publicação
  """
  try:
    tweet_user_screen_name = status.user.screen_name
    return URL_RAIZ + tweet_user_screen_name + '/status/' + status.id_str + '/'

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_url')


def tweet_texto(status:tw.Status, tem_extended_tweet:bool):
  """Função que recupera o texto do tweet e normaliza os emojis.

  :param status: a publicação sendo capturada na streaming
  :param tem_extended_tweet: indicador se na publicação está contido o atributo extended_tweet
  :return: string do texto sendo publicado, com os emojis normalizados
  """
  try:
    try:
      if tem_extended_tweet:
        tweet_texto = demoji.replace_with_desc(status.extended_tweet['full_text'], sep=SEP_DEMOJI)
      else:
        tweet_texto = demoji.replace_with_desc(status.text, sep=SEP_DEMOJI)

    except:
      tweet_texto = status.extended_tweet['full_text'] if tem_extended_tweet else status.text

    return tweet_texto

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_texto')


def tweet_hashtags(status:tw.Status, tem_extended_tweet:bool):
  """Função que recupera a(s) hashtag(s) do tweet, caso exista(m).

  :param status: a publicação sendo capturada na streaming
  :param tem_extended_tweet: indicador se na publicação está contido o atributo extended_tweet
  :return: uma lista da(s) hashtag(s) da publicação, caso exista(m)
  """
  try:
    tweet_hashtags = []
    if tem_extended_tweet:
      if len(status.extended_tweet['entities']['hashtags']):
        tweet_hashtags = [hashtag['text'] for hashtag in status.extended_tweet['entities']['hashtags']]

    else:
      if len(status.entities['hashtags']):
        tweet_hashtags = [hashtag['text'] for hashtag in status.entities['hashtags']]

    return tweet_hashtags

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_hashtags')


def tweet_urls_externos(status:tw.Status, tem_extended_tweet:bool):
  """Função que recupera o(s) url(s) externo(s) do tweet, caso exista(m).

  :param status: a publicação sendo capturada na streaming
  :param tem_extended_tweet: indicador se na publicação está contido o atributo extended_tweet
  :return: uma lista do(s) url(s) externo(s) da publicação, caso exista(m)
  """
  try:
    tweet_urls_externos = []
    if tem_extended_tweet:
      if len(status.extended_tweet['entities']['urls']):
        tweet_urls_externos = [url['expanded_url'] for url in status.extended_tweet['entities']['urls']]

    else:
      if len(status.entities['urls']):
        tweet_urls_externos = [url['expanded_url'] for url in status.entities['urls']]

    return tweet_urls_externos

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_urls_externos')


def tweet_usuarios_mencionados(status:tw.Status, tem_extended_tweet:bool):
  """Função que recupera o(s) usuários(s) mencionados(s) no tweet, caso exista(m).

  :param status: a publicação sendo capturada na streaming
  :param tem_extended_tweet: indicador se na publicação está contido o atributo extended_tweet
  :return: uma lista do(s) usuários(s) mencionados(s) na publicação, caso exista(m)
  """
  try:
    tweet_usuarios_mencionados = []
    if tem_extended_tweet:
      if len(status.extended_tweet['entities']['user_mentions']):
        tweet_usuarios_mencionados = __selecionar_chave_valor(lista_origem=status.extended_tweet['entities']['user_mentions'],
                                                              chaves=['screen_name', 'id_str'])
    else:
      if len(status.entities['user_mentions']):
        tweet_usuarios_mencionados = __selecionar_chave_valor(lista_origem=status.entities['user_mentions'],
                                                              chaves=['screen_name', 'id_str'])

    return tweet_usuarios_mencionados

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_usuarios_mencionados')


def tweet_em_resposta(status:tw.Status):
  """Função que recupera o usuários respondido no tweet, caso exista.

  :param status: a publicação sendo capturada na streaming
  :param tem_extended_tweet: indicador se na publicação está contido o atributo extended_tweet
  :return: dicionário do usuários respondido na publicação, caso exista
  """
  try:
    if status.in_reply_to_status_id_str:
      tweet_em_resposta = {'resposta_ao_tweet': status.in_reply_to_status_id_str,
                           'screen_name': status.in_reply_to_screen_name,
                           'id_str': status.in_reply_to_user_id_str}

    else:
      tweet_em_resposta = None

    return tweet_em_resposta

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_em_resposta')


def __autor_usuario_nome(nome:str):
  """Função privada para normalizar emojis no atributo name do autor ou usuário.

  :param nome: atributo name, do autor ou usuário
  :return: string do atributo name, com emojis normalizados
  """
  try:
    try:
      return demoji.replace_with_desc(nome, sep=SEP_DEMOJI)

    except:
      return nome

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__autor_usuario_nome')


def autor_nome(status:tw.Status):
  """Função para recuperar o atributo name do autor e normalizar emojis.

  :param status: a publicação sendo capturada na streaming
  :return: string do atributo name, com emojis normalizados
  """
  try:
    return __autor_usuario_nome(status.author.name)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'autor_nome')


def usuario_nome(status:tw.Status):
  """Função para recuperar o atributo name do usuário e normalizar emojis.

  :param status: a publicação sendo capturada na streaming
  :return: string do atributo name, com emojis normalizados
  """
  try:
    return __autor_usuario_nome(status.user.name)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'usuario_nome')


def __autor_usuario_url(screen_name:str):
  """Função privada para elaborar o endereço web do do perfil do autor ou usuário.

  :param screen_name: atributo name, do autor ou usuário
  :return: string da url elaborada
  """
  try:
    return URL_RAIZ + screen_name + '/'

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__autor_usuario_url')


def autor_url(status:tw.Status):
  """Função para elaborar o endereço web do do perfil do autor.

  :param status: a publicação sendo capturada na streaming
  :return: string da url elaborada para o autor
  """
  try:
    return __autor_usuario_url(status.author.screen_name)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'autor_url')


def usuario_url(status:tw.Status):
  """Função para elaborar o endereço web do do perfil do usuário.

  :param status: a publicação sendo capturada na streaming
  :return: a url elaborada para o usuário
  """
  try:
    return __autor_usuario_url(status.user.screen_name)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'usuario_url')


def __autor_usuario_descricao(descricao:str):
  """Função privada para normalizar emojis na descrição do autor ou usuário.

  :param descricao: atributo description, do autor ou usuário
  :return: string da descrição normalizada
  """
  try:
    try:
      return demoji.replace_with_desc(descricao, sep=SEP_DEMOJI)

    except:
      return descricao

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__autor_usuario_descricao')


def autor_descricao(status:tw.Status):
  """Função privada para recuperar a descrição do autor e normalizar os emojis.

  :param status: a publicação sendo capturada na streaming
  :return: string da descrição normalizada
  """
  try:
    return __autor_usuario_descricao(status.author.description)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'autor_descricao')


def usuario_descricao(status:tw.Status):
  """Função privada para recuperar a descrição do usuário e normalizar os emojis.

  :param status: a publicação sendo capturada na streaming
  :return: string da descrição normalizada
  """
  try:
    return __autor_usuario_descricao(status.user.description)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'usuario_descricao')


# URL IMAGEM PERFIL
def autor_url_imagem_perfil(status:tw.Status):
  """Função que recupera o endereço web da imagem de perfil do autor.

  :param status: a publicação sendo capturada na streaming
  :return: string da url da imagem
  """
  try:
    return status.author.profile_image_url_https if hasattr(status.author, "profile_image_url_https") else ""

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'autor_url_imagem_perfil')


# URL IMAGEM PERFIL
def usuario_url_imagem_perfil(status:tw.Status):
  """Função que recupera o endereço web da imagem de perfil do usuário.

  :param status: a publicação sendo capturada na streaming
  :return: string da url da imagem
  """
  try:
    return status.user.profile_image_url_https if hasattr(status.user, "profile_image_url_https") else ""

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'usuario_url_imagem_perfil')


# URL IMAGEM CAPA
def autor_url_imagem_capa(status: tw.Status):
  """Função que recupera o endereço web da imagem de capa do autor.

  :param status: a publicação sendo capturada na streaming
  :return: string da url da imagem
  """
  try:
    return status.author.profile_banner_url if hasattr(status.author, "profile_banner_url") else ""

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'autor_url_imagem_capa')


# URL IMAGEM CAPA
def usuario_url_imagem_capa(status: tw.Status):
  """Função que recupera o endereço web da imagem de capa do usuário.

  :param status: a publicação sendo capturada na streaming
  :return: string da url da imagem
  """
  try:
    return status.user.profile_banner_url if hasattr(status.user, "profile_banner_url") else ""

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'usuario_url_imagem_capa')


__doc__ = """Módulo com recursos para estruturação da informação do tweet sendo capturado."""
