from nltk import tokenize, corpus
import re
import utilidades.tratamento_erros as te
import maria_bonita.conjunto_dados.utilidades.pre_processamento.normalizacao as normalizacao


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.pre_processamento.tokenizacao.'


def __tratamento_remover_caractere(token:str, alvo:str):
  """Função para remover expressamente determinado caractere.

  :param token: fatia processada de um conjunto de caracteres
  :param alvo: caractere que deve ser removido
  :return: se houver remoção, o token original é dividido em uma lista, separada nos pontos onde houveram as remoções
  """
  try:
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

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__tratamento_remover_caractere')


def __tratamento_stopwords(tokens:list):
  """Função que remove stopwords da lista de tokens.

  :param tokens: lista de fatias processadas de um conjunto de caracteres
  :return: lista de tokens sem as stopwords
  """
  try:
    stopwords = corpus.stopwords.words('portuguese')
    return [token for token in tokens if token not in stopwords]

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__tratamento_stopwords')


def __verifica_hifen(token:str):
  """Função para verificar se contém hífen em um token.

  :param token: fatia processada de um conjunto de caracteres
  :return: verdadeiro se possuir hífen, caso contrário, falso
  """
  try:
    regex = r'\w*-\w*'
    resultado = re.search(regex, token)
    try:
      if resultado.group(): return True
    except:
      return False

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__verifica_hifen')


def tokenizar(tweet_texto:str, chaves_busca:list, mencionados:list, com_stopwords:bool):
  """ Função que recebe um tweet cru e lhe aplica os tratamentos necessários para o posterior processamento.

  :param tweet_texto: o texto publicado sendo processado
  :param chaves_busca: lista que contém os objetos das chaves de busca e respectivos rótulos
  :param mencionados: lista de usuários mencionados no tweet
  :param com_stopwords: parâmetro booleano que indica se as stopwords devem ou não serem mantidas
  :return: tweet tratado: stopwords e não alfanuméricos removidas, descapitalização e menções, números e emojis normalizados
  """
  try:
    tweet_texto = tweet_texto.lower()
    tweet_texto = normalizacao.chaves_busca(tweet_texto, chaves_busca)
    tweet_texto = normalizacao.usuarios_mencionados(tweet_texto, mencionados)
    tweet_texto = normalizacao.emoji(tweet_texto)
    tweet_texto = normalizacao.vogais_soltas(tweet_texto)
    tweet_texto = normalizacao.internetes(tweet_texto)
    tweet_texto = normalizacao.risadas(tweet_texto)
    tweet_texto = normalizacao.simbolos_com_alfanumericos(tweet_texto)

    tokens = tokenize.word_tokenize(tweet_texto, 'portuguese')
    if not com_stopwords: tokens = __tratamento_stopwords(tokens)

    tweet_tokens_texto = []
    for token in tokens:
      token = normalizacao.numeros(token)
      token = __tratamento_remover_caractere(token, '_')

      if isinstance(token, list):
        token = [token for token in token if token.isalpha or '0' in token or __verifica_hifen(token)]
        tweet_tokens_texto += token
      else:
        if token.isalpha() or '0' in token or __verifica_hifen(token): tweet_tokens_texto.append(token)

    return ' '.join(tweet_tokens_texto)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tokenizar')


__doc__ = """Módulo com recursos para efetuar tratamentos em tweet, possbilitando seu processamento."""
