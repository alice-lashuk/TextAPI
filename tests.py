from fastapi.testclient import TestClient

from main import app
import json
import pytest


def test_insert():
	with TestClient(app) as client:
		data = {"content":"some text"}
		response = client.post(f"/texts", data=json.dumps(data), headers={"Content-Type": "application/json"})
		new_id = response.json()['id']
		assert response.status_code == 201
		assert response.json()['Content'] == "some text"

def test_get():
	with TestClient(app) as client:
		response = client.get(f"/texts/7")
		failed_response = client.get(f"/texts/78987")
		assert response.status_code == 200
		assert response.json()['Content'] == "some text"
		assert failed_response.status_code == 404

def test_update():
	with TestClient(app) as client:
		data = {"content": "some new text"}
		response = client.put("/texts/8", data=json.dumps(data), headers={"Content-Type": "application/json"})
		assert response.status_code == 200
		assert response.json()['New content'] == "some new text"

		response = client.get(f"/texts/8")
		assert response.status_code == 200
		assert response.json() == {"Content": "some new text", "Views": 0}

def test_delete():
	with TestClient(app) as client:
		data = {"content": "to delete"}
		response = client.post(f"/texts", data=json.dumps(data), headers={"Content-Type": "application/json"})
		new_id = response.json()['id']
		get_inserted = client.get(f"/texts/{new_id}")
		assert response.status_code == 201
		assert response.json()['Content'] == "to delete"

		delete_response = client.delete(f"/texts/{new_id}")
		get_deleted_response = client.get(f"/texts/{new_id}")
		assert get_deleted_response.status_code == 404
