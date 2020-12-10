import utilidades.tratamento_erros as te


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.conjunto_dados.simulacao.captura.chaves_busca.'


class Chave_Busca:
  """Classe para rotular e instanciar chaves de busca, que serão utilizadas na captura de Tweets."""

  def __init__(self, rotulo:str, adjetivos_singular:list=[], adjetivos_singular_erro:list=[], adjetivos_plural:list=[],
               adjetivos_plural_erro:list=[], substantivos_singular:list=[], substantivos_singular_erro:list=[],
               substantivos_plural:list=[], substantivos_plural_erro:list=[], verbos_infinitivo:list=[],
               verbos_infinitivo_erro:list=[], verbos_presente_singular:list=[], verbos_presente_singular_erro:list=[],
               verbos_presente_plural:list=[], verbos_presente_plural_erro:list=[], verbos_passado_singular:list=[],
               verbos_passado_singular_erro:list=[], verbos_passado_plural:list=[], verbos_passado_plural_erro:list=[],
               lista_normalizacao:list=[]):
    """Método construtor.

    :param rotulo: palavra ou expressão que designa o conjunto de chaves de busca
    :param adjetivos_singular: lista de adjetivos, no singular
    :param adjetivos_singular_erro: lista de adjetivos, com erros na grafia, no singular
    :param adjetivos_plural: lista de adjetivos, no plural
    :param adjetivos_plural_erro: lista de adjetivos, com erros na grafia, no plural
    :param substantivos_singular: lista de substantivos, no singular
    :param substantivos_singular_erro: lista de substantivos, com erros na grafia, no singular
    :param substantivos_plural: lista de substantivos, no plural
    :param substantivos_plural_erro: lista de substantivos, com erros na grafia, no plural
    :param verbos_infinitivo: lista de verbos, no infinitivo
    :param verbos_infinitivo_erro: lista de verbos, com erros na grafia, no infinitivo
    :param verbos_presente_singular: lista de verbos, no presente e singular
    :param verbos_presente_singular_erro: lista de verbos, com erros na grafia, no presente e singular
    :param verbos_presente_plural: lista de verbos, no presente e plural
    :param verbos_presente_plural_erro: lista de verbos, com erros na grafia, no presente e plural
    :param verbos_passado_singular: lista de verbos, no passado e singular
    :param verbos_passado_singular_erro: lista de verbos, com erros na grafia, no passado e singular
    :param verbos_passado_plural: lista de verbos, no passado e plural
    :param verbos_passado_plural_erro: lista de verbos, com erros na grafia, no passado e plural
    :param lista_normalizacao: a lista de tuplas para normalizar erros de digitação nas chaves de busca
    """
    try:
      self.__rotulo = rotulo.lower()
      self.adjetivos_singular = adjetivos_singular
      self.adjetivos_singular_erro = adjetivos_singular_erro
      self.adjetivos_plural = adjetivos_plural
      self.adjetivos_plural_erro = adjetivos_plural_erro
      self.substantivos_singular = substantivos_singular
      self.substantivos_singular_erro = substantivos_singular_erro
      self.substantivos_plural = substantivos_plural
      self.substantivos_plural_erro = substantivos_plural_erro
      self.verbos_infinitivo = verbos_infinitivo
      self.verbos_infinitivo_erro = verbos_infinitivo_erro
      self.verbos_presente_singular = verbos_presente_singular
      self.verbos_presente_singular_erro = verbos_presente_singular_erro
      self.verbos_presente_plural = verbos_presente_plural
      self.verbos_presente_plural_erro = verbos_presente_plural_erro
      self.verbos_passado_singular = verbos_passado_singular
      self.verbos_passado_singular_erro = verbos_passado_singular_erro
      self.verbos_passado_plural = verbos_passado_plural
      self.verbos_passado_plural_erro = verbos_passado_plural_erro
      self.__lista_chaves = self.adjetivos_singular + self.adjetivos_singular_erro + \
                            self.adjetivos_plural + self.adjetivos_plural_erro + \
                            self.substantivos_singular + self.substantivos_singular_erro + \
                            self.substantivos_plural + self.substantivos_plural_erro + \
                            self.verbos_infinitivo + self.verbos_infinitivo_erro + \
                            self.verbos_presente_singular + self.verbos_presente_singular_erro + \
                            self.verbos_presente_plural + self.verbos_presente_plural_erro + \
                            self.verbos_passado_singular + self.verbos_passado_singular_erro + \
                            self.verbos_passado_plural + self.verbos_passado_plural_erro
      self.__lista_normalizacao = lista_normalizacao

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Chave_Busca.__init__')

  @property
  def rotulo(self):
    return self.__rotulo

  @property
  def lista_chaves(self):
    return self.__lista_chaves

  @property
  def lista_normalizacao(self):
    return self.__lista_normalizacao

  @classmethod
  def identificar_chave(cls, rotulo_alvo:str):
    """Método de classe para identificar uma chave de busca dentre as mapeadas no presente módulo.

    :param rotulo_alvo: rótulo correspondente a chave procurada
    :return: a chave de busca localizada
    """
    try:
      globais = globals().copy()
      for chave_busca in globais.values():
        if isinstance(chave_busca, Chave_Busca) and chave_busca.rotulo == rotulo_alvo:
          return chave_busca

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Chave_Busca.identificar_chave')


# CONSTANTES

# gerais
LISTA_GERAL = Chave_Busca(
  rotulo='lista-geral',
  adjetivos_singular=['de merda', 'pobre', 'miserável',
                      'filha da puta', 'favelada', 'pobretona', 'pobrinha',
                      'filho da puta', 'favelado', 'pobretão', 'pobrinho',
                      'ustra', 'tortura', 'torturar', 'torturador', 'torturadora',
                      'fascista', 'nazista', 'comunista', 'socialista'],
  adjetivos_singular_erro=['miseravel', 'pobretao', 'facista', 'nasista'],
  adjetivos_plural=['pobres', 'miseráveis',
                    'filhas da puta', 'faveladas', 'pobretonas', 'pobrinhas',
                    'filhos da puta', 'favelados', 'pobretões', 'pobrinhos',
                    'torturadores', 'torturadoras',
                    'fascistas', 'nazistas', 'comunistas', 'socialistas'],
  adjetivos_plural_erro=['miseraveis', 'pobretoes', 'facistas', 'nasistas'],
  substantivos_singular=['fascismo', 'socialismo', 'comunismo', 'esquerdismo', 'tortura'],
  substantivos_singular_erro=['facismo', 'esquerdizmo']
)

# específicas
ANTIPETISMO = Chave_Busca(
  rotulo='antipetismo',
  adjetivos_singular=['corruptível',
                      'ladra', 'bandida', 'corrupta', 'criminosa',
                      'ladrão', 'bandido', 'corrupto', 'criminoso',
                      'luladrão'],
  adjetivos_singular_erro=['corruptivel', 'ladrao', 'bandido',
                           'corrupito', 'criminoza', 'criminozo', 'luladrao'],
  adjetivos_plural=['corruptíveis',
                    'ladras', 'bandidas', 'corruptas', 'criminosas',
                    'ladrões', 'bandidos', 'corruptos', 'criminosos'],
  adjetivos_plural_erro=['corruptiveis', 'corrupitiveis', 'corrupitas', 'criminozas',
                         'ladroes', 'corrupitos', 'criminozos'],
  substantivos_singular=['roubo', 'crime', 'corrupção', 'roubalheira'],
  substantivos_singular_erro=['corrupçao', 'corrupição', 'corrupiçao',
                              'robalheira', 'roubalhera', 'robalhera'],
  substantivos_plural=['roubos', 'crimes', 'corrupções', 'roubalheiras'],
  substantivos_plural_erro=['corrupçoes','corrupições','corrupiçoes',
                            'robalheiras', 'roubalheras', 'robalheras'],
  verbos_infinitivo=['roubar'],
  verbos_passado_singular=['roubou', 'roubado'],
  verbos_passado_plural=['roubaram', 'roubados']
)

INTOLERANCIA_RELIGIOSA = Chave_Busca(
  rotulo='intolerancia-religiosa',
  adjetivos_singular=['macumbeira' 'macumbeiro'],
  adjetivos_singular_erro=['macumbera' 'macumbero'],
  adjetivos_plural=['macumbeiras', 'macumbeiros'],
  adjetivos_plural_erro=['macumberas', 'macumberos'],
  substantivos_singular=['macumba', 'macumbas']
)

GORDOFOBIA = Chave_Busca(
  rotulo='gordofobia',
  adjetivos_singular=['gorda', 'gordinha', 'gordona', 'balofa',
                      'gordo', 'gordinho', 'gordão', 'balofo',
                      'baleia', 'rolha de poço', 'rolha de poco'],
  adjetivos_singular_erro=['gordao'],
  adjetivos_plural=['gordas', 'gordinhas', 'gordonas', 'balofas',
                    'gordos', 'gordinhos', 'gordões', 'gordoes', 'balofos'],
  adjetivos_plural_erro=['gordoes'],
  substantivos_singular=['gordura']
)

HOMOFOBIA = Chave_Busca(
  rotulo='homofobia',
  adjetivos_singular=['sapatão',
                      'viado', 'viadinho', 'viadinha', 'viadão', 'bicha', 'bichinha',
                      'bichona', 'gayzinho', 'gayzinha', 'boiola', 'boiolinha', 'boiolão',
                      'marica', 'mariquinha', 'afeminado', 'mulherzinha', 'menininha',
                      'traveco', 'travecão', 'travequinho', 'trans', 'travesti'],
  adjetivos_singular_erro=['sapatao', 'bixa', 'bixinha', 'bixona',
                           'boiolao', 'minininha', 'travecao'],
  adjetivos_plural=['sapatões',
                    'viados', 'viadinhos', 'viadinhas', 'viadões', 'viadoes', 'bichas', 'bixas', 'bichinhas', 'bixinhas',
                    'bichonas', 'bixonas', 'gayzinhos', 'gayzinhas', 'boiolas', 'boiolinhas', 'boiolões', 'boioloes',
                    'maricas', 'mariquinhas', 'afeminados', 'mulherzinhas', 'minininhas',
                    'travecos', 'travecões', 'travecoes', 'travequinhos', 'travestis'],
  adjetivos_plural_erro=['sapatoes', 'sapatãos', 'sapataos', 'viadoes', 'bixas', 'bixinhas',
                         'bixonas', 'boioloes', 'minininhas', 'travecoes'],
  substantivos_singular=['viadagem', 'gayzice', 'frescura'],
  substantivos_singular_erro=['viadage', 'viadagi', 'gayzici']
)

MISOGINIA = Chave_Busca(
  rotulo='misoginia',
  adjetivos_singular=['puta', 'putinha', 'prostituta', 'piranha', 'biscate', 'vaca', 'vaquinha', 'pistoleira',
                      'gostosa', 'gostosinha', 'gostosona', 'delícia',
                      'feminista', 'feministinhas', 'feminazi', 'mocréia', 'baranga', 'gorda', 'ridícula',
                      'mulherzinha', 'menininha', 'empregada', 'empregadinha', 'burra',
                      'louca', 'louquinha', 'loucona', 'maluca', 'maluquinha', 'malucona', 'desequilibrada', 'perturbada', 'histérica', 'surtada', 'nervosa', 'nervosinha',
                      'mal comida', 'mal amada'],
  adjetivos_singular_erro=['biscati', 'biskate', 'biskati', 'vaka', 'vakinha', 'pistolera',
                           'gostoza', 'gostozinha', 'gostozona', 'delicia', 'delicinha',
                           'mocreia', 'mininha', 'ridicula',
                           'loca', 'loquinha', 'locona', 'louka', 'loukinha', 'loukona', 'loka', 'lokinha', 'lokona',
                           'maluka', 'malukinha', 'malukona', 'histerica', 'nervoza', 'nervozinha',
                           'mau comida', 'malcomida', 'maucomida', 'mal-comida', 'mau-comida', 'mau amada', 'mal-amada', 'mau-amada'],
  adjetivos_plural=['putas', 'putinhas', 'prostitutas', 'piranhas', 'biscates', 'vacas', 'vaquinhas', 'pistoleiras',
                    'gostosas', 'gostosinhas', 'gostosonas', 'delícias', 'delicinhas',
                    'feministas', 'feministinhas', 'feminazis', 'mocréias', 'barangas', 'gordas', 'ridículas',
                    'mulherzinhas', 'menininhas', 'empregadas', 'empregadinhas', 'burras',
                    'loucas', 'louquinhas', 'louconas', 'malucas', 'maluquinhas', 'maluconas', 'desequilibradas', 'perturbadas', 'histéricas', 'surtadas', 'nervosas', 'nervosinhas',
                    'mal comidas', 'mal amadas'],
  adjetivos_plural_erro=['biscatis', 'biskates', 'biskatis', 'vakas', 'vakinhas', 'pistoleras',
                         'gostozas', 'gostozinhas', 'gostozonas', 'delicias',
                         'mocreias', 'mininhas', 'ridiculas',
                         'locas', 'loquinhas', 'loconas', 'loukas', 'loukinhas', 'loukonas', 'lokas', 'lokinhas', 'lokonas',
                         'malukas', 'malukinhas', 'malukonas', 'histericas', 'nervozas', 'nervozinhas',
                         'mau comidas', 'malcomidas', 'maucomidas', 'mal-comidas', 'mau-comidas', 'mau amadas', 'mal-amadas', 'mau-amadas'],
  substantivos_singular=['feminismo', 'estupro', 'surto', 'boceta', 'tpm'],
  substantivos_singular_erro=['estrupo', 'buceta'],
  substantivos_plural=['estupros', 'surtos', 'bocetas'],
  substantivos_plural_erro=['estrupos', 'bucetas'],
  verbos_infinitivo=['estuprar', 'surtar', 'pirar'],
  verbos_infinitivo_erro=['estrupar'],
  verbos_presente_singular=['estupra', 'surta', 'pira'],
  verbos_presente_singular_erro=['estrupa'],
  verbos_presente_plural=['estupram', 'surtam', 'piram'],
  verbos_presente_plural_erro=['estrupam'],
  verbos_passado_singular=['estuprou', 'surtou', 'pirou'],
  verbos_passado_singular_erro=['estrupou'],
  verbos_passado_plural=['estupraram', 'surtaram', 'piraram'],
  verbos_passado_plural_erro=['estruparam', 'surtaram'],
  lista_normalizacao=[('biscate', ['biscati', 'biskate', 'biskati']), ('biscates', ['biscatis', 'biskates', 'biskatis']),
                      ('vaca', ['vaka'],), ('vacas', ['vakas'],),
                      ('vaquinha', ['vakinha']), ('vaquinhas', ['vakinhas']),
                      ('pistoleira', ['pistolera']), ('pistoleiras', ['pistoleras']),
                      ('gostosa', ['gostoza']), ('gostosas', ['gostozas']),
                      ('gostosinha', ['gostozinha']), ('gostosinhas', ['gostozinhas']),
                      ('gostosona', ['gostozona']), ('gostosonas', ['gostozonas']),
                      ('delícia', ['delicia']), ('delícias', ['delicias']),
                      ('mocréia', ['mocreia']), ('mocréias', ['mocreias']),
                      ('ridícula', ['ridicula']), ('ridículas', ['ridiculas']),
                      ('menininha', ['minininha']), ('menininhas', ['minininhas']),
                      ('louca', ['loca', 'louka', 'loka']), ('loucas', ['locas', 'loukas', 'lokas']),
                      ('louquinha', ['loquinha', 'loukinha', 'lokinha']), ('louquinhas', ['loquinhas', 'loukinhas', 'lokinhas']),
                      ('loucona', ['locona', 'loukona', 'lokona']), ('louconas', ['loconas', 'loukonas', 'lokonas']),
                      ('maluca', ['maluka']), ('malucas', ['malukas']),
                      ('maluquinha', ['malukinha']), ('maluquinhas', ['malukinhas']),
                      ('malucona', ['malukona']), ('maluconas', ['malukonas']),
                      ('histérica', ['histerica']), ('histéricas', ['histericas']),
                      ('nervosa', ['nervoza']), ('nervosas', ['nervozas']),
                      ('nervosinha', ['nervozinha']), ('nervosinhas', ['nervozinhas']),
                      ('mal comida', ['mau comida', 'malcomida', 'maucomida', 'mal-comida', 'mau-comida']), ('mal comidas', ['mau comidas', 'malcomidas', 'maucomidas', 'mal-comidas', 'mau-comidas']),
                      ('mal amada', ['mau amada', 'mal-amada', 'mau-amada']), ('mal amadas', ['mau amadas', 'mal-amadas', 'mau-amadas']),
                      ('estupro', ['estrupo']), ('estupros', ['estrupos']),
                      ('estuprar', ['estrupar']),
                      ('estupra', ['estrupa']), ('estupram', ['estrupam']),
                      ('estuprou', ['estrupou']), ('estupraram', ['estruparam']),
                      ('boceta', ['buceta']), ('bocetas', ['bucetas'])]
)

PEDOFILIA = Chave_Busca(
  rotulo='pedofilia',
  adjetivos_singular=['pedófila', 'pedófilo', 'criança', 'criancinha'],
  adjetivos_singular_erro=['pedofila', 'pedofilo', 'crianca'],
  adjetivos_plural=['pedófilas', 'pedofilas', 'pedófilos', 'pedofilos',
                    'crianças', 'criancas', 'criancinhas'],
  adjetivos_plural_erro=['pedofilas', 'pedofilos', 'criancas'],
  substantivos_singular=['pedofilia']
)

RACISMO = Chave_Busca(
  rotulo='racismo',
  adjetivos_singular=['pixaim', 'cabelo ruim',
                      'preta', 'pretinha', 'crioula', 'escrava', 'escravinha', 'doméstica', 'nega', 'neguinha', 'escura', 'escurinha',
                      'preto', 'pretinho', 'crioulo', 'escravo', 'escravinho', 'doméstico', 'nego', 'neguinho', 'escuro', 'escurinho'],
  adjetivos_singular_erro=['pichaim',
                           'criola', 'domestica',
                           'criolo', 'domestico'],
  adjetivos_plural=['pixains',
                    'pretas', 'pretinhas', 'crioulas', 'criolas', 'escravas', 'escravinhas', 'domésticas', 'negas', 'neguinhas', 'escuras', 'escurinhas',
                    'pretos', 'pretinhos', 'crioulos', 'criolos', 'escravos', 'escravinhos', 'domésticos', 'negos', 'neguinhos', 'escuros', 'escurinhos'],
  adjetivos_plural_erro=['pichains',
                         'criolas', 'domesticas',
                         'criolos', 'domesticos'],
  substantivos_singular=['escravidão'],
  substantivos_singular_erro=['escravidao']
)


__doc__ = """Módulo com as chaves de busca segmentadas em comportamentos, visando direcionar a coleta de dados para um
conjunto_dados."""
