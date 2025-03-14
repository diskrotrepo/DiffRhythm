from enum import Enum
from flask_restx import Namespace, Resource, fields
from flask import request
from music_queue.background_thread import BackgroundThreadFactory
from music_queue.extensions import db
from music_shared.models import Music

api = Namespace("status", description="Queue Status related APIs")

queue_status_definition = api.model(
    "Queue Status",
    {
        "title": fields.String(
            required=True,
            description="Title for your song",
            example="Banger #1",
        ),
        "dt_created": fields.DateTime(
            required=False,
            description="The date the song was created",
            example="2025-03-12T00:00:00+05:00",
        ),
        "status": fields.String(
            required=True,
            description="Current status of the song in the queue",
            example="NEW",
        ),
    },
)


@api.route("/<string:id>")
class StatusController(Resource):

    @api.doc(
        description="Returns status of music generation in the queue",
        tags=["Queue Library"],
    )
    @api.response(200, "Success", [queue_status_definition])
    def get(self, id):
        """Retrieve queue status."""
        try:

            # Base query
            query = db.session.query(Music).filter_by(id=id)

            # Fetch results
            song = query.one_or_none()

            if not song:
                return {"error": "No song found"}, 404

            return {
                "status": {
                    "id": song.id,
                    "title": song.title,
                    "dt_created": (
                        song.dt_created.isoformat() if song.dt_created else None
                    ),
                    "filename": song.filename,
                    "processing_status": song.processing_status.value,
                }
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500
