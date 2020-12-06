import json
import os
from tweepy import OAuthHandler
import utilidades.tratamento_erros as te


# CONSTANTES
_CAMINHO_MODULO = 'autenticacao.'


def autenticar(chaves_twitter:str='/chaves_twitter_NAO_VERSIONAR.json'):
  """Método que acessa localmente as credenciais de acesso ao end-point do Twitter e produz um autenticador.

  :param caminho_chaves_twitter: caminho do .json que contém as credenciais
  :return: autenticador de conexão
  """
  caminho = os.getcwd().replace('\\', r'/')
  fim = caminho.find('projeto_cangaco') + len('projeto_cangaco')
  caminho_chaves = caminho[:fim] + chaves_twitter

  with open(caminho_chaves, 'r') as arquivo:
    chaves_twitter = json.load(arquivo)

  for chave, valor in chaves_twitter.items():
    if chave == 'api_key': api_key = valor
    elif chave == 'api_secret_key': api_secret_key = valor
    elif chave == 'access_token': access_token = valor
    elif chave == 'access_token_secret': access_token_secret = valor

  try:
    auth = OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return auth

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + ' autenticar')
