import utilidades.tratamento_erros as te
from maria_bonita.modelos.utilidades.StatusSimulado import Status_Simulado
from maria_bonita.modelos.utilidades.StreamListenerSimulado import StreamListenerSimulado
from maria_bonita.eu_Maria import Instancia_Conexao_API


_CAMINHO_MODULO = 'maria_bonita.modelos.utilidades.StreamMB.'
_COM_STOPWORDS = True
_PLATAFORMA = 'MB'


class StreamMB:
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
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamMB.__init__')

  def filter_adjetivos(self, chaves_busca:list, dict_frases_projetadas:dict):
    """Método que cria uma lista de projeções de textos, acrescentando chaves e usuários mencionados. A lista criada é
    percorrida e a informação é estruturada, sendo que, ao final de cada iteração, o dicionário da projeção é
    acrescentado na lista de dicionários de projeções do receptor da transmissão.

    :param chaves_busca: lista de objetos chave de busca
    :param dict_frases_projetadas: dicionários, no singular e plural, que contém expressões para serem somadas as chaves e caracterizarem crime
    :return: lista de dicionários de projeções de tweets
    """
    try:
      projecoes_frases_chaves = []
      if 'singular' in dict_frases_projetadas:
        chaves = []
        for chave in chaves_busca:
          chaves += chave.adjetivos_singular
        projecoes_frases_chaves.append({
          'frases': dict_frases_projetadas['singular'],
          'chaves': chaves.copy(),
          'mencionados': [self.usuarios_mencionados[0]]
        })
      if 'plural' in dict_frases_projetadas:
        chaves = []
        for chave in chaves_busca:
          chaves += chave.adjetivos_plural
        projecoes_frases_chaves.append({
          'frases': dict_frases_projetadas['plural'],
          'chaves': chaves.copy(),
          'mencionados': self.usuarios_mencionados
        })

      dict_frases_projetadas = None
      chave = None
      del dict_frases_projetadas
      del chave

      lista_dict_projecoes = []
      for dict_projecoes in projecoes_frases_chaves:
        frases = dict_projecoes['frases']
        chaves = dict_projecoes['chaves']
        screen_name = None
        for mencionado in dict_projecoes['mencionados']:
          if not screen_name: screen_name = '@' + mencionado.screen_name
          else: screen_name += ' @' + mencionado.screen_name

        for frase in frases:
          for chave in chaves:
            lista_dict_projecoes += [
              {
                'projecao': frase + ' ' + chave,
                'autor': self.autor,
                'usuario': self.usuario,
                'mencionados': None
               },
              {
                'projecao': screen_name + ' ' + frase + ' ' + chave,
                'autor': self.autor,
                'usuario': self.usuario,
                'mencionados': [mencionado]
              },
              {
                'projecao': frase + ' ' + chave + ' ' + screen_name,
                'autor': self.autor,
                'usuario': self.usuario,
                'mencionados': [mencionado]
              }
            ]

      projecoes_frases_chaves = None
      dict_projecoes = None
      frases = None
      chaves = None
      mencionado = None
      screen_name = None
      frase = None
      chave = None
      del projecoes_frases_chaves
      del dict_projecoes
      del frases
      del chaves
      del mencionado
      del screen_name
      del frase
      del chave

      for dict_projecoes in lista_dict_projecoes:
        status = Status_Simulado(
          projecao_tweet=dict_projecoes['projecao'],
          autor=dict_projecoes['autor'],
          usuario=dict_projecoes['usuario'],
          mencionados=dict_projecoes['mencionados'],
          plataforma=_PLATAFORMA
        )

        tweet_simulado_MB = self.listener.on_status(
          status=status,
          chaves_busca=chaves_busca,
          com_stopwords=_COM_STOPWORDS
        )

        self.listener.lista_resultados.append(tweet_simulado_MB)

        self.usuario.incrementa_statuses_count()

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamMB.filter_adjetivos')


__doc__ = """Módulo criado para reproduzir a mesma sequência lógica utilizada em uma captura real de dados no Twitter."""