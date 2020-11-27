import tweepy as tw
import maria_bonita.conjunto_dados.utilidades.tratamento_erros as te
import demoji
# demoji.download_codes()


#CONSTANTES
CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.captura.info_tweet.'
URL_RAIZ = 'https://twitter.com/'
SEP_DEMOJI = '§'


def tweet(status:tw.Status, dicionario_tweet:dict):
  """Médodo que estrutura as informações do tweet.

  :param status: apublicação capturada pela streaming
  :param dicionario_tweet:  estrutura de dados em que as inforções do tweet são armazenadas
  """
  try:
    # CRIADO EM
    dicionario_tweet["criado_em"] = status.created_at

    # RETWEET
    dicionario_tweet["retweet"] = status.text.startswith('RT')

    # TWEET ID
    dicionario_tweet["tweet_id"] = status.id_str

    # TWEET URL
    tweet_user_screen_name = status.user.screen_name
    dicionario_tweet['tweet_url'] = URL_RAIZ + tweet_user_screen_name + '/status/' + dicionario_tweet["tweet_id"]

    # TWEET TEXTO
    tem_extended_tweet = hasattr(status, "extended_tweet")
    tweet_texto = demoji.replace_with_desc(status.extended_tweet['full_text'], sep=SEP_DEMOJI) if tem_extended_tweet \
      else demoji.replace_with_desc(status.text, sep=SEP_DEMOJI)
    dicionario_tweet["tweet_texto"] = tweet_texto

    # TWEET HASHTAGS
    dicionario_tweet["tweet_hashtags"] = []
    if tem_extended_tweet:
      if len(status.extended_tweet['entities']['hashtags']):
        dicionario_tweet["tweet_hashtags"] = [hashtag['text'] for hashtag in status.extended_tweet['entities']['hashtags']]

    else:
      if len(status.entities['hashtags']):
        dicionario_tweet["tweet_hashtags"] = [hashtag['text'] for hashtag in status.entities['hashtags']]

    # TWEET URLS EXTERNOS
    dicionario_tweet["tweet_urls_externos"] = []
    if tem_extended_tweet:
      if len(status.extended_tweet['entities']['urls']):
        dicionario_tweet["tweet_urls_externos"] = [url['expanded_url'] for url in status.extended_tweet['entities']['urls']]
    else:
      if len(status.entities['urls']):
        dicionario_tweet["tweet_urls_externos"] = [url['expanded_url'] for url in status.entities['urls']]

    # TWEET USUÁRIOS MENCIONADOS
    dicionario_tweet["tweet_usuarios_mencionados"] = []
    if tem_extended_tweet:
      if len(status.extended_tweet['entities']['user_mentions']):                        
        dicionario_tweet["tweet_usuarios_mencionados"] = __selecionar_chave_valor(status.extended_tweet['entities']['user_mentions'], ['screen_name', 'id_str'])
    else:
      if len(status.entities['user_mentions']):
        dicionario_tweet["tweet_usuarios_mencionados"] = __selecionar_chave_valor(status.entities['user_mentions'], ['screen_name', 'id_str'])

    # TWEET PLATAFORMA DE ORIGEM
    dicionario_tweet["tweet_plataforma_origem"] = status.source[12:]

    # TWEET EM RESPOSTA
    if status.in_reply_to_status_id_str:
      dicionario_tweet["tweet_em_resposta"] = {'resposta_ao_tweet': status.in_reply_to_status_id_str,
                                               'screen_name': status.in_reply_to_screen_name,
                                               'id_str': status.in_reply_to_user_id_str}
    else:
      dicionario_tweet["tweet_em_resposta"] = None

    # TWEET LÍNGUA
    dicionario_tweet["tweet_lingua"] = status.lang

    # TWEET JSON
    dicionario_tweet["tweet_json"] = status._json

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'tweet', dicionario_tweet)


def antevisao_tweets_capturados(status:tw.Status):
  """Método que imprime no console a antevisão dos tweets sendo capturados pela streaming.

  :param status: apublicação capturada pela streaming
  """
  try:
    print(f'Usuário: {status.user.screen_name}')
    print(f'Texto: {status.text}')

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'antevisao_tweets_capturados')


def __selecionar_chave_valor(lista_origem:list, chaves:list):
  """Função que, no tweet, acessa diferentes estruturas de dados e retorna somente os aqueles selecionados.

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
    te.base_exception(erro, CAMINHO_MODULO + '__selecionar_chave_valor')


def autor(status:tw.Status, dicionario_tweet:dict):
  """Médodo que estrutura as informações do autor do tweet (quem publicou originalmente, em casos de retweets).

  :param status: publicação capturada pela streaming
  :param dicionario_tweet:  estrutura de dados em que as inforções do tweet são armazenadas
  """
  try:
    # NOME
    dicionario_tweet["autor_nome"] = demoji.replace_with_desc(status.author.name, sep=SEP_DEMOJI)

    # SCREEN NAME
    dicionario_tweet["autor_screen_name"] = status.author.screen_name

    # ID
    dicionario_tweet["autor_id"] = status.author.id_str

    # URL
    dicionario_tweet["autor_url"] = URL_RAIZ + dicionario_tweet["autor_screen_name"]

    # VERIFICADO
    dicionario_tweet["autor_verificado"] = status.author.verified

    # LOCALIZAÇÃO
    dicionario_tweet["autor_localizacao"] = status.author.location

    # DESCRICAO
    dicionario_tweet["autor_descricao"] = demoji.replace_with_desc(status.author.description, sep=SEP_DEMOJI)

    # QUANTIDADE SEGUIDORES
    dicionario_tweet["autor_qtd_seguidores"] = status.author.followers_count

    # QUANTIDADE AMIGOS
    dicionario_tweet["autor_qtd_amigos"] = status.author.friends_count

    # QUANTIDADE TWEETS
    dicionario_tweet["autor_qtd_tweets"] = status.author.statuses_count

    # URL IMAGEM PERFIL ############################################ VERIFICAR - RECEBENDO NONE
    dicionario_tweet["autor_url_imagem_perfil"] = status.author.profile_image_url_https if hasattr(status, "profile_image_url") else ""

    # URL IMAGEM CAPA ############################################ VERIFICAR - RECEBENDO NONE
    dicionario_tweet["autor_url_imagem_capa"] = status.author.profile_banner_url if hasattr(status, "profile_banner_url") else ""

    # CRIADO EM
    dicionario_tweet["autor_criado_em"] = status.author.created_at

    # JSON
    dicionario_tweet["autor_json"] = status.author._json

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'autor', dicionario_tweet)


def usuario(status:tw.Status, dicionario_tweet:dict):
  """Médodo que estrutura as informações do usuário que publicou o tweet (ou retweetou).

  :param status: publicação capturada pela streaming
  :param dicionario_tweet:  estrutura de dados em que as inforções do tweet são armazenadas
  """
  try:
    # NOME
    dicionario_tweet["usuario_nome"] = demoji.replace_with_desc(status.user.name, sep=SEP_DEMOJI)

    # SCREEN NAME
    dicionario_tweet["usuario_screen_name"] = status.user.screen_name

    # ID
    dicionario_tweet["usuario_id"] = status.user.id_str

    # URL
    dicionario_tweet["usuario_url"] = URL_RAIZ + dicionario_tweet["usuario_screen_name"]

    # VERIFICADO
    dicionario_tweet["usuario_verificado"] = status.user.verified

    # LOCALIZAÇÃO
    dicionario_tweet["usuario_localizacao"] = status.user.location

    # DESCRICAO
    dicionario_tweet["usuario_descricao"] = demoji.replace_with_desc(status.user.description, sep=SEP_DEMOJI)

    # QUANTIDADE SEGUIDORES
    dicionario_tweet["usuario_qtd_seguidores"] = status.user.followers_count

    # QUANTIDADE AMIGOS
    dicionario_tweet["usuario_qtd_amigos"] = status.user.friends_count

    # QUANTIDADE TWEETS
    dicionario_tweet["usuario_qtd_tweets"] = status.user.statuses_count

    # URL IMAGEM PERFIL ############################################ VERIFICAR - RECEBENDO NONE
    dicionario_tweet["usuario_url_imagem_perfil"] = status.user.profile_image_url_https if hasattr(status, "profile_image_url") else ""

    # URL IMAGEM CAPA ############################################ VERIFICAR - RECEBENDO NONE
    dicionario_tweet["usuario_url_imagem_capa"] = status.user.profile_banner_url if hasattr(status, "profile_banner_url") else ""

    # CRIADO EM
    dicionario_tweet["usuario_criado_em"] = status.user.created_at

    # JSON
    dicionario_tweet["usuario_json"] = status.user._json

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'usuario', dicionario_tweet)


__doc__ = """Módulo com recursos para realizar a estruturação da informação capturada, pela streaming, em uma
publicação, formando uma linha do conjunto de dados."""
