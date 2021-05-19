import mariadb
import sys
import utilidades.tratamento_erros as te
from pandas import isna


# CONSTANTES
_CAMINHO_MODULO = "utilidades.conexao_mariadb."


def __cursor():
  """Função privada que efetivamente cria o cursor.

  :return: o cursor criado
  """
  try:
    conexao = mariadb.connect(
      user="root",
      password="",
      host="mariadb",
      port=3306,
      database="projeto_cangaco",
      autocommit=True
    )

    return conexao.cursor()

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + '__Conexao.__criar_cursor')
    sys.exit(1)


def __monta_clausulas(comando, clausulas):
  """

  :param comando:
  :param clausulas:
  :return:
  """
  if clausulas and len(clausulas):
    clausulas_comando = ''
    for clausula in clausulas:
      if not len(clausulas_comando):
        clausulas_comando += f"\nWHERE {clausula}"
      else:
        clausulas_comando += f"   AND {clausula}"
      clausulas_comando += '\n'
    comando += clausulas_comando

  return comando


def consulta(tabela:str, colunas:tuple='*', clausulas:tuple=None, cursor=__cursor()):
  """

  :param tabela:
  :param colunas:
  :param clausulas:
  :param cursor:
  :return:
  """
  comando = f"SELECT {colunas}\n" + \
            f"  FROM {tabela}"

  comando = __monta_clausulas(comando, clausulas)
  cursor.execute(comando)
  resultado = cursor.fetchall()
  cursor.close()

  return resultado


def insere(tabela:str, colunas:tuple, valores:list, cursor=__cursor()):
  """

  :param tabela:
  :param colunas:
  :param valores:
  :param cursor:
  :return:
  """
  colunas = "(" + ", ".join(colunas) + ")"

  for n in range(len(valores)):
    if isinstance(valores[n], str):
      valores[n] = "'" + (valores[n].replace("'", r"\'")) + "'"
    elif isinstance(valores[n], int):
      valores[n] = "'" + str(valores[n]) + "'"
    elif not isna(valores[n]):
      valores[n] = str(valores[n])
    else:
      valores[n] = "''"
  valores = "(" + ", ".join(valores) + ")"

  comando = f"INSERT INTO {tabela}\n" + \
            f"  {colunas}\n" + \
            f"VALUES\n" + \
            f"  {valores}\n"

  cursor.execute(comando)
  cursor.close()


def atualiza(tabela:str, colunas:tuple, valores:tuple, clausulas:tuple=None, cursor=__cursor()):
  """

  :param tabela:
  :param colunas:
  :param valores:
  :param cursor:
  :return:
  """
  comando = f"UPDATE {tabela} SET"

  for n in range(len(colunas)):
    comando += f"\n{colunas[n]} = {valores[n]}"

  comando = __monta_clausulas(comando, clausulas)
  cursor.execute(comando)
  cursor.close()


def remove(tabela:str, clausulas:tuple=None, sem_clausula:bool=False, cursor=__cursor()):
  """

  :param tabela:
  :param clausulas:
  :param cursor:
  :return:
  """
  ok = True
  if sem_clausula and (not clausulas or not len(clausulas)):
    ok = False

  comando = f"DELETE FROM {tabela}"
  comando = __monta_clausulas(comando, clausulas)
  if ok: cursor.execute(comando)
  cursor.close()

__doc__ = """"""