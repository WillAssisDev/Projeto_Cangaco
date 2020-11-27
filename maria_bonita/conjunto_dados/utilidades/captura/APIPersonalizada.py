import tweepy as tw
from time import sleep
from datetime import datetime
from autenticacao import autenticar
import maria_bonita.conjunto_dados.utilidades.tratamento_erros as te


# CONSTANTES
CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.captura.APIPersonalizada.'

PAUSA_API = 900
LIMITE_FICTICIO_API = 150
PAUSA_FICTICIA_API = 15




class RecursoAPI():
  """Super classe que representa, genericamente, a taxa limite dos recursos da API, em que são criados seus atributos,
  métodos e propriedades."""

  def __init__(self, producao:bool):
    self._producao = producao
    self._limite = None
    self.__contador = 0

  @property
  def limite(self):
    return self._limite

  @property
  def contador(self):
    return self.__contador

  def contabiliza_acesso(self):
    self.__contador += 1


class Application(RecursoAPI):
  """Classe que representa a taxa limite do recurso Application.
  """
  def __init__(self, api:tw.API, producao:bool):
    super().__init__(producao)
    try:
      limite = int(api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining'])
      self._limite = limite if self._producao else LIMITE_FICTICIO_API

    except ConnectionError as erro:
      te.connection_error(erro, CAMINHO_MODULO + 'Application.__init__')


class FriendshipShow(RecursoAPI):
  """Classe que representa a taxa limite do recurso Friendshipshow.
  """
  def __init__(self, api:tw.API, producao:bool):
    super().__init__(producao)
    try:
      limite = int(api.rate_limit_status()['resources']['friendships']['/friendships/show']['remaining'])
      self._limite = limite if self._producao else LIMITE_FICTICIO_API

    except ConnectionError as erro:
      te.connection_error(erro, CAMINHO_MODULO + 'FriendshipShow.__init__')


class API():
  """Classe com novos recursos customizados para o Projeto Cangaço, facilitando o gerenciamento dos limites dos recursos
  do end-point do Twitter. Também possibilita a simulação de conexão, em que, no lugar dos limites dos recursos do
  end-point, é estabelecido um limite fictício.
  """

  def __init__(self, producao:bool=True):
    """Método construtor.

    :param producao: indica se deve ser realizada a conexão com o end-point do Twitter. Se falso, realiza a simulação de conexão (necessária para validar outros recursos, sem comprometer a taxa limite)
    """
    try:
      self.__producao = producao
      self.__auth = autenticar() if producao else None
      self.__api = tw.API(self.__auth) if producao else None
      self.__pausa_em_limite_api = PAUSA_API if producao else PAUSA_FICTICIA_API
      self.__recursos_api = [Application(self.__api, self.__producao), FriendshipShow(self.__api, self.__producao)]

    except ConnectionError as erro:
      te.connection_error(erro, CAMINHO_MODULO + 'API.__init__')

  @property
  def producao(self):
    """Propriedade booleana que indica se a API é instanciada para Produção.
    """
    return self.__producao

  @property
  def api(self):
    """Propriedade da instância da API Tweepy.
    """
    return self.__api

  @property
  def recursos_api(self):
    """Propriedade com a lista de recursos instanciados na API."""
    return self.__recursos_api

  def __localizar_recurso_api(self, classe: RecursoAPI):
    """Função privada que recebe a classe de um recurso e localiza suas instância.

    :param classe: a classe do recurso desejado
    :return: instãncia do recurso indicado
    """
    for recurso in self.recursos_api:
      if isinstance(recurso, classe):
        return recurso

  def recurso_api(self, recurso):
    """Função em que é indicado um recurso e o mesmo é retornado.

    :param recurso: o recurso desejado, podendo ser indicado pelo índice ou classe
    :type recurso: str or int
    :return: instãncia, no contexto da classe API, do recurso indicado
    """
    if type(recurso) == int: return self.recursos_api[recurso]
    # RECURSOS API
    elif type(recurso) == str:
      recurso = recurso.lower()
      if recurso == 'application': return self.__localizar_recurso_api(Application)
      elif recurso == 'friendship_show': return self.__localizar_recurso_api(FriendshipShow)

  @property
  def status_acessos(self):
    """Propriedade que mede a taxa de acessos dos recursos, indicando o que está mais próximo de atingir o limite de
    chamadas no end-point do Twitter.
    """
    recurso_mais_acessado = None
    maxima_taxa_acessos = 0

    for recurso in self.recursos_api:
      calculo_taxa_acesso = ((recurso.contador + 1) / (recurso.limite + 1))
      if calculo_taxa_acesso > maxima_taxa_acessos:
        recurso_mais_acessado = recurso
        maxima_taxa_acessos = calculo_taxa_acesso
    return f"{recurso_mais_acessado.contador}/{recurso_mais_acessado.limite}"

  def reset_API(self):
    """Método para gerenciar as chamadas no end-point do Twitter. Para respeitar o limite de consultas, pausa as
    chamadas durante o tempo indicado em __pausa_em_limite_api. Ao fim da pausa, reatribui __recursos_api.
    """
    print(f"\n\n{datetime.now().strftime('%H:%M:%S')}: foi atingido o limite de requisições " +
          f"da API. A consulta será pausada por {int(self.__pausa_em_limite_api / 60)} minutos.\n")
    sleep(self.__pausa_em_limite_api)

    print("REINICIANDO", end=' ')
    sleep(1)
    print(".", end=' ')
    sleep(1)
    print(".", end=' ')
    sleep(1)
    print(".", end='\n\n')
    sleep(1)

    self.__recursos_api = [Application(self.api, self.producao), FriendshipShow(self.api, self.producao)]


__doc__ = """Módulo em que é sobrescrita a API do módulo Tweepy, criando novos recursos customizados para o Projeto
Cangaço."""
