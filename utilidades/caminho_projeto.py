import os
import utilidades.tratamento_erros as te
from sys import modules

# CONSTANTES
_CAMINHO_MODULO = 'simulacao.caminho_projeto.'


def __caminho_projeto():
  """Função privada em que o caminho absoluto do Projeto Cangaço é estabelecido.

  :return: string do caminho obtido.
  """
  try:
    rodando_google_colab = 'google.colab' in modules

    if rodando_google_colab:
      caminho = '/content/drive/My Drive/workspace/Projetos/projeto_cangaco/'

    else:
      caminho = os.getcwd().replace('\\', r'/')
      fim = caminho.find('projeto_cangaco') + len('projeto_cangaco')
      caminho = caminho[:fim] + '/'

    return caminho

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__caminho_projeto')


CAMINHO_PROJETO = __caminho_projeto()


__doc__ = """Módulo para capturar, dinamicamente, o caminho absoluto do Projeto Cangaço."""
