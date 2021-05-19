import tweepy as tw
import utilidades.tratamento_erros as te
import maria_bonita.conjunto_dados.utilidades.captura.atributos_tweet as at
from maria_bonita.conjunto_dados.utilidades.captura.ferramentas_conjunto_dados import filtro_chaves_busca


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.conjunto_dados.simulacao.captura.StreamListenerPersonalizado.'


def antevisao_tweets_capturados(status:tw.Status):
  """Método que imprime no console a antevisão dos tweets sendo capturados pela streaming.

  :param status: apublicação capturada pela streaming
  """
  try:
    print(f'Usuário: {status.user.screen_name}')
    print(f'Texto: {status.text}')

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'antevisao_tweets_capturados')


def consolidar_dados(**kwargs):
  """Função que recebe argumentos dinãmicos, para estruturação das informações de um tweet.

  :param kwargs: argumentos correspondentes as informações que serão usadas para criar o dicionário do tweet
  :return: dicionário em que as inforções do tweet foram estruturadas, para posterior armazenamento
  """
  dicionario_tweet = {}

  try:
    # TWEET
    dicionario_tweet["criado_em"] = kwargs['criado_em']
    dicionario_tweet["retweet"] = kwargs['retweet']
    dicionario_tweet["tweet_id"] = kwargs['tweet_id']
    dicionario_tweet['tweet_url'] = kwargs['tweet_url']
    dicionario_tweet["tweet_texto"] = kwargs['tweet_texto']
    dicionario_tweet["tweet_hashtags"] = kwargs['tweet_hashtags']
    dicionario_tweet["tweet_urls_externos"] = kwargs["tweet_urls_externos"]
    dicionario_tweet["tweet_usuarios_mencionados"] = kwargs["tweet_usuarios_mencionados"]
    dicionario_tweet["tweet_plataforma_origem"] = kwargs["tweet_plataforma_origem"]
    dicionario_tweet["tweet_em_resposta"] = kwargs["tweet_em_resposta"]
    dicionario_tweet["tweet_idioma"] = kwargs["tweet_idioma"]
    dicionario_tweet["tweet_json"] = kwargs["tweet_json"]

    # AUTOR
    dicionario_tweet["autor_nome"] = kwargs["autor_nome"]
    dicionario_tweet["autor_screen_name"] = kwargs["autor_screen_name"]
    dicionario_tweet["autor_id"] = kwargs["autor_id"]
    dicionario_tweet["autor_url"] = kwargs["autor_url"]
    dicionario_tweet["autor_verificado"] = kwargs["autor_verificado"]
    dicionario_tweet["autor_localizacao"] = kwargs["autor_localizacao"]
    dicionario_tweet["autor_descricao"] = kwargs["autor_descricao"]
    dicionario_tweet["autor_qtd_seguidores"] = kwargs["autor_qtd_seguidores"]
    dicionario_tweet["autor_qtd_amigos"] = kwargs["autor_qtd_amigos"]
    dicionario_tweet["autor_qtd_tweets"] = kwargs["autor_qtd_tweets"]
    dicionario_tweet["autor_url_imagem_perfil"] = kwargs["autor_url_imagem_perfil"]
    dicionario_tweet["autor_url_imagem_capa"] = kwargs["autor_url_imagem_capa"]
    dicionario_tweet["autor_criado_em"] = kwargs["autor_criado_em"]
    dicionario_tweet["autor_json"] = kwargs["autor_json"]

    # USUÁRIO
    dicionario_tweet["usuario_nome"] = kwargs["usuario_nome"]
    dicionario_tweet["usuario_screen_name"] = kwargs["usuario_screen_name"]
    dicionario_tweet["usuario_id"] = kwargs["usuario_id"]
    dicionario_tweet["usuario_url"] = kwargs["usuario_url"]
    dicionario_tweet["usuario_verificado"] = kwargs["usuario_verificado"]
    dicionario_tweet["usuario_localizacao"] = kwargs["usuario_localizacao"]
    dicionario_tweet["usuario_descricao"] = kwargs["usuario_descricao"]
    dicionario_tweet["usuario_qtd_seguidores"] = kwargs["usuario_qtd_seguidores"]
    dicionario_tweet["usuario_qtd_amigos"] = kwargs["usuario_qtd_amigos"]
    dicionario_tweet["usuario_qtd_tweets"] = kwargs["usuario_qtd_tweets"]
    dicionario_tweet["usuario_url_imagem_perfil"] = kwargs["usuario_url_imagem_perfil"]
    dicionario_tweet["usuario_url_imagem_capa"] = kwargs["usuario_url_imagem_capa"]
    dicionario_tweet["usuario_criado_em"] = kwargs["usuario_criado_em"]
    dicionario_tweet["usuario_json"] = kwargs["usuario_json"]

    return dicionario_tweet

  except BaseException as erro:
    te.base_exception(erro, _CAMINHO_MODULO + 'consolidar_dados', dicionario_tweet)


class StreamListenerPersonalizado(tw.StreamListener):
  """Classe que sobrescreve a transmissão de dados do end-point do Twitter."""

  def __init__(self, lista_resultados:list, chaves_busca:list, quantidade_tweets:int, com_retweets:bool):
    """Método construtor.

    :param lista_resultados: estrutura de dados que recebe o resultado de toda captura
    :param chaves_busca: lista com as chaves de busca para filtrar a captura de tweets
    :param quantidade_tweets: limite de tweets a serem capturados
    :param com_retweets: indicador se retweets deverão ser capturados
    """
    try:
      tw.StreamListener.__init__(self)
      self.lista_resultados = lista_resultados
      self.chaves_busca = chaves_busca
      self.quantidade_tweets = quantidade_tweets
      self.com_retweets = com_retweets

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamListenerPersonalizado.__init__')

  def on_status(self, status):
    """ Recebe um status proveniente da streaming, estrutura a informação para consolidação, a preparando para o
    armazenamento.

    :param status: uma publicação capturada na streaming
    :return: dicionário em que as inforções do tweet foram estruturadas
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
          tem_extended_tweet = hasattr(status, "extended_tweet")
          tweet_texto = at.tweet_texto(status, tem_extended_tweet)

          if filtro_chaves_busca(tweet_texto, self.chaves_busca):
            # cabeçalho
            print(quantidade_capturados, (72 - len(str(quantidade_capturados))) * '-')

            antevisao_tweets_capturados(status)

            dicionario_tweet = consolidar_dados(
              # TWEET
              criado_em=status.created_at,
              retweet=status.text.startswith('RT'),
              tweet_id=status.id_str,
              tweet_url=at.tweet_url(status),
              tweet_texto=tweet_texto,
              tweet_hashtags=at.tweet_hashtags(status, tem_extended_tweet),
              tweet_urls_externos=at.tweet_urls_externos(status, tem_extended_tweet),
              tweet_usuarios_mencionados=at.tweet_usuarios_mencionados(status, tem_extended_tweet),
              tweet_plataforma_origem=status.source[12:],
              tweet_em_resposta=at.tweet_em_resposta(status),
              tweet_idioma=status.lang,
              tweet_json=status._json,

              # AUTOR
              autor_nome=at.autor_nome(status),
              autor_screen_name=status.author.screen_name,
              autor_id=status.author.id_str,
              autor_url=at.autor_url(status),
              autor_verificado=status.author.verified,
              autor_localizacao=status.author.location,
              autor_descricao=at.autor_descricao(status),
              autor_qtd_seguidores=status.author.followers_count,
              autor_qtd_amigos=status.author.friends_count,
              autor_qtd_tweets=status.author.statuses_count,
              autor_url_imagem_perfil=at.autor_url_imagem_perfil(status),
              autor_url_imagem_capa=at.autor_url_imagem_capa(status),
              autor_criado_em=status.author.created_at,
              autor_json=status.author._json,

              # USUÁRIO
              usuario_nome=at.usuario_nome(status),
              usuario_screen_name=status.user.screen_name,
              usuario_id=status.user.id_str,
              usuario_url=at.usuario_url(status),
              usuario_verificado=status.user.verified,
              usuario_localizacao=status.user.location,
              usuario_descricao=at.usuario_descricao(status),
              usuario_qtd_seguidores=status.user.followers_count,
              usuario_qtd_amigos=status.user.friends_count,
              usuario_qtd_tweets=status.user.statuses_count,
              usuario_url_imagem_perfil=at.usuario_url_imagem_perfil(status),
              usuario_url_imagem_capa=at.usuario_url_imagem_capa(status),
              usuario_criado_em=status.user.created_at,
              usuario_json=status.user._json
            )

            self.lista_resultados.append(dicionario_tweet)

            # rodapé
            print(72 * '-', end='\n\n')

        else:
          return

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamListenerPersonalizado.on_status')

    except ConnectionError as erro:
      te.connection_error(erro, _CAMINHO_MODULO + 'StreamListenerPersonalizado.on_status')


__doc__ = """Módulo em que o receptor da trasmissão de tweets foi customizado para atender as necessidades do
Projeto Cangaço."""
