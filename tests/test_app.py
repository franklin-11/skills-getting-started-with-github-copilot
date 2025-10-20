from fastapi.testclient import TestClient
import importlib


def setup_module(module):
    # Ensure we import the app module freshly
    global app_mod, client
    app_mod = importlib.import_module('src.app')
    client = TestClient(app_mod.app)


def test_get_activities_contains_known_activity():
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # ensure a known activity exists
    assert 'Chess Club' in data


def test_signup_and_remove_participant():
    activity = 'Chess Club'
    email = 'test.user@example.com'

    # Ensure participant not present initially
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert email not in data[activity]['participants']

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    j = resp.json()
    assert 'Signed up' in j['message']

    # Confirm participant present
    resp = client.get('/activities')
    data = resp.json()
    assert email in data[activity]['participants']

    # Remove participant
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    j = resp.json()
    assert 'Removed' in j['message']

    # Confirm participant removed
    resp = client.get('/activities')
    data = resp.json()
    assert email not in data[activity]['participants']
