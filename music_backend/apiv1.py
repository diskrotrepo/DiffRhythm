from flask import Blueprint
from flask_restx import Api

from music_backend.controllers.v1.music import api as music_api
from music_backend.controllers.v1.prompt import api as prompt_api
from music_backend.controllers.v1.library import api as library_api
from music_backend.controllers.v1.status import api as status_api

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    title="diskrot: Music Generation",
    version="1.0",
    description="A local way to explore the latent space of sound",
    doc="/docs/",
)

api.add_namespace(music_api)
api.add_namespace(prompt_api)
api.add_namespace(library_api)
api.add_namespace(status_api)
