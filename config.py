import os

class Config(object):
	SECRET_KEY= os.environ.get('APP_SECRET_KEY')
	GPT_API_KEY= os.environ.get('GPT_API_KEY')

class DevelopmentConfig(Config):
	SECRET_KEY = 'supersecurepw'

class ProductionConfig(Config):
	SECRET_KEY= os.environ.get('APP_SECRET_KEY')
