import json
from tweepy import OAuthHandler
import utilidades.tratamento_erros as te
from utilidades.caminho_projeto import CAMINHO_PROJETO


# CONSTANTES
_CAMINHO_MODULO = 'simulacao.autenticacao.'


def autenticar(chaves_twitter:str='chaves_twitter_NAO_VERSIONAR.json'):
  """Método que acessa localmente as credenciais de acesso ao end-point do Twitter e produz um autenticador.

  :param caminho_chaves_twitter: caminho do .json que contém as credenciais
  :return: autenticador de conexão
  """
  caminho_chaves = CAMINHO_PROJETO + chaves_twitter

  try:
    with open(caminho_chaves, 'r') as arquivo:
      chaves_twitter = json.load(arquivo)

    for chave, valor in chaves_twitter.items():
      if chave == 'api_key': api_key = valor
      elif chave == 'api_secret_key': api_secret_key = valor
      elif chave == 'access_token': access_token = valor
      elif chave == 'access_token_secret': access_token_secret = valor


    auth = OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return auth

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'autenticar')


__doc__ = "Módulo que automatiza autenticação de conexão com o o end-point do Twitter."
