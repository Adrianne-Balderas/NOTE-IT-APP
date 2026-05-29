from flask_restx import Namespace, Resource, fields
from flask import request
from flask_login import current_user
from datetime import datetime

from website.models import Notes
from website import db

api = Namespace("notes", description="Notes operations")

# ----------------------
# Swagger Model (Schema)
# ----------------------
note_model = api.model("Note", {
    "note_id": fields.Integer(readOnly=True),
    "title": fields.String(required=True, description="Note title"),
    "body": fields.String(description="Note body"),
    "user_id": fields.Integer(description="Owner user ID")
})

note_input = api.model("NoteInput", {
    "title": fields.String(required=True),
    "body": fields.String()
})

# ----------------------
# /api/notes/
# ----------------------
@api.route("/")
class NoteList(Resource):

    @api.marshal_list_with(note_model)
    def get(self):
        """Get all notes"""
        return Notes.query.all()

    @api.expect(note_input, validate=True)
    @api.response(201, "Note created successfully")
    @api.response(400, "Invalid request")
    def post(self):
        """Create a new note"""

        data = request.get_json()

        # Validation
        if not data:
            return {"error": "Request body is required"}, 400

        if not data.get("title"):
            return {"error": "Title is required"}, 400

        if not data.get("title").strip():
            return {"error": "Title cannot be empty"}, 400

        note = Notes(
            title=data["title"],
            body=data.get("body", ""),
            is_public=0,
            update_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id=current_user.id if current_user.is_authenticated else 1
        )

        db.session.add(note)
        db.session.commit()

        return {
            "message": "Note created successfully",
            "note_id": note.note_id
        }, 201


# ----------------------
# /api/notes/<id>
# ----------------------
@api.route("/<int:id>")
class Note(Resource):

    @api.marshal_with(note_model)
    @api.response(404, "Note not found")
    def get(self, id):
        """Get a note by ID"""

        note = db.session.get(Notes, id)

        if not note:
            return {"error": "Note not found"}, 404

        return note

    @api.expect(note_input, validate=True)
    @api.response(200, "Note updated successfully")
    @api.response(400, "Invalid request")
    @api.response(404, "Note not found")
    def put(self, id):
        """Update a note"""

        note = db.session.get(Notes, id)

        if not note:
            return {"error": "Note not found"}, 404

        data = request.get_json()

        if not data:
            return {"error": "Request body is required"}, 400

        if "title" in data and not data["title"].strip():
            return {"error": "Title cannot be empty"}, 400

        note.title = data.get("title", note.title)
        note.body = data.get("body", note.body)
        note.update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.session.commit()

        return {
            "message": "Note updated successfully"
        }, 200

    @api.response(200, "Deleted successfully")
    @api.response(404, "Note not found")
    def delete(self, id):
        """Delete a note"""

        note = db.session.get(Notes, id)

        if not note:
            return {"error": "Note not found"}, 404

        db.session.delete(note)
        db.session.commit()

        return {
            "message": "Note deleted successfully"
        }, 200