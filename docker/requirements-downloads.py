from nltk import download
from demoji import download_codes
from os import system, remove

download('punkt')
download('stopwords')
download_codes()
system('python -m spacy download pt_core_news_sm')
remove('requirements.txt')
remove('requirements-downloads.py')