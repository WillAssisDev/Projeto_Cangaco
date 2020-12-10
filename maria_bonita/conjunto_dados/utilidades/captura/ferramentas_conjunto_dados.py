from pandas import isna
from random import choice
import maria_bonita.conjunto_dados.utilidades.captura.API_Personalizada as ap
import maria_bonita.conjunto_dados.utilidades.captura.chaves_busca as chaves_busca
import utilidades.tratamento_erros as te
import maria_bonita.conjunto_dados.utilidades.pre_processamento.conversor_str_2_struct as cs2s


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.conjunto_dados.simulacao.captura.ferramentas_conjunto_dados.'

# parametrização
QUANTIDADE_TWEETS = 2000
COM_RETWEETS = False
IDIOMA_PADRAO = 'pt'
IDIOMAS_PADRAO = [IDIOMA_PADRAO]
DIRETORIO_SAIDA = './saida/'
FORMATO_SAIDA = '.csv'

# relacionamento
INDEFINIDO = -1
NAO_RELACIONADOS = 0
AMIZADE = 1
SEGUINDO = 2
SEGUIDO = 3


def parametros(chaves_busca:list=(chaves_busca.LISTA_GERAL), quantidade_tweets:int=QUANTIDADE_TWEETS,
               com_retweets:bool=COM_RETWEETS, idiomas:list=IDIOMAS_PADRAO):
  """Função para facilitar a parametrização do conjunto de dados sendo gerado.

  :param chaves_busca: lista de objetos chave de busca
  :param quantidade_tweets: inteiro que indica a quantidades de tweets que deverão ser capturados
  :param com_retweets: booleano que indica se, no streaming, deverão ser capturados retweets
  :param idiomas: lista dos idiomas monitorados no streaming
  :return: tupla com os parâmetros configurados, respectivamente: chaves_selecionadas, quantidade_tweets, com_retweets, idiomas, caminho_saida
  """
  try:
    chaves_selecionadas = []
    caminho_saida = ''

    for chave in chaves_busca:
      if not caminho_saida:
        caminho_saida = chave.rotulo
      else:
        caminho_saida += '_' + chave.rotulo
      chaves_selecionadas += chave.lista_chaves
    caminho_saida = DIRETORIO_SAIDA + caminho_saida + FORMATO_SAIDA

    return chaves_selecionadas, quantidade_tweets, com_retweets, idiomas, caminho_saida

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'parametros')


def __relacionar_usuarios(API:ap.API, usuario_id_origem:str, usuario_id_alvo:str):
  """Função privada para estabelecer o relacionamento entre o usuário origem e o usuário alvo. Se a propriedade PRODUCAO
  do objeto API for TRUE, é realizada conexão no end-point do Twitter para estabelecer o relacionmaneto. Se a
  propriedade for FALSE, é realizada uma simulação através do módulo RANDOM.

  :param API: a instância da API criada
  :param usuario_id_origem: ID do usuário que publicou
  :param usuario_id_alvo: ID do usuário mencionado ou respondido
  :return: A API, com taxa limite atualizada e o ID correspondente ao relacionamento entre os usuários origem e alvo
  """
  relacionamento = INDEFINIDO

  recurso_application = API.recurso_api('application')
  recurso_friendship_show = API.recurso_api('friendship_show')

  try:
    atingiu_limite_application = recurso_application.contador >= recurso_application.limite
    atingiu_limite_friendship_show = recurso_friendship_show.contador >= recurso_friendship_show.limite

    if not atingiu_limite_application and not atingiu_limite_friendship_show:
      if API.producao:
        amizade = API.api.show_friendship(source_id=int(usuario_id_origem), target_id=int(usuario_id_alvo))

        seguindo = amizade[0].following
        seguido = amizade[0].followed_by

        if seguindo and seguido:
          relacionamento = AMIZADE
        elif seguindo:
          relacionamento = SEGUINDO
        elif seguido:
          relacionamento = SEGUIDO
        else:
          relacionamento = NAO_RELACIONADOS

      else:
        relacionamento = choice([AMIZADE, SEGUINDO, SEGUIDO, NAO_RELACIONADOS])

      API.contabiliza_acessos_recursos([ap.Application, ap.FriendshipShow])

      print("\nChamadas API:", API.status_acessos)

    else:
      API = API.reset_API()

    return API, relacionamento

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__relacionar_usuarios')
    API.contabiliza_acessos_recursos([ap.Application, ap.FriendshipShow])
    return API, relacionamento

  except ConnectionError as erro:
    te.connection_error(erro, _CAMINHO_MODULO + '__relacionar_usuarios')
    return ap.API(), relacionamento


def relacionamento_com_mencionados(API:ap.API, usuario_id_origem:str, mencionados:list):
  """Função que recebe os usuários mencionados e estabele o relacionamento entre eles e o usuário que publicou.

  :param API: a instância da API criada
  :param usuario_id_origem: ID do usuário que publicou
  :param mencionados: lista de dicionários de usuários mencionados
  :return: lista de dicionários dos usuários mencionadas, agora com o ID do relacionamento com o usuário origem
  """
  try:
    tipo_mencionados = type(mencionados)
    nao_esta_vazio = bool((mencionados != '[]' and tipo_mencionados == str) or (len(mencionados) and tipo_mencionados == list))
    if nao_esta_vazio:
      if tipo_mencionados == str: mencionados = cs2s.converter_str_em_list_dict(mencionados)

      for mencao in mencionados:
        API, mencao['relacionamento'] = __relacionar_usuarios(API, usuario_id_origem, mencao['id_str'])

    return mencionados

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'relacionamento_com_mencionados')
    return mencionados


def relacionamento_com_respondido(API:ap.API, usuario_id_origem:str, mencionados:list, em_resposta:dict):
  """Função que recebe o usuário respondido e estabele o relacionamento entre ele e o usuário que publicou. Se o usuário
  respondido tiver sido mencionado, para reduzir o gasto da taxa de limite de chamadas no end-point do Twitter, localiza
  o ID de relacionamento na lista MENCIONADOS.

  :param API: a instância da API criada
  :param usuario_id_origem: ID do usuário que publicou
  :param mencionados: lista de dicionários de usuários mencionados
  :param em_resposta: dicionário do usuário respondido
  :return: lista de dicionários dos usuários mencionadas, agora com o ID do relacionamento com o usuário origem
  """

  try:
    nao_esta_vazio = not isna(em_resposta)
    if nao_esta_vazio:
      if type(em_resposta) == str: em_resposta = cs2s.converter_str_em_dict(em_resposta)

      tipo_mencionados = type(mencionados)
      nao_esta_vazio = bool((mencionados != '[]' and tipo_mencionados == str) or (len(mencionados) and tipo_mencionados == list))
      if nao_esta_vazio:
        if tipo_mencionados == str: mencionados = cs2s.converter_str_em_list_dict(mencionados)

        for mencao in mencionados:
          if mencao['id_str'] == em_resposta['id_str']:
            em_resposta['relacionamento'] = mencao['relacionamento']
            return em_resposta

      API, em_resposta['relacionamento'] = __relacionar_usuarios(API, usuario_id_origem, em_resposta['id_str'])
      return em_resposta

    return em_resposta

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'relacionamento_com_respondido')
    em_resposta['relacionamento'] = INDEFINIDO
    return em_resposta


__doc__ = """Módulo com recursos para a parametrização do conjunto de dados e conclusão de captura."""
