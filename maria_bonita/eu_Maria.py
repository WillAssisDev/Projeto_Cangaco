import tweepy as tw
from datetime import datetime
from utilidades import tratamento_erros as te
from utilidades import autenticacao
from utilidades.formatar_data import formatar as data


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.eu_Maria.'


class Instancia_Conexao_API():
  """Superclasse onde estão estruturados atributos e métodos dos dados de instância da conexão no endpoint ou simulação
  desta."""

  def __init__(self, API:tw.API=None, **kwargs):
    """Método construtor.

    :param API: instância da API Tweepy, conectada no end-point.
    :param kwargs: lista dinâmica de argumentos em que devem ser indexados atributos de um simulacro de Instancia_Conexao_API
    """
    try:
      if API:
        dados_conexao = API.me()

        self.id = dados_conexao.id
        self.id_str = dados_conexao.id_str
        self.screen_name = dados_conexao.screen_name
        self.name = dados_conexao.name
        self.description = dados_conexao.description
        self.verified = dados_conexao.verified
        self.location = dados_conexao.location
        self.profile_location = dados_conexao.profile_location
        self.profile_image_url = dados_conexao.profile_image_url
        self.profile_banner_url = dados_conexao.profile_banner_url
        self.followers_count = dados_conexao.followers_count
        self.friends_count = dados_conexao.friends_count
        self.statuses_count = dados_conexao.statuses_count
        self.created_at = data(dados_conexao.created_at)

      else:
        self.id = kwargs['id'] if 'id' in kwargs else 3.14159265359
        self.id_str = str(self.id)
        self.screen_name = kwargs['screen_name'] if 'screen_name' in kwargs else 'nao_definido'
        self.name = kwargs['name'] if 'name' in kwargs else self.screen_name.replace('_', ' ').capitalize()
        self.description = kwargs['description'] if 'description' in kwargs else 'Descrição padrão'
        self.verified = False
        self.location = None
        self.followers_count = 0
        self.friends_count = 0
        self.statuses_count = 0
        self.profile_image_url = kwargs['profile_image_url'] if 'profile_image_url' in kwargs else \
          'https://ronaldmottram.co.nz/wp-content/uploads/2019/01/default-user-icon-8.jpg'
        self.profile_banner_url = None
        self.created_at = data(datetime.today())

      self.profile_url = 'https://twitter.com/' + self.screen_name + '/'
      self.__json = self.__constroi_json()

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Instancia_Conexao_API.__init__')

  @property
  def json(self):
    return self.__json

  def incrementa_statuses_count(self):
    self.statuses_count += 1
    self.__json['statuses_count'] += 1

  def __constroi_json(self):
    return {
      'screen_name': self.screen_name,
      'name': self.name,
      'id': self.id,
      'id_str': self.id_str,
      'profile_url': self.profile_url,
      'verified': self.verified,
      'location': self.location,
      'description': self.description,
      'followers_count': self.followers_count,
      'friends_count': self.friends_count,
      'statuses_count': self.statuses_count,
      'profile_image_url': self.profile_image_url,
      'profile_banner_url': self.profile_banner_url,
      'created_at': self.created_at
    }


class __Eu_Maria(Instancia_Conexao_API):
  """Se achegue, cabra. Eu sou a MB!"""

  def __init__(self):
    """Método construtor.
    """
    try:
      auth = autenticacao.autenticar()
      API = tw.API(auth)

      super().__init__(API)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + '__Eu_Maria.__init__')


class __Durvinha(Instancia_Conexao_API):
  """- A senhora atirou muito no cangaço? - Não.. eu tinha um medo danado de atirar."""

  def __init__(self):
    """
    Método construtor.
    """
    super().__init__(id=-1,
                     screen_name='durvinha',
                     name='Maria Jovina',
                     description='Diz qui cê é muito macho nas brigadas, quiria vê se é home memo',
                     profile_image_url='https://i.pinimg.com/564x/ff/4e/be/ff4ebe3b9611a8b3e9d1ad89b9c86bea.jpg')


class __Joao_Ninguem(Instancia_Conexao_API):
  """Eu sou irrelevante."""

  def __init__(self):
    """Método construtor.
    """
    super().__init__(id=-2,
                     screen_name='joao_ninguem',
                     name='João Ninguém',
                     description='Eu sou ninguém.',
                     profile_image_url='https://www.fbi.gov/wanted/vicap/unidentified-persons/john-doe-21/@@images/image/large')


class __Aletorio(Instancia_Conexao_API):
  """Objeto correspondente a instância de uma menção aletória."""

  def __init__(self):
    """Método construtor.
    """
    super().__init__(id=-3,
                     screen_name='mencao_aleatoria',
                     name='Menção Aleatória',
                     description='Estou aqui para menções aleatórias em tweets',
                     profile_image_url='https://norrismgmt.com/wp-content/uploads/2020/05/24-248253_user-profile-default-image-png-clipart-png-download.png')


MB = __Eu_Maria()
MJ = __Durvinha()
JN = __Joao_Ninguem()
ALEATORIO = __Aletorio()


__doc__ = """Módulo em que são instanciados os dados da conexão com o end-point do Twitter. Também são estruturados
simulacros desta conexão."""
