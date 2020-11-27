import tweepy as tw
from maria_bonita.conjunto_dados.utilidades.captura.info_tweet import antevisao_tweets_capturados, tweet, autor, usuario
import maria_bonita.conjunto_dados.utilidades.tratamento_erros as te


# CONSTANTES
CAMINHO_MODULO = 'maria_bonita.conjunto_dados.utilidades.captura.StreamListenerPersonalizado.'


class StreamListenerPersonalizado(tw.StreamListener):
  """Classe que sobrescreve a transmissão de dados do end-point do Twitter."""

  def __init__(self, lista_resultados:list, quantidade_tweets:int, com_retweets:bool):
    """Método construtor.

    :param lista_resultados: estrutura de dados que recebe o resultado de toda captura
    :param quantidade_tweets: limite de tweets a serem capturados
    :param com_retweets: indicador se retweets deverão ser capturados
    """
    tw.StreamListener.__init__(self)
    self.lista_resultados = lista_resultados
    self.quantidade_tweets = quantidade_tweets
    self.com_retweets = com_retweets

  def on_status(self, status):
    """Método que captura as informações de uma publicação e apresenta no console a respectiva antevisão.

    :param status: a própria instância da publicação
    :return: None (nos casos em que o limite de tweets já foi atingido)
    """
    captura = True
    if not self.com_retweets:
      # verifica se é retweet
      captura = not status.text.startswith('RT')
    
    try:
      if captura:
        quantidade_capturados = len(self.lista_resultados) + 1
        atingiu_quantidade_tweets = quantidade_capturados >= self.quantidade_tweets
        if not atingiu_quantidade_tweets:
          
          # cabeçalho
          print(quantidade_capturados, (72 - len(str(quantidade_capturados))) * '-')

          antevisao_tweets_capturados(status)

          dicionario_tweet = {}
          tweet(status, dicionario_tweet)
          autor(status, dicionario_tweet)
          usuario(status, dicionario_tweet)

          self.lista_resultados.append(dicionario_tweet)

          # rodapé
          print(72 * '-', end='\n\n')

      else:
        return
    
    except BaseException as erro:
      te.base_exception(erro, CAMINHO_MODULO + 'on_status')

    except ConnectionError as erro:
      te.connection_error(erro, CAMINHO_MODULO + 'on_status')


__doc__ = """Módulo em que o receptor da trasmissão de tweets foi customizado para atender as necessidades do
Projeto Cangaço."""
