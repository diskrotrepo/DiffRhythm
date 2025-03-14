from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import transformers
import torch
import os
import logging

lrc_pipeline = None
poet_pipeline = None

if os.getenv("LLM_SOURCE") == "huggingface":
    if lrc_pipeline is None:
        lrc_model_id = os.getenv("HF_LRC_MODEL")
        lrc_pipeline = transformers.pipeline(
            "text-generation",
            model=lrc_model_id,
            model_kwargs={"torch_dtype": torch.float32},
            device_map="auto",
        )

    if poet_pipeline is None:
        poet_model_id = os.getenv("HF_POET_MODEL")
        poet_pipeline = transformers.pipeline(
            "text-generation",
            model=poet_model_id,
            model_kwargs={"torch_dtype": torch.float32},
            device_map="auto",
        )
        print(f"Poet Model {poet_model_id} loaded successfully!")



db = SQLAlchemy()
migrate = Migrate()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def register_extensions(app):

    db.init_app(app)
    migrate.init_app(app, db)

    app.logger.info(f"Pipeline source -> {os.getenv("LLM_SOURCE")}")

    from music_shared.models import (
        Music,
        Prompt,
    )
