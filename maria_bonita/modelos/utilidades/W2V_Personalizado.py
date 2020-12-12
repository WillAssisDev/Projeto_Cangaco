#!python -m spacy download pt_core_news_sm
import pandas as pd
import spacy
from gensim.models import Word2Vec, KeyedVectors
import logging
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle
from utilidades.caminho_projeto import CAMINHO_PROJETO
import utilidades.tratamento_erros as te


# CONSTANTES
_CAMINHO_MODULO = 'maria_bonita.modelos.utilidades.W2V_Personalizado.'
CAMINHO_SAIDA_MODELO = CAMINHO_PROJETO + 'maria_bonita/modelos/'
_NAME_SPACY = 'pt_core_news_sm'
_TAMANHO_VEC = 300
CBOW = 0
SKIPGRAM = 1
INDEFINIDO = -1
_RANDOM_STATE = 13
_MAX_ITER = 800


class Word2VecPersonalizado:
  """Classe para gerar um modelo word to vector, efetuando a configuração dos seus hiperparâmetros e seu treinanamento."""

  def __init__(self, tipo:int, dados:pd.Series, name_spacy:str=_NAME_SPACY, janela:int=2, tamanho_vec:int=_TAMANHO_VEC,
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
      self.__pln = spacy.load(name_spacy,
                              disable=['parser', 'ner', 'tagger', 'textcat'])

      lista_doc = [doc.text for doc in self.__pln.pipe(dados,
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
      self.__treinar()

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Word2VecPersonalizado.__init__')

  @property
  def pln(self):
    return self.__pln

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
      te.base_exception(erro, _CAMINHO_MODULO + 'Word2VecPersonalizado.__construir_vocabulario')

  def __treinar(self):
    """Método privado que treina o modelo com os dados fornecidos, o estruturando com o contexto indicado.
    """
    try:
      if self.log:
        logging.basicConfig(format='%(asctime)s : - %(message)s', level=logging.INFO)

      self.__construir_vocabulario()

      self.__modelo.train(self.__lista_lista_tokens,
                          total_examples=self.__modelo.corpus_count,
                          epochs=30)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Word2VecPersonalizado.__construir_vocabulario')

  def exportar(self, nome_arquivo:str='modelo', caminho_saida:str=CAMINHO_SAIDA_MODELO):
    """Método que consolida o arquivo gerado pelo modelo de word embedding.

    :param nome_arquivo: nome do arquivo de saída
    :param caminho_saida: caminho de saída do arquivo
    """
    try:
      nome_arquivo += '_'
      if self.tipo == CBOW: nome_arquivo += 'cbow'
      elif self.tipo == SKIPGRAM: nome_arquivo += 'skipgram'
      nome_arquivo += '.txt'

      self.__modelo.wv.save_word2vec_format(caminho_saida + nome_arquivo,
                                            binary=False)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'Word2VecPersonalizado.exportar')


class ClassificadorW2V:
  """Classe em que é criado o objeto classificador, capaz de identificar comportamentos criminosos."""

  def __init__(self, textos_base:pd.Series, alvo_base:pd.Series, modelo_txt:str, pln=None,
               perc_treino:float=0.75, perc_teste:float=0.25, random_state_fixo:bool=False,
               mostra_relatorio:bool=False):
    """Método construtor.

    :param textos_base: uma series do Pandas (coluna do DataFrame), que representa o corpus
    :param alvo_base: uma series do Pandas, com a coluna objetivo da classificação
    :param modelo_txt: string com o caminho do modelo Word2Vec gerado, em .txt
    :param pln: o processador de linguagem natural da spaCy
    :param perc_treino: ponto flutuante que indica o percentual do conjunto de dados que será utilizado no treino
    :param perc_teste: ponto flutuante que indica o percentual do conjunto de dados que será utilizado nos testes
    :param random_state_fixo: booleano que indica se será utilizado valor random state fixo na criação do classificador
    :param mostra_relatorio: booleano que indica se deverá ser impresso o relatório de acurácia do classificador
    """
    try:
      if 'cbow' in modelo_txt.lower():
        self.tipo = CBOW
      elif 'skipgram' in modelo_txt.lower():
        self.tipo = SKIPGRAM
      else:
        self.tipo = INDEFINIDO
      self.__modelo_txt = KeyedVectors.load_word2vec_format(modelo_txt)
      self.__pln = pln if pln else spacy.load(_NAME_SPACY,
                                              disable=['parser', 'ner', 'tagger', 'textcat'])
      self.__perc_treino, self.__perc_teste = perc_treino, perc_teste
      random_state = _RANDOM_STATE if random_state_fixo else None
      self.__x_treino, self.__x_teste, \
      self.__y_treino, self.__y_teste = train_test_split(textos_base, alvo_base,
                                                         train_size=perc_treino,
                                                         test_size=perc_teste,
                                                         random_state=random_state)
      self.__matriz_treino, self.__matriz_teste = self.__matriz_vetores()
      self._classificador, self.relatorio = self.__classificador(self.__matriz_treino, self.__matriz_teste,
                                                                 self.__y_treino, self.__y_teste,
                                                                 mostra_relatorio)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'ClassificadorW2V.__init__')

  def __combinacao_vetores_por_soma(self, texto):
    """Função privada que combina os vetores de tokens obtidos do doc do texto, os somando.

    :param texto: o texto da series sendo iterada
    :return: o vetor resultante da combinação
    """
    try:
      tokens = [token.text for token in self.__pln(texto)]

      vetor_resultante = np.zeros((1, _TAMANHO_VEC))
      for token in tokens:
        try:
          vetor_resultante += self.__modelo_txt.get_vector(token)

        except KeyError:
          pass

      return vetor_resultante

    except BaseException as erro:
      print(texto)
      te.base_exception(erro, _CAMINHO_MODULO + 'ClassificadorW2V.__combinacao_vetores_por_soma')

  def __matriz_vetores(self):
    """Função privada que estrutura as matrizes de treino e testes com os respectivos vetores de Word Embedding.

    :return: a matriz de vetores
    """
    try:
      matrizes = []
      for grupo_textos in [self.__x_treino, self.__x_teste]:
        qtd_linhas = len(grupo_textos)
        matriz = np.zeros((qtd_linhas, _TAMANHO_VEC))

        for n in range(qtd_linhas - 1):
          matriz[n] = self.__combinacao_vetores_por_soma(grupo_textos.iloc[n])

        matrizes.append(matriz)

      return matrizes

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'ClassificadorW2V.__matriz_vetores')

  def __classificador(self, x_treino:pd.Series, x_teste:pd.Series, y_treino:pd.Series, y_teste:pd.Series,
                      mostra_relatorio:bool):
    """Função privada que cria o classificador e elabora o relatório da acuária do mesmo.

    :param x_treino: variáveis independentes para treinamento do modelo
    :param y_treino: váriáveis dependentes, objetivas pela previsão, utilizadas no treinamento
    :param x_teste: variáveis independentes para testes do modelo
    :param y_teste: váriáveis dependentes, objetivas pela previsão, utilizadas nos testes
    :param mostra_relatorio: booleano que indica se deverá ser impresso o relatório de acurácia
    :return: o classificador obtido e seu relatório de acurácia
    """
    try:
      regressor_logistico = LogisticRegression(max_iter=_MAX_ITER)
      regressor_logistico.fit(x_treino, y_treino)

      possiveis_crimes = regressor_logistico.predict(x_teste)
      relatorio = classification_report(y_teste, possiveis_crimes)
      if mostra_relatorio:
        print(relatorio)

      return regressor_logistico, relatorio

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'ClassificadorW2V.__classificador')

  def exportar(self, nome_arquivo:str='rl', caminho_saida:str=CAMINHO_SAIDA_MODELO):
    """Método que consolida o modelo obtido em um arquivo Pickle, possibilitando sua utilização em outros contextos.

    :param nome_arquivo: nome do arquivo de saída
    :param caminho_saida: caminho de saída do arquivo
    """
    try:
      nome_arquivo += '_'
      if self.tipo == CBOW: nome_arquivo += 'cbow'
      elif self.tipo == SKIPGRAM: nome_arquivo += 'skipgram'
      nome_arquivo += '.pkl'

      with open(caminho_saida + nome_arquivo, 'wb') as arquivo:
        pickle.dump(self._classificador, arquivo)

    except BaseException as erro:
      te.base_exception(erro, _CAMINHO_MODULO + 'ClassificadorW2V.exportar')


__doc__ = """Módulo com recursos para criação e disponibilização de modelo word embedding, utilizando Word2Vec, e para
criação de modelo de classificação de regressão logística."""
