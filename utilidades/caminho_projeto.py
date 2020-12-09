import os
import utilidades.tratamento_erros as te


# CONSTANTES
_CAMINHO_MODULO = 'utilidades.caminho_projeto.'


def __caminho_projeto():
  """Função privada em que o caminho absoluto do Projeto Cangaço é estabelecido.

  :return: string do caminho obtido.
  """
  try:
    caminho = os.getcwd().replace('\\', r'/')
    fim = caminho.find('projeto_cangaco') + len('projeto_cangaco')
    return caminho[:fim] + '/'

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'caminho_projeto')


CAMINHO_PROJETO = __caminho_projeto()


__doc__ = """Módulo para capturar, dinamicamente, o caminho absoluto do Projeto Cangaço."""
