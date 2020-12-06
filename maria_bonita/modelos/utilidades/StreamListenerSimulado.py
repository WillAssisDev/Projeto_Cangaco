import utilidades.tratamento_erros as te
import maria_bonita.modelos.utilidades.atributos_simulados as simula
import maria_bonita.conjunto_dados.utilidades.pre_processamento.novas_variaveis as nv
from maria_bonita.modelos.utilidades.StatusSimulado import Status_Simulado
import maria_bonita.conjunto_dados.utilidades.captura.StreamListenerPersonalizado as slp


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.modelos.utilidades.StreamListenerSimulado.'
_COM_STOPWORDS = True
_POSSIVEL_CRIME = 1


class StreamListenerSimulado:
  """Classe criada para simular o receptor de uma transmissão de tweets, também simulada."""

  def __init__(self, lista_resultados):
    """Método construtor.

    :param lista_resultados: a lista na qual os dicionários de projeções de tweets deverão ser armazenados
    """
    try:
      self.lista_resultados = lista_resultados

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamListenerSimulado.__init__')


  def on_status(self, status:Status_Simulado, chaves_busca:list, com_stopwords:bool):
    """Função que estrutura os dados da projeção de um tweet em um dicionário.

    :param status: uma projeção simulada na stream simulada
    :param chaves_busca: lista de objetos chave de busca
    :param com_stopwords: booleano que indica se as stopwords ignorados no processamento (tokenização)
    :return: o dicionário do tweet simulado
    """
    try:
      dicionario_tweet = slp.consolidar_dados(
        criado_em=                  status.created_at,
        retweet=                    status.retweet,
        tweet_id=                   status.id_str,
        tweet_url=                  simula.tweet_url(status.user.screen_name, status.id_str),
        tweet_texto=                status.text,
        tweet_hashtags=             status.entities.hashtags,
        tweet_urls_externos=        status.entities.urls,
        tweet_usuarios_mencionados= simula.tweet_usuarios_mencionados(status.entities.user_mentions),
        tweet_plataforma_origem=    status.source,
        tweet_em_resposta=          status.in_reply_to_status_id_str,
        tweet_idioma=               status.lang,
        tweet_json=                 None,

        # AUTOR
        autor_nome=                 status.author.name,
        autor_screen_name=          status.author.screen_name,
        autor_id=                   status.author.id_str,
        autor_url=                  status.author.profile_url,
        autor_verificado=           status.author.verified,
        autor_localizacao=          status.author.location,
        autor_descricao=            status.author.description,
        autor_qtd_seguidores=       status.author.followers_count,
        autor_qtd_amigos=           status.author.friends_count,
        autor_qtd_tweets=           status.author.statuses_count,
        autor_url_imagem_perfil=    status.author.profile_image_url,
        autor_url_imagem_capa=      status.author.profile_banner_url,
        autor_criado_em=            status.author.created_at,
        autor_json=                 status.author.json,

        # USUÁRIO
        usuario_nome=               status.user.name,
        usuario_screen_name=        status.user.screen_name,
        usuario_id=                 status.user.id_str,
        usuario_url=                status.user.profile_url,
        usuario_verificado=         status.user.verified,
        usuario_localizacao=        status.user.location,
        usuario_descricao=          status.user.description,
        usuario_qtd_seguidores=     status.user.followers_count,
        usuario_qtd_amigos=         status.user.friends_count,
        usuario_qtd_tweets=         status.user.statuses_count,
        usuario_url_imagem_perfil=  status.user.profile_image_url,
        usuario_url_imagem_capa=    status.user.profile_banner_url,
        usuario_criado_em=          status.user.created_at,
        usuario_json=               status.user.json,
      )

      # NOVAS VARIÁVEIS
      nv.novas_variaveis(
        dicionario_tweet=  dicionario_tweet,
        chaves_busca=      chaves_busca,
        possivel_crime=    _POSSIVEL_CRIME,
        com_stopwords=     com_stopwords
      )

      return dicionario_tweet

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'StreamListenerSimulado.on_status')


__doc__ = """Módulo criado para estruturar o dados produzidos na simulação, reproduzindo os mesmos recursos utilizados
em uma captura real."""
