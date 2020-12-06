import utilidades.tratamento_erros as te
from utilidades.formatar_data import formatar as data
from maria_bonita.conjunto_dados.utilidades.captura.ferramentas_conjunto_dados import IDIOMA_PADRAO
import maria_bonita.modelos.utilidades.atributos_simulados as simula
from maria_bonita.eu_Maria import Instancia_Conexao_API


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.modelos.utilidades.StatusSimulado.'


class _Entities:
  """Classe entidades, criada somente para replicar nas simulações a mesma estrutura de dados utilizada pelo Twitter."""

  def __init__(self, mencionados:list):
    """Método construtor.

    :param mencionads: lista de usuários, instâncias de eu_Maria.Instancia_Conexao_API
    """
    try:
      self.hashtags = []
      self.urls = []
      self.user_mentions = mencionados

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + '_Entities.__init__')


class Status_Simulado:
  """Classe para representar a mesma estrutura de dados utilizada pelo Twitter na estruturação de um tweet."""

  def __init__(self, projecao_tweet:str, autor:Instancia_Conexao_API, usuario:Instancia_Conexao_API, mencionados:list,
               plataforma:str='MB', idioma:str=IDIOMA_PADRAO):
    """Método construtor.

    :param projecao_tweet: o texto simulado do tweet
    :param autor: o autor simulado do tweet, instância de eu_Maria.Instancia_Conexao_API
    :param usuario: o usuário origem simulado do tweet
    :param mencionados: lista de usuários mencionados (instâncias de Instancia_Conexao_API) em projecao_tweet
    :param plataforma: sigla para identificar origem da simulação
    :param idioma: idioma utilizado na simulação
    """
    try:
      self.created_at =                data()
      self.retweet =                   simula.retweet()
      self.id =                        usuario.statuses_count
      self.id_str =                    str(self.id)
      self.text =                      projecao_tweet
      self.entities =                  _Entities(mencionados)
      self.source =                    plataforma
      self.in_reply_to_status_id_str = simula.in_reply_to_status_id_str(mencionados)
      self.lang =                      idioma
      self.author =                    autor
      self.user =                      usuario
      self._json =                     None

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Status_Simulado.__init__')


__doc__ = """Módulo em que foi recriada a estrutura de dados (considerando o escopo do projeto), utilizada pelo Twitter
na estruturação da informação contida em um tweet."""