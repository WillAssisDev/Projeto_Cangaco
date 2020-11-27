from nltk import tokenize, corpus
import re
from maria_bonita.conjunto_dados.utilidades.captura.info_tweet import SEP_DEMOJI
import maria_bonita.conjunto_dados.utilidades.captura.chaves_busca as cb
import maria_bonita.conjunto_dados.utilidades.tratamento_erros as te


CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.pre_processamento.tokenizacao.'


def __tratamento_emoji(tweet_texto:str, sep:str=SEP_DEMOJI):
  """Função que reconhece e normaliza emojis processados pela biblioteca demoji.

  :param tweet_texto: o texto publicado sendo processado
  :param sep: deve ser o mesmo separador de emojis utilizado na captura dos tweets
  :return: o tweet com da remoção do SEP e capitalização
  """
  if SEP_DEMOJI in tweet_texto:
    regex_sep = r'[' + sep + r']{1}[\w\s\-]+[' + sep + r']{1}'
    regex2_espacos = r'[' + sep + r']{1,}'

    for i in re.finditer(regex_sep, tweet_texto):
      emoji = i.group().upper()
      inicio = i.span()[0]
      fim = i.span()[1]

      tweet_texto = tweet_texto.replace(tweet_texto[inicio:fim], emoji)

    return re.sub(regex2_espacos, ' ', tweet_texto)
  return tweet_texto


def __tratamento_mencionados(tokens:str, mencionados:list, resultado='MENÇÃO'):
  """Função que reconhece e normaliza os usuários mencionados em um tweet.

  :param tokens: lista de fatias processadas de um conjunto de caracteres
  :param mencionados: lista com screen_names de usuários mencionados no tweet
  :param resultado: tweet resultante da substituição dos usuários mencionados pelo valor de RESULTADO
  :return:
  """
  lista_tokens = []
  for token in tokens:
    lista_tokens.append(token) if token not in mencionados else lista_tokens.append(resultado)
  return lista_tokens


def __tratamento_normalizacao_chaves(tweet_texto: str, chaves_busca: list):
  """Função que identifica no tweet chaves de busca grafadas incorretamente e as normaliza.

  :param tweet_texto: o texto publicado sendo processado
  :param chaves_busca: lista que contém os objetos das chaves de busca e respectivos rótulos
  :return:
  """
  for chave in chaves_busca:
    if not isinstance(chave, cb.Chave_Busca): chave = cb.Chave_Busca.identificar_chave(chave)

    for chave_normal, lista_a_normalizar in chave.lista_normalizacao:
      for item_a_normalizar in lista_a_normalizar:
        if item_a_normalizar in tweet_texto: tweet_texto = tweet_texto.replace(item_a_normalizar, chave_normal)

  return tweet_texto


def __tratamento_numeros(token:str):
  """Função que reconhece e normaliza números.

  :param token: fatia processada de um conjunto de caracteres
  :return: token resultante do arredondamento para inteiro e da substituição de números por '0'
  """
  token = token.replace(',', '.')
  try:
    return '0' * len(str(int(float(token))))
  except:
    return token


def __tratamento_remover_caractere(token: str, alvo: str):
  """Função para remover expressamente determinado caractere.

  :param token: fatia processada de um conjunto de caracteres
  :param alvo: caractere que deve ser removido
  :return: se houver remoção, o token original é dividido em uma lista, separada nos pontos onde houveram as remoções
  """
  if isinstance(token, list):
    lista_novos_tokens = []
    for novo_token in token:
      novo_token = __tratamento_remover_caractere(novo_token, alvo)
      lista_novos_tokens.append(novo_token)
    return lista_novos_tokens
  else:
    token = token.replace(alvo, ' ').split()
    if len(token) > 1:
      return [novo_token.strip() for novo_token in token]
    else:
      return ''.join(token).strip()


def __tratamento_stopwords(tokens:list):
  """Função que remove stopwords da lista de tokens.

  :param tokens: lista de fatias processadas de um conjunto de caracteres
  :return: lista de tokens sem as stopwords
  """
  stopwords = corpus.stopwords.words('portuguese')
  return [token for token in tokens if token not in stopwords]


def __verifica_hifen(token:str):
  """Função para verificar se contém hífen em um token.

  :param token: fatia processada de um conjunto de caracteres
  :return: verdadeiro se possuir hífen, caso contrário, falso
  """
  regex = r'\w*-\w*'
  resultado = re.search(regex, token)
  try:
    if resultado.group(): return True
  except:
    return False


def tokenizar(tweet_texto:str, chaves_busca:list, mencionados:list):
  """ Função que recebe um tweet cru e lhe aplica os tratamentos necessários para o posterior processamento.

  :param tweet_texto: o texto publicado sendo processado
  :param chaves_busca: lista que contém os objetos das chaves de busca e respectivos rótulos
  :param mencionados: lista de usuários mencionados no tweet
  :return: tweet tratado: stopwords e não alfanuméricos removidas, descapitalização e menções, números e emojis normalizados
  """
  try:
    tweet_texto = tweet_texto.lower()
    tweet_texto = __tratamento_normalizacao_chaves(tweet_texto, chaves_busca)
    tweet_texto = __tratamento_emoji(tweet_texto)

    tokens = tokenize.word_tokenize(tweet_texto, 'portuguese')
    tokens = __tratamento_mencionados(tokens, mencionados)
    tokens = __tratamento_stopwords(tokens)

    tweet_tokens_texto = []
    for token in tokens:
      token = __tratamento_numeros(token)
      token = __tratamento_remover_caractere(token, '_')

      if isinstance(token, list):
        token = [token for token in token if token.isalpha or '0' in token or __verifica_hifen(token)]
        tweet_tokens_texto += token
      else:
        if token.isalpha() or '0' in token or __verifica_hifen(token): tweet_tokens_texto.append(token)

    return ' '.join(tweet_tokens_texto)

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'tokenizar')


__doc__ = """Módulo com recursos para efetuar tratamentos em tweet, possbilitando seu processamento."""
