import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY= os.environ.get('APP_SECRET_KEY')
	GPT_API_KEY= os.environ.get('GPT_API_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')	
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SESSION_COOKIE_SECURE=True
	SESSION_COOKIE_HTTPONLY=True
	SESSION_COOKIE_SAMESITE='None'
	


class DevelopmentConfig(Config):
	SECRET_KEY = 'supersecurepw'
	CORS_ORIGINS = '*'
	FREE_SEARCH_LIMIT = 50
	STRIPE_KEY = 'sk_test_51QAHVjC28JYJI4X0TS0D8zzYeSOIG3qa8eIatYfTGr5JPb9gueb0O7wrd2MU44LkI3qbGfq8N8BfVfHIggwFJzbD00ZxxN0dQ5'
	STRIPE_WEBHOOK_SECRET = ''
	STRIPE_SUCCESS_URL = 'http://localhost:8100/success?session_id={CHECKOUT_SESSION_ID}'
	STRIPE_CANCEL_URL = 'http://localhost:8100/cancel-checkout-session'
	STRIPE_PRICE_ID = 'price_1QAHmJC28JYJI4X0XsXKmD1l'
	

	

class ProductionConfig(Config):
	CORS_ORIGINS = 'https://www.hedgehog.fyi'
	FREE_SEARCH_LIMIT = 5
	STRIPE_KEY = os.environ.get('STRIPE_KEY')
	STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
	STRIPE_SUCCESS_URL = 'https://www.hedgehog.fyi/success?session_id={CHECKOUT_SESSION_ID}'
	STRIPE_CANCEL_URL = 'https://www.hedgehog.fyi/cancel-checkout-session'
	STRIPE_PRICE_ID = 'price_1Q4pYlFfkjHZI58R7LZkhEft'


