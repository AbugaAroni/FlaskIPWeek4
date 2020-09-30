import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://abuga:password@localhost/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://urcjcoifyosqxc:23d82a3e3a5a8347c8923a36906f1585d3549df39a2ebbf2e46c47e073082647@ec2-204-236-228-169.compute-1.amazonaws.com:5432/d38mu29fcqi5f0'

class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}
