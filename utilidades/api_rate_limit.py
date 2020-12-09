import tweepy as tw
from utilidades.autenticacao import autenticar


api = tw.API(autenticar())
print(int(api.rate_limit_status()['resources']['application']['/application/rate_limit_status']['remaining']))
print(int(api.rate_limit_status()['resources']['friendships']['/friendships/show']['remaining']))
print(api.me())


__doc__ = """Módulo para rápida visualização da taxa de limite da API."""
