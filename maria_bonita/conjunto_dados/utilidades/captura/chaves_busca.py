class Chave_Busca:
  """Classe para rotular e instanciar chaves de busca, que serão utilizadas na captura de Tweets."""

  def __init__(self, rotulo:str, lista_chaves:list, lista_normalizacao:list):
    """Método construtor.

    :param rotulo: palavra ou expressão que designa o conjunto de chaves de busca
    :param lista_chaves: a lista de chaves de busca
    :param lista_corretor: a lista de tuplas para normalizar erros de digitação nas chaves de busca
    """
    self.__rotulo = rotulo.lower()
    self.__lista_chaves = lista_chaves
    self.__lista_normalizacao = lista_normalizacao

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
    """Método de classe para identificar uma chave de busca dentre as aqui constantes.

    :param rotulo_alvo: rótulo correspondente a chave procurada
    :return: a chave de busca localizada
    """
    globais = globals().copy()
    for chave_busca in globais.values():
      if isinstance(chave_busca, Chave_Busca) and chave_busca.rotulo == rotulo_alvo:
        return chave_busca


# CONSTANTES

# gerais
LISTA_GERAL = Chave_Busca(
  rotulo='lista-geral',
  lista_chaves=['de merda', 'pobre', 'miserável', 'miseravel', 'pobres', 'miseráveis', 'miseraveis',
                'filha da puta', 'favelada', 'pobretona', 'pobrinha', 'filhas da puta', 'faveladas', 'pobretonas', 'pobrinhas',
                'filho da puta', 'favelado', 'pobretão', 'pobretao', 'pobrinho', 'filhos da puta', 'favelados', 'probretões', 'pobretoes', 'pobrinhos',
                'ustra', 'tortura', 'torturar', 'torturador', 'torturadora', 'torturadores', 'torturadoras',
                'fascismo', 'facismo', 'fascista', 'facista', 'nazista', 'comunista', 'socialista', 'fascistas', 'facistas', 'nazistas', 'comunistas', 'socialistas'],
  lista_normalizacao=[]
)

# específicas
ANTIPETISMO = Chave_Busca(
  rotulo='antipetismo',
  lista_chaves=['roubar', 'roubo', 'roubou', 'roubalheira', 'crime', 'corrupção', 'roubaram', 'roubado', 'roubados', 'crimes', 'corruptível', 'corruptivel', 'corruptíveis', 'corruptiveis',
                'ladra', 'bandida', 'corrupta', 'criminosa', 'ladras', 'bandidas', 'corruptas', 'criminosas',
                'ladrão', 'ladrao', 'bandido', 'corrupto', 'criminoso', 'ladrões', 'ladroes', 'bandidos', 'corruptos', 'criminosos',
                'luladrão', 'luladrao'],
  lista_normalizacao=[]
)

INTOLERANCIA_RELIGIOSA = Chave_Busca(
  rotulo='intolerancia-religiosa',
  lista_chaves=['macumba', 'macumbas',
                'macumbeira', 'macumbeiras',
                'macumbeiro', 'macumbeiros'],
  lista_normalizacao=[]
)

GORDOFOBIA = Chave_Busca(
  rotulo='gordofobia',
  lista_chaves=['gordura',
                'gorda', 'gordinha', 'gordona', 'gordas', 'gordinhas', 'gordonas', 'balofa', 'balofas',
                'gordo', 'gordinho', 'gordão', 'gordao', 'gordos', 'gordinhos', 'gordões', 'gordoes', 'balofo', 'balofos',
                'baleia', 'rolha de poço', 'rolha de poco', 'balão', 'peppa'],
  lista_normalizacao=[]
)

HOMOFOBIA = Chave_Busca(
  rotulo='homofobia',
  lista_chaves=['sapatão', 'sapatões',
                'viado', 'viadinho', 'viadinha', 'viadão', 'viadao', 'bicha', 'bixa', 'bichinha', 'bixinha', 'bichona', 'bixona', 'gayzinho', 'gayzinha', 'boiola', 'boiolinha', 'boiolão', 'boiolao', 'marica', 'mariquinha', 'afeminado', 'mulherzinha', 'minininha',
                'viados', 'viadinhos', 'viadinhas', 'viadões', 'viadoes', 'bichas', 'bixas', 'bichinhas', 'bixinhas', 'bichonas', 'bixonas','gayzinhos', 'gayzinhas', 'boiolas', 'boiolinhas', 'boiolões', 'boioloes','maricas', 'mariquinhas', 'afeminados', 'mulherzinhas', 'minininhas',
                'traveco', 'travecão', 'travecao', 'travequinho', 'trans', 'travesti',
                'travecos', 'travecões', 'travecoes', 'travequinhos', 'travestis'],
  lista_normalizacao=[]
)

MISOGINIA = Chave_Busca(
  rotulo='misoginia',
  lista_chaves=['puta', 'putinha', 'prostituta', 'piranha', 'biscate', 'biscati', 'biskate', 'biskati', 'vaca', 'vaka', 'vaquinha', 'vakinha', 'pistoleira', 'pistolera',
                'putas', 'putinhas' 'prostitutas', 'piranhas', 'biscates', 'biscatis', 'biskates', 'biskatis', 'vacas', 'vakas', 'vaquinhas', 'vakinhas', 'pistoleiras', 'pistoleras',
                'gostosa', 'gostoza', 'gostosinha', 'gostozinha', 'gostosona', 'gostozona', 'delícia', 'delicia',
                'gostosas', 'gostozas', 'gostosinha', 'gostozinhas', 'gostosonas', 'gostozonas', 'delícias', 'delicias',
                'feminazi', 'feminazis',
                'mulherzinha', 'menininha', 'empregada', 'empregadinha', 'mulherzinhas', 'menininhas', 'empregadas', 'empregadinhas',
                'louca', 'loca', 'louka', 'loka', 'louquinha', 'lokinha', 'maluca', 'maluka', 'maluquinha', 'malukinha', 'malucona', 'malukona', 'desequilibrada', 'perturbada',
                'loucas', 'locas', 'loukas', 'lokas', 'louquinhas', 'lokinhas', 'malucas', 'malukas', 'maluquinhas', 'malukinhas', 'desequilibradas', 'perturbadas',
                'mal comida', 'mau comida', 'malcomida', 'maucomida', 'mal amada', 'mau amada',
                'mal comidas', 'mau comidas', 'malcomidas', 'maucomidas', 'mal amadas', 'mau amadas'],
  lista_normalizacao=[('biscate', ['biscati', 'biskate', 'biskati']), ('biscates', ['biscatis', 'biskates', 'biskatis']),
                      ('vaca', ['vaka'],), ('vacas', ['vakas'],),
                      ('vaquinha', ['vakinha']), ('vaquinhas', ['vakinhas']),
                      ('pistoleira', ['pistolera']), ('pistoleiras', ['pistoleras']),
                      ('gostosa', ['gostoza']), ('gostosas', ['gostozas']),
                      ('gostosinha', ['gostozinha']), ('gostosinhas', ['gostozinhas']),
                      ('gostosona', ['gostozona']), ('gostosonas', ['gostozonas']),
                      ('delícia', ['delicia']), ('delícias', ['delicias']),
                      ('louca', ['loca', 'louka', 'loka']), ('loucas', ['locas', 'loukas', 'lokas']),
                      ('louquinha', ['loquinha', 'loukinha', 'lokinha']), ('louquinhas', ['loquinhas', 'loukinhas', 'lokinhas']),
                      ('maluca', ['maluka']), ('malucas', ['malukas']),
                      ('maluquinha', ['malukinha']), ('maluquinhas', ['malukinhas']),
                      ('malucona', ['malukona']), ('maluconas', ['malukonas']),
                      ('mal comida', ['mau comida', 'malcomida', 'maucomida']), ('mal comidas', ['mau comidas', 'malcomidas', 'maucomidas']),
                      ('mal amada', ['mau amada']), ('mal amadas', ['mau amadas'])]
)

PEDOFILIA = Chave_Busca(
  rotulo='pedofilia',
  lista_chaves=['pedofilia',
                'pedófila', 'pedofila', 'pedófilas', 'pedofilas',
                'pedófilo', 'pedofilo', 'pedófilos', 'pedofilos',
                'criança', 'crianca', 'criancinha', 'crianças', 'criancas', 'criancinhas'],
  lista_normalizacao=[])

RACISMO = Chave_Busca(
  rotulo='racismo',
  lista_chaves=['escravidão', 'pixaim', 'pichaim', 'cabelo ruim', 'pixains', 'pichains',
                'preta', 'pretinha', 'crioula', 'criola', 'escrava', 'éscravinha', 'doméstica', 'nega', 'neguinha', 'escura', 'escurinha',
                'pretas', 'prtinhas', 'crioulas', 'criolas', 'escravas', 'escravinhas', 'domésticas', 'negas', 'neguinhas', 'escuras', 'escurinhas',
                'preto', 'pretinho', 'crioulo', 'criolo', 'escravo', 'éscravinho', 'doméstico', 'nego', 'neguinho', 'escuro', 'escurinho',
                'pretos', 'pretinhos', 'crioulos', 'criolos', 'escravos', 'escravinhos', 'domésticos', 'negos', 'neguinhos', 'escuros', 'escurinhos'],
  lista_normalizacao=[]
)


__doc__ = """Módulo com as chaves de busca segmentadas em comportamentos, visando direcionar a coleta de dados para um
conjunto_dados"""