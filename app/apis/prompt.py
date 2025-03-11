from flask_restx import Namespace, Resource, fields
from flask import request, jsonify

from app.models import (
    Prompt,
    PromptyCategoryEnum,
)

from app.extensions import db

api = Namespace("prompt", description="Prompt related APIs")

category_values = [e.value for e in PromptyCategoryEnum]

prompt_definition = api.model(
    "Prompt",
    {
        "prompt": fields.String(
            required=True,
            description="Lyrics for your song",
            example="""Take the input, and produce an Simple LRC format file which takes into account time required to sing the previous line. 
            Time tags have the format [mm:ss.xx]lyric , where mm is minutes, ss is seconds, xx is hundredths of a second, 
            and lyric is the lyric to be played at that time. Do not provide any other information. I require just the file.

            Example output:

            [00:12.00]Line 1 lyrics
            [00:17.20]Line 2 lyrics""",
        ),
        "model": fields.String(
            required=True,
            description="Model that should be used by running this system prompt",
            example="llama-3.2-3b-instruct",
        ),
        "category": fields.String(
            required=True,
            description=f"Category of the prompt. Allowed values: {category_values}",
            example="lrc",
            enum=category_values,
        ),
        "is_default": fields.Boolean(
            required=True,
            description=f"Is this the default prompt for the given category",
            example=True,
        ),
    },
)

response = api.model(
    "PromptResponse",
    {
        "id": fields.String(
            description="Unique identifier for the prompt",
            example="b7e6a5d9-5f42-4a8b-9a38-47ef2e2a8df1",
        ),
    },
)


@api.route("/")
class PromptV1(Resource):

    @api.expect(prompt_definition, True)
    @api.response(200, "Success", response)
    def post(self):
        try:
            # Get parameters from the request
            data = request.json or {}

            prompt = data.get("prompt")
            category = data.get("category")
            is_default = data.get("is_default")
            model = data.get("model")

            if category not in [e.value for e in PromptyCategoryEnum]:
                return {"error": "Invalid category"}, 400

            if is_default:
                db.session.query(Prompt).filter_by(category=category).update(
                    {"is_default": False}
                )

            new_prompt = Prompt(
                prompt=prompt,
                category=PromptyCategoryEnum(category),
                is_default=is_default,
                model=model,
            )

            db.session.add(new_prompt)
            db.session.commit()

            return {"id": new_prompt.id}, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @api.response(200, "Success")
    def get(self):
        try:

            return {"id": "ok"}, 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
