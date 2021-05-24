from fastapi.testclient import TestClient
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from main import app
from main import delete_from_db, delete_text_by_id
import json
import pytest

def test_register():
	with TestClient(app) as client:
		headers = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		headers2 = {'Authorization': 'Basic YWxpY2U3OnBhc3M='}
		failed_response = client.post(f"/register", headers = headers)
		success_response = client.post(f"/register", headers = headers2)
		assert failed_response.status_code == 409
		assert success_response.status_code == 201
		delete_from_db("alice7")

def test_login():
	with TestClient(app) as client:
		headers = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		headers2 = {'Authorization': 'Basic YWxpY2U3OnBhc3M='}
		success_response = client.post(f"/login", headers = headers)
		failed_response = client.post(f"/login", headers = headers2)
		assert success_response.status_code == 201
		assert failed_response.status_code == 401
		
		
def test_logout():
	with TestClient(app) as client:
		headers = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		success_response = client.post(f"/login", headers = headers)
		cookie_token = success_response.json()['token']
		logout_headers = {'Cookie': f'session_token={cookie_token}'}
		success_logout_response = client.delete("/logout", headers=logout_headers)
		headers2 = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		success_response2 = client.post(f"/login", headers = headers)
		logout_headers2 = {'Cookie': 'session_token=hi'}
		failed_logout_response = client.delete("/logout", headers=logout_headers2)
		assert success_logout_response.json() == "Logged out"
		assert failed_logout_response.status_code == 401


def test_insert():
	with TestClient(app) as client:
		headers = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		success_response = client.post(f"/login", headers = headers)
		cookie_token = success_response.json()['token']
		insert_headers = {'Cookie': f'session_token={cookie_token}', "Content-Type": "application/json"}
		data = {"content":"some text"}
		response = client.post(f"/texts", data=json.dumps(data), headers=insert_headers)
		new_id = response.json()['id']
		assert response.status_code == 201
		assert response.json()['Content'] == "some text"
		delete_text_by_id(new_id)
		logout_headers = {'Cookie': f'session_token={cookie_token}'}
		success_logout_response = client.delete("/logout", headers=logout_headers)


def test_get():
	with TestClient(app) as client:
		headers = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		success_response = client.post(f"/login", headers = headers)
		cookie_token = success_response.json()['token']
		insert_headers = {'Cookie': f'session_token={cookie_token}', "Content-Type": "application/json"}
		data = {"content":"some text"}
		response = client.post(f"/texts", data=json.dumps(data), headers=insert_headers)
		new_id = response.json()['id']
		logout_headers = {'Cookie': f'session_token={cookie_token}'}
		success_logout_response = client.delete("/logout", headers=logout_headers)

		response = client.get(f"/texts/{new_id}")
		failed_response = client.get(f"/texts/78987")
		assert response.status_code == 200
		assert response.json()['Content'] == "some text"
		assert failed_response.status_code == 404
		delete_text_by_id(new_id)

def test_update():
	with TestClient(app) as client:
		headers = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		success_response = client.post(f"/login", headers = headers)
		cookie_token = success_response.json()['token']
		insert_headers = {'Cookie': f'session_token={cookie_token}', "Content-Type": "application/json"}
		data = {"content":"some text"}
		response = client.post(f"/texts", data=json.dumps(data), headers=insert_headers)
		new_id = response.json()['id']
		response = client.get(f"/texts/{new_id}")

		data = {"content": "some new text"}
		response = client.put(f"/texts/{new_id}", data=json.dumps(data), headers=insert_headers)
		assert response.status_code == 200
		assert response.json()['New content'] == "some new text"

		logout_headers = {'Cookie': f'session_token={cookie_token}'}
		success_logout_response = client.delete("/logout", headers=logout_headers)

		response = client.get(f"/texts/{new_id}")
		assert response.status_code == 200
		assert response.json() == {"Content": "some new text", "Views": 0}
		delete_text_by_id(new_id)

def test_delete():
	with TestClient(app) as client:
		headers = {'Authorization': 'Basic YWxpY2U6cGFzcw=='}
		success_response = client.post(f"/login", headers = headers)
		cookie_token = success_response.json()['token']
		insert_headers = {'Cookie': f'session_token={cookie_token}', "Content-Type": "application/json"}
		data = {"content": "to delete"}
		response = client.post(f"/texts", data=json.dumps(data), headers={"Content-Type": "application/json"})
		new_id = response.json()['id']
		get_inserted = client.get(f"/texts/{new_id}")
		assert response.status_code == 201
		assert response.json()['Content'] == "to delete"

		delete_response = client.delete(f"/texts/{new_id}")
		logout_headers = {'Cookie': f'session_token={cookie_token}'}
		success_logout_response = client.delete("/logout", headers=logout_headers)
		get_deleted_response = client.get(f"/texts/{new_id}")
		assert get_deleted_response.status_code == 404
