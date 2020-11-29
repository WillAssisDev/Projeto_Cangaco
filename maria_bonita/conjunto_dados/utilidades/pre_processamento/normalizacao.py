import regex as re
import maria_bonita.conjunto_dados.utilidades.tratamento_erros as te
from maria_bonita.conjunto_dados.utilidades.captura.info_tweet import SEP_DEMOJI
import maria_bonita.conjunto_dados.utilidades.captura.chaves_busca as cb


# CONSTANTES
CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.pre_processamento.normalizacao.'


def chaves_busca(tweet_texto:str, chaves_busca:list):
  """Função que identifica no tweet chaves de busca grafadas incorretamente e as normaliza.

  :param tweet_texto: o texto publicado sendo processado
  :param chaves_busca: lista que contém os objetos das chaves de busca e respectivos rótulos
  :return:
  """
  try:
    for chave in chaves_busca:
      if not isinstance(chave, cb.Chave_Busca): chave = cb.Chave_Busca.identificar_chave(chave)

      for chave_normal, lista_a_normalizar in chave.lista_normalizacao:
        for item_a_normalizar in lista_a_normalizar:
          if item_a_normalizar in tweet_texto: tweet_texto = tweet_texto.replace(item_a_normalizar, chave_normal)

    return tweet_texto

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'chaves_busca')


def emoji(tweet_texto:str, sep:str=SEP_DEMOJI):
  """Função que reconhece e normaliza emojis processados pela biblioteca demoji.

  :param tweet_texto: o texto publicado sendo processado
  :param sep: deve ser o mesmo separador de emojis utilizado na captura dos tweets
  :return: o tweet com da remoção do SEP e capitalização
  """
  try:
    if SEP_DEMOJI in tweet_texto:
      regex_sep = r'[' + sep + r']{1}[\w\s\-]+[' + sep + r']{1}'
      regex2_espacos = r'[' + sep + r']{1,}'

      for i in re.finditer(regex_sep, tweet_texto):
        emoji = i.group().upper()
        inicio = i.span()[0]
        fim = i.span()[1]

        tweet_texto = tweet_texto.replace(tweet_texto[inicio:fim], emoji)

      return re.sub(regex2_espacos, ' ', tweet_texto)
    return tweet_texto

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'emoji')


def internetes(tweet_texto:str):
  """Função que reconhece expressões do internetes e as normaliza.

  :param tweet_texto: o texto publicado sendo processado
  :return: o tweet com expressões do internetes normalizadas
  """
  try:
    lista_internetes = [
      ('a propósito', ['btw']), ('abraço', ['abs']), ('adicionar', ['add']), ('amigo', ['amg', 'amgo']),
      ('amiga', ['amga']), ('amigos', ['amgs', 'amgos']), ('amigas', ['amgas']), ('amor', ['amr']),
      ('babaca', ['bbq', 'bbk']), ('melhores amigos pra sempre', ['bff']), ('beijo', ['bjs', 'btk', 'bejo']),
      ('beijos', ['bjss', 'bjsss', 'bjssss', 'bjsssss', 'btks']), ('beijou', ['bjou', 'bejou']),
      ('beijar', ['bjar', 'bejar']), ('volto já', ['brb']), ('brinca', ['brink']), ('brincadeira', ['brinks']),
      ('boto fé', ['btf']), ('comigo', ['cmg']), ('contigo', ['ctg']), ('certeza', ['ctz']), ('legal', ['cool']),
      ('delícia', ['dlç']), ('delícias', ['dlçs']), ('mensagem particular', ['dm']), ('de nada', ['dnd']),
      ('de novo', ['dnv']), ('vitória épica', ['epicwin']), ('falhou', ['fail']), ('falso', ['fake']),
      ('fica a dica', ['fikdik']), ('rumo à vitória', ['ftw']), ('felicidade extrema', ['fuckyeah']),
      ('gente', ['gnt']), ('galera', ['glr']), ('vá embora', ['gtfo']), ('tenho que ir', ['gtg']),
      ('odiador', ['hater']), ('odiadores', ['haters']), ('imagem', ['img', 'pic']),
      ('na minha modesta opinião', ['imho']), ('publicação atrasada', ['lategram']), ('rindo alto', ['lol']),
      ('meu deus', ['mds']), ('mulher', ['mlr']), ('mentira', ['mntr']), ('mensagem', ['msg']),
      ('mesmo', ['msm', 'msmo']), ('mesma', ['msma']), ('muito', ['mto', 'mt']), ('muita', ['mta']),
      ('nada', ['nd', 'nda']), ('nada a ver', ['ndv']), ('nunca', ['never']), ('ninguém', ['ngm']),
      ('sem filtro', ['nofilter']), ('novato', ['noob']), ('não abra no trabalho', ['nsfw']), ('obrigado', ['obg']),
      ('look do dia', ['ootd']), ('sério', ['orly']), ('por favor', ['pfv']), ('pelo amor de deus', ['plmdds']),
      ('porque', ['pq']), ('papo reto', ['pprt']), ('quando', ['qdo']), ('quanto', ['qnt']), ('qualquer', ['qqr']),
      ('querido', ['qrdo']), ('querida', ['qrda']), ('quero', ['qro']), ('repost', ['regram']),
      ('descanse em paz', ['rip']), ('saudades', ['saudade', 'sdd', 'sdds']), ('segue de volta', ['sdv']),
      ('só li verdades', ['slv']), ('você é louco', ['slc']), ('só que não', ['sqn']), ('cale a boca', ['stfu']),
      ('também', ['tb', 'tbm']), ('quinta da nostalgia', ['tbt']), ('teclar', ['tc']),
      ('graças a deus é sexta-feira', ['tgif']), ('linha do tempo', ['tl']), ('você', ['cê', 'ce', 'vc']),
      ('vocês', ['cês', 'ces', 'cêis', 'ceis', 'vcs']), ('verdade', ['vd', 'vdd']), ('vontade', ['vntd']),
      ('vai se foder', ['vsf']), ('vai tomar no cu', ['vtnc']), ('que diabos', ['wtf']), ('beijos e abraços', ['xoxo']),
      ('você só vive uma vez', ['yolo']), ('whats app', ['zap', 'zapzap'])
    ]

    for substituto, expressoes in lista_internetes:
      for expressao in expressoes:
        regex = r'(?<=\s|^)' + expressao
        tweet_texto = re.sub(regex, ' ' + substituto + ' ', tweet_texto)

    return tweet_texto

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'risadas')


def usuarios_mencionados(tokens:str, mencionados:list, resultado=' MENÇÃO '):
  """Função que reconhece e normaliza os usuários mencionados em um tweet.

  :param tokens: lista de fatias processadas de um conjunto de caracteres
  :param mencionados: lista com screen_names de usuários mencionados no tweet
  :param resultado: tweet resultante da substituição dos usuários mencionados pelo valor de RESULTADO
  :return:
  """
  try:
    lista_tokens = []
    for token in tokens:
      lista_tokens.append(token) if token not in mencionados else lista_tokens.append(resultado)
    return lista_tokens

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'usuarios_mencionados')


def numeros(token:str):
  """Função que reconhece e normaliza números.

  :param token: fatia processada de um conjunto de caracteres
  :return: token resultante do arredondamento para inteiro e da substituição de números por '0'
  """
  try:
    token = token.replace(',', '.')
    try:
      return '0' * len(str(int(float(token))))
    except:
      return token

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'numeros')


def risadas(tweet_texto:str, substituto=' RISADA '):
  """Função que identifica no tweet diferentes risadas e as normaliza.

  :param tweet_texto: o texto publicado sendo processado
  :return: o tweet com as risadas normalizadas
  """
  try:
    lista_regex = [r'(?<=\s|^)rs[rs]{1,}', r'(?<=\s|^)ha[ha]{2,}', r'(?<=\s|^)he[he]{2,}', r'(?<=\s|^)hi[hi]{2,}',
                   r'(?<=\s|^)kk[k]*', r'(?<=\s|^)[hua]{3}[hua]{2,}', r'(?<=\s|^)[hue]{3}[hue]{2,}',
                   r'(?<=\s|^)[huae]{3,4}[huae]{2,}']

    for regex in lista_regex:
      tweet_texto = re.sub(regex, substituto, tweet_texto)

    return tweet_texto

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'risadas')


def simbolos_com_alfanumericos(tweet_texto:str):
  """Função que identifica no tweet símbolos representado com caracteres alfanuméricos e os converte em linguagem natural.

  :param tweet_texto: o texto publicado sendo processado
  :return: o tweet com os símbolos traduzidos em linguagem natural
  """
  try:
    lista_simbolos = [
      (' formato de coração ', ['s2'])
    ]

    for substituto, simbolos in lista_simbolos:
      for simbolo in simbolos:
        regex = simbolo
        tweet_texto = re.sub(regex, substituto, tweet_texto)

    return tweet_texto

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'simbolos_com_alfanumericos')


def vogais_soltas(tweet_texto:str):
  """Função que identifica no tweet expressões vogais "soltas" do internetês e as normaliza.

  :param tweet_texto: o texto publicado sendo processado
  :return: o tweet com as vogais soltas normalizadas
  """
  try:
    vogais = ['a', 'e', 'i', 'o', 'u']

    for vogal in vogais:
      regex = r'(?<=\s|^)' + vogal + '[' + vogal + 'h]{1,}'
      tweet_texto = re.sub(regex, ' ' + vogal + ' ', tweet_texto)

    return tweet_texto

  except BaseException as erro:
    te.base_exception(erro, CAMINHO_MODULO + 'vogais_soltas')


__doc__ = """Módulo com recursos para efetuar normalizar o corpus textual e otimizar a precisão do modelo."""
