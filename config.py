import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://abuga:password@localhost/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgres://xznwkyhozgogtk:a8545b0b6b04f15d30fd66c101cb908477bdfe2bc8ab97f59dffd22dd62f0338@ec2-107-20-15-85.compute-1.amazonaws.com:5432/d5dv71jens3e1p'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}
