from datetime import datetime

def base_exception(erro:BaseException, rotina:str, dicionario_tweet:dict = None):
  """Método para gerenciamento de erros básicos.

  :param erro: erro interceptado
  :param rotina: caminho indicando a rotina em que o erro emergiu
  """
  print('Rotina:', rotina)
  print('Erro:', str(erro))
  if dicionario_tweet:
    with open('saida/log_de_erros.txt', 'a') as log:
      log.write(f"\n\n{datetime.now().strftime('%H:%M:%S')}: {dicionario_tweet}")
      log.write(dicionario_tweet)
      log.write("-------------------------\n\n")


def connection_error(erro:ConnectionError, rotina:str):
  """Método para gerenciamento de erros de conexão.

  :param erro: erro interceptado
  :param rotina: caminho indicando a rotina em que o erro emergiu
  """
  print('Rotina:', rotina)
  print('Erro:', str(erro))


__doc__ = """Módulo com recursos para impedir a emersão de erros, mas que são mostrados no console, sem interromper a
execução das aplicações."""
