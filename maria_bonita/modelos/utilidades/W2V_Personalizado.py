#!python -m spacy download pt_core_news_sm
import pandas as pd
import spacy
from gensim.models import Word2Vec
import logging
from utilidades.caminho_projeto import CAMINHO_PROJETO
import utilidades.tratamento_erros as te


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.modelos.utilidades.w2v_treinamento.'
_CAMINHO_SAIDA_MODELO = CAMINHO_PROJETO + 'maria_bonita/modelos/'
CBOW = 0
SKIPGRAM = 1


class Word2VecPersonalizado:
  """Classe para gerar um modelo word to vector, efetuando a configuração dos seus hiperparâmetros e seu treinanamento."""

  def __init__(self, tipo:int, dados:pd.Series, name_spacy:str='pt_core_news_sm', janela:int=2, tamanho_vec:int=300,
               freq_min:int=5, alpha:float=0.03, min_alpha:float=0.007, log:bool=False):
    """Método construtor.

    :param tipo: tipo de contexto do modelo
    :param dados: os dados JÁ TRATADOS, que vão formar o modelo
    :param name_spacy: indicador para spacy carregar: tokenizer, tagger, parser, NER e vetores de palavras
    :param janela: quantidade de palavras a serem consideradas para o contexto do modelo
    :param tamanho_vec: tamanho do vetor resultante word2vec
    :param freq_min: frequência mínima para palavra entrar no vetor word2vec
    :param alpha: taxa de aprendizagem em intervalos de decaimento
    :param min_alpha: redução da taxa de aprendizagem a cada iteração
    :param log: indicador se será impresso log
    """
    try:
      nlp = spacy.load(name_spacy)
      lista_doc = [doc.text for doc in nlp.pipe(dados,
                                                batch_size=1000,
                                                n_process=1)]
      conjunto_tweets = pd.DataFrame({"tweet_texto": lista_doc}).dropna().drop_duplicates()

      self.log = log
      self.tipo = tipo
      self.__lista_lista_tokens = [tweet.split(" ") for tweet in conjunto_tweets.tweet_texto]
      self.__modelo = Word2Vec(sg=tipo,
                               window=janela,
                               size=tamanho_vec,
                               min_count=freq_min,
                               alpha=alpha,
                               min_alpha=min_alpha)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Modelo.__init__')

  @property
  def lista_lista_tokens(self):
    return self.__lista_lista_tokens

  @property
  def modelo(self):
    return self.__modelo

  def __construir_vocabulario(self):
    """Método privado que constrói o vocabulário internamente no objeto Word2Vec, no atributo modelo.
    """
    try:
      if self.log:
        self.__modelo.build_vocab(self.__lista_lista_tokens,
                                      progress_per=5000)
      else:
        self.__modelo.build_vocab(self.__lista_lista_tokens)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Modelo.__construir_vocabulario')

  def treinar(self):
    """Método que treina o modelo com os dados fornecidos, o estruturando com o contexto indicado.
    """
    try:
      if self.log:
        logging.basicConfig(format='%(asctime)s : - %(message)s', level=logging.INFO)

      self.__construir_vocabulario()

      self.__modelo.train(self.__lista_lista_tokens,
                          total_examples=self.__modelo.corpus_count,
                          epochs=30)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Modelo.__construir_vocabulario')

  def salvar(self, nome_arquivo:str='modelo', caminho_saida:str=_CAMINHO_SAIDA_MODELO):
    """Método que consolida o arquivo gerado pelo modelo de word embedding.

    :param nome_arquivo: nome do arquivo de saída
    :param caminho_saida: caminho de saída do arquivo
    """
    try:
      if self.tipo == CBOW: nome_arquivo += '_cbow.txt'
      elif self.tipo == SKIPGRAM: nome_arquivo += '_skipgram.txt'

      self.__modelo.wv.save_word2vec_format(caminho_saida + nome_arquivo,
                                            binary=False)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Modelo.salvar')


__doc__ = """Módulo com recursos para criação e disponibilização de modelo word embedding utilizando Word2Vec."""
