import json
from nltk import tokenize
from maria_bonita.conjunto_dados.utilidades.captura.chaves_busca import MISOGINIA
import maria_bonita.modelos.utilidades.StreamMB as sMB
import maria_bonita.modelos.utilidades.StreamJSON as sJSON
import maria_bonita.modelos.utilidades.StreamListenerSimulado as slp
import utilidades.tratamento_erros as te
from maria_bonita.eu_Maria import MB, MJ, JN, ALEATORIO
from utilidades.caminho_projeto import CAMINHO_PROJETO
from maria_bonita.conjunto_dados.utilidades.pre_processamento.normalizacao import vogais_soltas, internetes, risadas


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.modelos.utilidades.misoginia.'
_CHAVES_BUSCA = (MISOGINIA)
_MENCIONADAS = [MB, MJ]
_MISOGINO = JN
_PROJECOES_ADJETIVOS = {
  'singular': ['é', 'que', 'é uma', 'você é uma', 'sua'],
  'plural': ['são', 'que', 'são umas', 'vocês são umas', 'suas']
}

__NOMES_ARQUIVOS_JSON = ['aj', 'al', 'am', 'jv', 'jx', 'me', 'md']
__CAMINHO_ARQUIVOS_JSON = CAMINHO_PROJETO + 'maria_bonita/modelos/dados_simulados/'
_ARQUIVOS_JSON = [__CAMINHO_ARQUIVOS_JSON + nome_arquivo + '_misoginia.json' for nome_arquivo in __NOMES_ARQUIVOS_JSON]
_CHAVES_MENCOES = ['fulana', 'ciclana', 'mencao_aleatoria']


def projecoes(chaves_busca:list=_CHAVES_BUSCA):
  """Função que cria uma lista de tweets com projeções de tweets misóginos.

  :param chaves_busca: lista de objetos chave de busca
  :return: a lista com dicionários de projecoes de tweets misóginos
  """
  try:
    if not len(chaves_busca): chaves_busca = [MISOGINIA]

    lista_tweets = []

    stream_misoginia = sMB.StreamMB(
      listener=slp.StreamListenerSimulado(
        lista_resultados=lista_tweets
      ),
      usuarios_mencionados=_MENCIONADAS,
      autor=_MISOGINO,
      usuario=_MISOGINO
    )

    stream_misoginia.filter_adjetivos(
      chaves_busca=chaves_busca,
      dict_frases_projetadas=_PROJECOES_ADJETIVOS,
      vocabulario=_VOCABULARIO
    )

    stream_misoginia_2 = sJSON.StreamJSON(
      listener=slp.StreamListenerSimulado(
        lista_resultados=lista_tweets
      ),
      usuarios_mencionados=_MENCIONADAS + [ALEATORIO],
      autor=_MISOGINO,
      usuario=_MISOGINO
    )

    stream_misoginia_2.filter_fixos(
      chaves_busca=chaves_busca,
      chaves_mencoes=_CHAVES_MENCOES,
      lista_arquivos_json=_ARQUIVOS_JSON,
      vocabulario=_VOCABULARIO
    )

    return lista_tweets

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'projecoes')


def __vocabulario_misoginia():
  lista_dados_arquivos_json = []
  for arquivo_json in _ARQUIVOS_JSON:
    with open(arquivo_json, 'r', encoding='utf-8') as arquivo:
      lista_dados_arquivos_json.append(json.load(arquivo))

  projecoes = []
  for dados_arquivos_json in lista_dados_arquivos_json:
    dados_singular_plural = dados_arquivos_json['tweets']['singular'] + dados_arquivos_json['tweets']['plural']

    for dado in dados_singular_plural:
      for chave in _CHAVES_MENCOES:
        projecao = vogais_soltas(internetes(risadas(dado['texto'].lower().replace('@' + chave, ''))))

      projecao = [alfanumerico for alfanumerico in tokenize.word_tokenize(projecao, 'portuguese') if alfanumerico.isalpha()]
      projecoes += projecao

  projecoes_adjetivos = []
  for projecao_adjetivo in _PROJECOES_ADJETIVOS['singular'] + _PROJECOES_ADJETIVOS['plural']:
    projecoes_adjetivos += projecao_adjetivo.split()

  return list(set(MISOGINIA.lista_chaves + projecoes_adjetivos + projecoes))


_VOCABULARIO = __vocabulario_misoginia()


__doc__ = """Módulo para criação de uma lista com tweets misóginos."""
