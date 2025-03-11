import os


class Config:
    DEBUG = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'diskrot.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    CELERY_SEND_SENT_EVENT = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


available_configs = dict(development=DevelopmentConfig, production=ProductionConfig)
selected_config = os.getenv("FLASK_ENV", "production")
config = available_configs.get(selected_config, "production")
