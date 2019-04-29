# Example Configuration File

AMIV_API_URL = 'https://api-dev.amiv.ethz.ch'
AMIV_API_KEY = 'replace me'
AMIV_API_PRIVILEGED_GROUPS = ['<group-id-1>', '<group-id-2>']
AMIV_API_TRUSTED_GROUPS = ['<group-id-3>', '<group-id-4>']
# No restrictions (Unendlich-Legi)
AMIV_API_UNRESTRICTED_GROUPS = ['<group-id-5>']

OAUTH_CLIENT_ID = 'Local Tool'
OAUTH_OWN_URL = 'http://localhost:5000'

DEBUG = False 
TESTING = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@<host>/<db-name>'
SECRET_KEY = 'replace me (24 random bytes)'
