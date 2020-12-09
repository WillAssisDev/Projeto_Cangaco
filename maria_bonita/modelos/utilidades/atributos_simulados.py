from numpy.random import choice
import utilidades.tratamento_erros as te
from maria_bonita.conjunto_dados.utilidades.captura.ferramentas_conjunto_dados import COM_RETWEETS
from maria_bonita.conjunto_dados.utilidades.captura.ferramentas_conjunto_dados import NAO_RELACIONADOS, SEGUINDO
from maria_bonita.conjunto_dados.utilidades.captura.atributos_tweet import URL_RAIZ


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.utilidades.modelos.utilidades.atributos_simulados.'
_OPCOES_RETWEET = (True, False)
_PROBABILIDADES_RETWEET = (0.8, 0.2)
_OPCOES_RELACIONAMENTO = (NAO_RELACIONADOS, SEGUINDO)
_PROBABILIDADES_RELACIONAMENTO = (0.95, 0.05)
_PROBABILIDADE_SEM_RESPONDIDO = 0.6


def retweet(com_retweets:bool=COM_RETWEETS, probabilidades=_PROBABILIDADES_RETWEET):
  """Função que simula origem de um tweet, como um retweet ou não.

  :param com_retweets: indicador se retweets estão permitidos na captura
  :param probabilidades: probabilidades de o tweet ser ou não sorteado como retweet, True ou False, respectivamente
  :return: se foi sorteado ou não como um retweet
  """
  try:
    return False if not com_retweets else choice(_OPCOES_RETWEET, 1, p=probabilidades)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'retweet')


def tweet_url(screen_name:str, id:str):
  """Função que elabora uma simulação de endereço web para o tweet simulado.

  :param screen_name: o nome de usuário (@usuario)
  :param id: o id que foi atribuído à simulação
  :return: o url simulado
  """
  try:
    return URL_RAIZ + screen_name + '/' + id + '/'

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_url')


def __relacionamento(relacionamentos:list=_OPCOES_RELACIONAMENTO, probabilidades:list=_PROBABILIDADES_RELACIONAMENTO):
  """Função privada que simula o estabelecimento de um relacionamento, com chance ponderada.

  :param relacionamentos: lista com os relacionamentos possíveis
  :param probabilidades: lista com a probabilidade de um dos relacionamentos listados ser selecionado
  :return: id do relacionamento sorteado
  """
  try:
    return choice(relacionamentos, 1, p=probabilidades)[0]

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__relacionamento')


def tweet_usuarios_mencionados(usuarios_mencionados_tweet:list):
  """Função que recebe uma lista de usuários mencionados e a acomoda em uma estrutura de dados padronizada e simula um
  relacionamento com o usuário origem do tweet.

  :param usuarios_mencionados_tweet: lista de dicionários de usuários mencionados
  :return: lista de nenhum ou de dicionário(s) de usuário(s) mencionado(s)
  """
  try:
    if usuarios_mencionados_tweet:
      lista_usuarios = []
      for usuario in usuarios_mencionados_tweet:
        lista_usuarios.append({
          'screen_name': usuario.screen_name,
          'id_str': usuario.id_str,
          'relacionamento': __relacionamento()
        })
      return lista_usuarios

    else:
      return []

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tweet_usuarios_mencionados')


def in_reply_to_status_id_str(usuarios_mencionados_tweet:list, probabilidade_none:float=_PROBABILIDADE_SEM_RESPONDIDO):
  """Função que recebe usuários mencionados em tweet e, de forma aleatória, retorna um ou nenhum como o em resposta.

  :param usuarios_mencionados_tweet: lista de dicionários de usuários mencionados
  :param probabilidade_none: probabilidade de ser selecionado nenhum usuário
  :return: nenhum ou um usuário, neste último caso, retornando o dicionário em_resposta
  """
  try:
    if usuarios_mencionados_tweet != None and usuarios_mencionados_tweet != []:
      usuarios = [None] + usuarios_mencionados_tweet
      qtd_usuarios = len(usuarios_mencionados_tweet)
      prob_usuarios = (1 - probabilidade_none) / qtd_usuarios
      probabilidades = [probabilidade_none]
      for n in range(qtd_usuarios):
        probabilidades.append(prob_usuarios)

      escolhido = choice(usuarios, 1, p=probabilidades)[0]

      if hasattr(escolhido, 'screen_name'):
        return {'resposta_ao_tweet': '-2',
                'screen_name': escolhido.screen_name,
                'id_str': escolhido.id_str,
                'relacionamento': __relacionamento()}

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'in_reply_to_status_id_str')


__doc__ = """Módulo com recursos para criar simulações dos valores de atributos de um tweet."""
