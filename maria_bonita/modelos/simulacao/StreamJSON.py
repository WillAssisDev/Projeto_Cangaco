import json
import utilidades.tratamento_erros as te
from maria_bonita.modelos.simulacao.StatusSimulado import Status_Simulado
from maria_bonita.modelos.simulacao.StreamListenerSimulado import StreamListenerSimulado
from maria_bonita.eu_Maria import Instancia_Conexao_API


_CAMINHO_MODULO = 'maria_bonita.modelos.simulacao.StreamJSON.'


class StreamJSON:
  """Classe para simular a transmissão de tweets. Na realidade, primeiramente, são criadas todas as projeções de textos
  de tweets, que então são iteradas e o dados são estruturados"""

  def __init__(self, listener:StreamListenerSimulado, usuarios_mencionados:list, autor:Instancia_Conexao_API,
               usuario:Instancia_Conexao_API):
    """Método construtor.

    :param listener: receptor simulado de uma transmissão de tweets simulada
    :param usuarios_mencionados: lista de usuários (instâncias de Instancia_Conexao_API) que deverão ser utilizados nas projeções
    :param autor: autor do tweet, instância de Instancia_Conexao_API
    :param usuario: usuário origem do tweet, instância de Instancia_Conexao_API
    """
    try:
      self.listener = listener
      self.usuarios_mencionados = usuarios_mencionados
      self.autor = autor
      self.usuario = usuario

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamJSON.__init__')

  def filter_fixos(self, chaves_busca:list, chaves_mencoes:list, lista_arquivos_json:list, vocabulario:list=[]):
    """

    :param chaves_busca: lista de objetos chave de busca
    :param chaves_mencoes: lista de strings de screen_names genéricos que serão monitorados para substituição
    :param lista_json: lista arquivos json de que serão extraídas projeções
    :param vocabulario: lista com o vocabulario, para forçar que stopwords presentes não sejam removidas
    :return: lista de dicionários de projeções de tweets
    """
    try:
      lista_dict_json = []
      for arquivo_json in lista_arquivos_json:
        with open(arquivo_json, 'r', encoding='utf-8') as arquivo:
          lista_dict_json.append(json.load(arquivo))

      lista_dict_projecoes = []
      for dict_json in lista_dict_json:
        lista_dicionario_textos = dict_json['tweets']['singular'] + dict_json['tweets']['plural']

        for dicionario_texto in lista_dicionario_textos:
          texto = dicionario_texto['texto']

          mencionados_texto = []
          for n in range(len(chaves_mencoes)):
            if chaves_mencoes[n] in texto:
              texto = texto.replace(chaves_mencoes[n], self.usuarios_mencionados[n].screen_name)
              texto = texto.replace(chaves_mencoes[n].upper(), self.usuarios_mencionados[n].name)
              mencionados_texto.append(self.usuarios_mencionados[n])
          if not len(mencionados_texto): mencionados_texto = None

          dict_projecoes = {
            'projecao': texto,
            'autor': self.autor,
            'usuario': self.usuario,
            'mencionados': mencionados_texto,
            'hashtags': dicionario_texto['hashtags'],
            'urls': dicionario_texto['urls'],
            'plataforma': dict_json['plataforma']
          }

          lista_dict_projecoes.append(dict_projecoes)

      for dict_projecoes in lista_dict_projecoes:
        status = Status_Simulado(
          projecao_tweet= dict_projecoes['projecao'],
          autor=          dict_projecoes['autor'],
          usuario=        dict_projecoes['usuario'],
          mencionados=    dict_projecoes['mencionados'],
          hashtags=       dict_projecoes['hashtags'],
          urls=           dict_projecoes['urls'],
          plataforma=     dict_projecoes['plataforma']
        )

        tweet_simulado_JSON = self.listener.on_status(
          status=       status,
          chaves_busca= chaves_busca,
          vocabulario=  vocabulario
        )

        self.listener.lista_resultados.append(tweet_simulado_JSON)

        self.usuario.incrementa_statuses_count()

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamJSON.filter_fixos')


__doc__ = """Módulo criado para reproduzir a mesma sequência lógica utilizada em uma captura real de dados no Twitter,
cujos textos dos tweets utilizados nas projeções são importados de arquivos json e foram recebidos anonimamente."""
