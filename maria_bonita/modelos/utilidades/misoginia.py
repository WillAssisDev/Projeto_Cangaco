from maria_bonita.conjunto_dados.utilidades.captura.chaves_busca import MISOGINIA
import maria_bonita.modelos.utilidades.StreamMB as sMB
import maria_bonita.modelos.utilidades.StreamListenerSimulado as slp
import utilidades.tratamento_erros as te
from maria_bonita.eu_Maria import MB, MJ, JN


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.modelos.utilidades.misoginia.'
_CHAVES_BUSCA = (MISOGINIA)
_MENCIONADAS = [MB, MJ]
_MISOGINO = JN
_PROJECOES_ADJETIVOS = {
  'singular': ['é', 'que', 'é uma', 'você é uma', 'sua'],
  'plural': ['são', 'que', 'são umas', 'vocês são umas', 'suas']
}

_ARQUIVOS_JSON = ['aj', 'al', 'jv', 'jx', 'md']


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
      dict_frases_projetadas=_PROJECOES_ADJETIVOS
    )

    return lista_tweets

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'projecoes')


__doc__ = """Módulo para criação de uma lista com tweets misóginos."""