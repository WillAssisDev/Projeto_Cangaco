import utilidades.tratamento_erros as te
from datetime import datetime


_CAMINHO_MODULO = 'simulacao.formatar_data.'


def formatar(data:datetime=datetime.today()):
  """Função para padronizar a formato de datas.

  :param data: a data a ser padronizada. Se None, formata datetime.today()
  :return: string da data formatada
  """
  try:
    if isinstance(data, str): datetime.strptime(data, '%m/%d/%y %H:%M:%S')

    return f'{str(data.day).zfill(2)}/{str(data.month).zfill(2)}/{str(data.year).zfill(2)} ' + \
           f'{str(data.hour).zfill(2)}:{str(data.minute).zfill(2)}:{str(data.second).zfill(2)}'

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'formatar')


__doc__ = """Módulo criado para padronização do formato de datas."""
