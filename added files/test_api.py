import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from website import create_app, db
from website.models import Notes


# =====================================================
# FIXTURE
# =====================================================
@pytest.fixture
def client():

    app = create_app()

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():

            db.create_all()

            yield client

            db.session.remove()
            db.drop_all()


# =====================================================
# CREATE NOTE
# =====================================================
def test_create_note(client):

    response = client.post('/api/notes/', json={
        'title': 'Test',
        'body': 'Testing'
    })

    assert response.status_code == 201


def test_create_note_no_title(client):

    response = client.post('/api/notes/', json={
        'body': 'Testing'
    })

    assert response.status_code == 400


def test_create_note_no_data(client):

    response = client.post('/api/notes/', json={})

    assert response.status_code == 400


def test_create_note_empty_title(client):

    response = client.post('/api/notes/', json={
        'title': '',
        'body': 'Testing'
    })

    assert response.status_code == 400


# =====================================================
# GET NOTES
# =====================================================
def test_get_notes(client):

    response = client.get('/api/notes/')

    assert response.status_code == 200


# =====================================================
# GET SINGLE NOTE
# =====================================================
def test_get_single_note(client):

    note = Notes(
        title='Sample',
        body='Sample Content',
        is_public=0,
        update_date='2026-05-28',
        user_id=1
    )

    db.session.add(note)
    db.session.commit()

    response = client.get(f'/api/notes/{note.note_id}')

    assert response.status_code == 200


def test_get_single_note_not_found(client):

    response = client.get('/api/notes/999')

    assert response.status_code == 404


# =====================================================
# UPDATE NOTE
# =====================================================
def test_update_note(client):

    note = Notes(
        title='Old',
        body='Old Content',
        is_public=0,
        update_date='2026-05-28',
        user_id=1
    )

    db.session.add(note)
    db.session.commit()

    response = client.put(f'/api/notes/{note.note_id}', json={
        'title': 'New',
        'body': 'New Content'
    })

    assert response.status_code == 200


def test_update_note_not_found(client):

    response = client.put('/api/notes/999', json={
        'title': 'New'
    })

    assert response.status_code == 404


def test_update_note_no_data(client):

    note = Notes(
        title='Old',
        body='Old Content',
        is_public=0,
        update_date='2026-05-28',
        user_id=1
    )

    db.session.add(note)
    db.session.commit()

    response = client.put(f'/api/notes/{note.note_id}', json={})

    assert response.status_code == 400


# =====================================================
# DELETE NOTE
# =====================================================
def test_delete_note(client):

    note = Notes(
        title='Delete',
        body='Delete Content',
        is_public=0,
        update_date='2026-05-28',
        user_id=1
    )

    db.session.add(note)
    db.session.commit()

    response = client.delete(f'/api/notes/{note.note_id}')

    assert response.status_code == 200


def test_delete_note_not_found(client):

    response = client.delete('/api/notes/999')

    assert response.status_code == 404