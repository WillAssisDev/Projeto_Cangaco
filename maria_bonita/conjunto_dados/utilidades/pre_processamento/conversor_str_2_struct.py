import utilidades.tratamento_erros as te

# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.pre_processamento.conversor_str_2_struct.'


def converter_str_em_list_dict(string:str):
  """Função que converte uma string em uma lista de dicionários.

  :param string: lista de dicionários convertida em string no momento da exportação
  :return: a lista de dicionários originalmente estruturada
  """
  try:
    lista = []
    if string != '[]':
      dicionario = {}
      for item in string.strip("][}{").replace("'", "").split(", "):
        item = item.replace("}", "").replace("{", "")
        dicionario[item[:item.find(':')]] = item[item.find(':') + 2:]
      lista.append(dicionario)
    return lista

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__converter_str_em_list_dict')


def converter_str_em_dict(string:str):
  """Função que converte uma string em dicionário.

  :param string: dicionário convertido em string no momento da exportação
  :return: o dicionário originalmente estruturado
  """
  try:
    dicionario = {}
    if string != '{}':
      dicionario = {}
      for item in string.strip("}{").replace("'", "").split(", "):
        dicionario[item[:item.find(':')]] = item[item.find(':') + 2:]
    return dicionario

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__converter_str_em_dict')


__doc__ = """Módulo com recursos para conversão de strings nas estruturas de dados originais do conjunto_dados, antes da
exportação."""
