from pandas import isna
import utilidades.tratamento_erros as te
import maria_bonita.conjunto_dados.utilidades.pre_processamento.conversor_str_2_struct as cs2s
import maria_bonita.conjunto_dados.utilidades.pre_processamento.tokenizacao as tk
import maria_bonita.conjunto_dados.utilidades.captura.ferramentas_conjunto_dados as fcd


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.pre_processamento.novas_variaveis.'
COM_STOPWORDS = True


def __mapear_relacionamento(numero_relacionamento:int):
  """Função privada que recebe o ID correspondente a um relacionamento e o traduz para seu respectivo significado.

  :param numero_relacionamento: ID de relacionamento
  :return: relacionamento em linguagem natural
  """
  try:
    if not isinstance(numero_relacionamento, int): numero_relacionamento = int(numero_relacionamento)
    if numero_relacionamento == fcd.INDEFINIDO:
      return 'indefinido'
    elif numero_relacionamento == fcd.NAO_RELACIONADOS:
      return 'não relacionados'
    elif numero_relacionamento == fcd.AMIZADE:
      return 'amizade'
    elif numero_relacionamento == fcd.SEGUINDO:
      return 'seguindo'
    elif numero_relacionamento == fcd.SEGUIDO:
      return 'seguido'

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__mapear_relacionamento')


def relacionamento_com_mencionados(mencionados:list):
  """Função que recebe os usuários mencionados com os respectivos IDs de relacionamentos com o usuário que publicou e os
  traduz.

  :param mencionados: lista de dicionários dos usuários mencionados e respectivos IDs de relacionamentos
  :return: lista de dicionários dos usuários mencionados e respectivos relacionamentos em lingaugem natural
  """
  try:
    relacionamento_com_mencionados = []

    tipo_mencionados = type(mencionados)
    nao_esta_vazio = bool((mencionados != '[]' and tipo_mencionados == str) or (len(mencionados) and tipo_mencionados == list))

    if nao_esta_vazio:
      if tipo_mencionados == str: mencionados = cs2s.converter_str_em_list_dict(mencionados)

      for mencao in mencionados:
        relacionamento_com_mencionados.append({'usuario': mencao['screen_name'],
                                               'relacionamento': __mapear_relacionamento(mencao['relacionamento'])})

    return relacionamento_com_mencionados if len(relacionamento_com_mencionados) else ''

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'relacionamento_com_mencionados')


def relacionamento_com_respondido(em_resposta:dict):
  """Função que recebe o usuário respondido com o respectivo IDs de relacionamento com o usuário que publicou e o
  traduz.

  :param em_resposta: dicionário com o usuário respondido e respectivo IDs de relacionamento
  :return: dicionário do usuário respondido e respectivo relacionamento em lingaugem natural
  """
  try:
    relacionamento_com_respondido = ''

    nao_esta_vazio = not isna(em_resposta)
    if nao_esta_vazio:
      if type(em_resposta) == str: em_resposta = cs2s.converter_str_em_dict(em_resposta)

      relacionamento_com_respondido = {'usuario': em_resposta['screen_name'],
                                       'relacionamento': __mapear_relacionamento(em_resposta['relacionamento'])}

    return relacionamento_com_respondido

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'relacionamento_com_respondido')


def tokenizar(tweet_texto:str, chaves_busca:list, mencionados:list, vocabulario:list):
  """ Função que recebe um tweet cru e lhe aplica os tratamentos necessários para o posterior processamento.

  :param tweet_texto: o tweet não tratado
  :param chaves_busca: lista que contém os objetos das chaves de busca e respectivos rótulos
  :param usuarios_mencionados: lista de dicionários de usuários mencionados no tweet
  :param vocabulario: lista com o vocabulario, para forçar que stopwords presentes não sejam removidas
  :return: tweet tratado: stopwords e não alfanuméricos removidas, descapitalização e menções, números e emojis normalizados
  """
  try:
    tipo_mencionados = type(mencionados)
    nao_esta_vazio = bool((mencionados != '[]' and tipo_mencionados == str) or (len(mencionados) and tipo_mencionados == list))

    if nao_esta_vazio:
      if tipo_mencionados == str: mencionados = cs2s.converter_str_em_list_dict(mencionados)
      lista_screen_names = [mencao['screen_name'] for mencao in mencionados]

      return tk.tokenizar(tweet_texto, chaves_busca, lista_screen_names, vocabulario)
    return tk.tokenizar(tweet_texto, chaves_busca, [], vocabulario)

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'tokenizar')


def novas_variaveis(dicionario_tweet:dict, chaves_busca:list, possivel_crime=None, vocabulario:list=[]):
  """Função que recebe um dicionário de tweet e cria novos atributos.

  :param dicionario_tweet: o dicionário de um tweet
  :param chaves_busca: lista de objetos chave de busca
  :param possivel_crime: valor para indicador ou não tweet criminoso
  :param vocabulario: lista com o vocabulario, para forçar que stopwords presentes não sejam removidas
  :return: o dicionário do tweet, com as novas variáveis incorporadas
  """
  try:
    dicionario_tweet['relacionamento_com_mencionados'] = relacionamento_com_mencionados(dicionario_tweet['tweet_usuarios_mencionados'])

    dicionario_tweet['relacionamento_com_respondido'] = relacionamento_com_respondido(dicionario_tweet['tweet_em_resposta'])

    dicionario_tweet['texto_original'] = dicionario_tweet['tweet_texto']

    dicionario_tweet['tokens'] = tokenizar(tweet_texto=dicionario_tweet['texto_original'],
                                           chaves_busca=chaves_busca,
                                           mencionados=dicionario_tweet['tweet_usuarios_mencionados'],
                                           vocabulario=vocabulario)

    dicionario_tweet['possivel_crime'] = possivel_crime

    return dicionario_tweet

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'novas_variaveis')


__doc__ = """Módulo com recursos para criação de novas variáveis, somente baseadas em um conjunto de dados já criado,
o deixando mais inteligível (em linguagem natural), com objetivo de facilitar a classificação manual."""
