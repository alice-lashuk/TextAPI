# API for inserting, retrieving, editing and deleting small texts

Link to the application deployed on Heroku [link](https://textapi-alicelashuk.herokuapp.com/)
## Run the app

    uvicorn main:app

## Run the tests

    pytest tests.py

## Register

### Request
Uses Basic authentication scheme

Url `http://127.0.0.1:8000/register`

`POST /register`

    curl -X 'POST' 'http://127.0.0.1:8000/register' -H 'accept: application/json' -H 'Authorization: Basic czpkZmhydGV0dWV0eXRy' -d ''

### Response

    Request Method: POST
    Status Code: 201 Created
    content-length: 9 
    content-type: application/json 
    date: Mon,24 May 2021 16:48:06 GMT 
    server: uvicorn 

    "Success"
    
## Register with already existing username
### Request
Uses Basic authentication scheme

Url `http://127.0.0.1:8000/register`


`POST /register`

    curl -X 'POST' 'http://127.0.0.1:8000/register' -H 'accept: application/json' -H 'Authorization: Basic YWxpY2U6cGFzcw==' -d ''

### Response

    Request Method: POST
    Status Code: 409 Conflict
    content-length: 36 
    content-type: application/json 
    date: Mon,24 May 2021 16:42:04 GMT 
    server: uvicorn 

    {"detail": "username already exists"}
    
## Login
### Request
Uses Basic authentication scheme

Url `http://127.0.0.1:8000/login`


`POST /login`

    curl -X 'POST' 'http://127.0.0.1:8000/login' -H 'accept: application/json' -H 'Authorization: Basic YWxpY2U6cGFzcw==' -d ''

### Response

    Request Method: POST
    Status Code: 201 Created
    content-length: 76 
    content-type: application/json 
    date: Mon,24 May 2021 16:58:06 GMT 
    server: uvicorn 

    {"token": "f4c53ffdaed37de8994196e44ab14e92c55ba45f30a396d53fa7d24f8b6a7623"}
    
## Login with bad credentials
### Request
Uses Basic authentication scheme

Url `http://127.0.0.1:8000/login`


`POST /login`

    curl -X 'POST' 'http://127.0.0.1:8000/login' -H 'accept: application/json' -H 'Authorization: Basic YWw6cw==' -d ''

### Response

    Request Method: POST
    Status Code: 401 Unauthorized
    content-length: 30 
    content-type: application/json 
    date: Mon,24 May 2021 17:00:58 GMT 
    server: uvicorn 

    {"detail": "Unathorised login"}
    
## Unautharized log out
### Request

Url `http://127.0.0.1:8000/login`


`POST /logout`

    curl -X 'DELETE' 'http://127.0.0.1:8000/logout' -H 'accept: application/json' -H 'Cookie: session_token=sfdfg'

### Response

    Request Method: DELETE
    Status Code: 401 Unauthorized
    content-length: 31 
    content-type: application/json 
    date: Mon,24 May 2021 17:10:19 GMT 
    server: uvicorn 

    {"detail": "Unathorised logout"}
  
## Log out
### Request

Url `http://127.0.0.1:8000/logout`


`POST /logout`

    curl -X 'DELETE' 'http://127.0.0.1:8000/logout' -H 'accept: application/json' -H 'Cookie: session_token=0d4a7cf1562b3aee789e4a31fd263b32772fd0a4aa3ce00a753bb07e022a58ea'

### Response

    Request Method: DELETE
    Status Code: 200 OK
    content-length: 12 
    content-type: application/json 
    date: Mon,24 May 2021 17:14:05 GMT 
    server: uvicorn 

    "Logged out"

## Get text by id

### Request

Url `http://127.0.0.1:8000/texts/8`


`GET /texts/id`

    curl -X 'GET' 'http://127.0.0.1:8000/texts/8' -H 'accept: application/json'

### Response
    Request Method: GET
    Status Code: 200 OK
    content-length: 37 
    content-type: application/json 
    date: Mon,24 May 2021 16:36:54 GMT 
    server: uvicorn 

    {"Content": "some new text", "Views": 4}
    
## Get text by non-existent id

### Request

Url `http://127.0.0.1:8000/texts/189`


`GET /texts/id`

    curl -X 'GET' 'http://127.0.0.1:8000/texts/189' -H 'accept: application/json'

### Response
    Request Method: GET
    Status Code: 404 Not found
    content-length: 37 
    content-type: application/json 
    date: Mon,24 May 2021 16:36:54 GMT 
    server: uvicorn 

    {"detail": "Text not found"}
    
## Add text
For authorised users only 
### Request

Url `http://127.0.0.1:8000/texts`

`POST /texts`

    curl -X 'POST' 'http://127.0.0.1:8000/texts' -H 'accept: application/json' -H 'Cookie: session_token=149a2637a75198d31584aea83075199198a494f3aa8c68a78604380fb9e17c65' -H 'Content-Type: application/json' -d '{"content": "some text"}'

### Response
    Request Method: POST
    Status Code: 201 Created
    content-length: 31 
    content-type: application/json 
    date: Mon,24 May 2021 17:40:02 GMT 
    server: uvicorn 

    {"id": 72,"Content": "some text"}
    
## Update text by id
For authorised users only 
### Request

Url `http://127.0.0.1:8000/texts/15`


`PUT /texts/id`

    curl -X 'PUT' 'http://127.0.0.1:8000/texts/15' -H 'accept: application/json' -H 'Cookie: session_token=149a2637a75198d31584aea83075199198a494f3aa8c68a78604380fb9e17c65' -H 'Content-Type: application/json' -d '{"content": "new text"}'

### Response
    Request Method: PUT
    Status Code: 200 OK
    content-length: 31 
    content-type: application/json 
    date: Mon,24 May 2021 17:40:02 GMT 
    server: uvicorn 

    {"id": 15,"New content": "new text"}
    
## Update text by non-existent id
For authorised users only 
### Request

Url `http://127.0.0.1:8000/texts/1`


`PUT /texts/id`

    curl -X 'PUT' 'http://127.0.0.1:8000/texts/1' -H 'accept: application/json' -H 'Cookie: session_token=149a2637a75198d31584aea83075199198a494f3aa8c68a78604380fb9e17c65' -H 'Content-Type: application/json' -d '{"content": "new text"}'

### Response
    Request Method: PUT
    Status Code: 404 Not found
    content-length: 27 
    content-type: application/json 
    date: Mon,24 May 2021 17:58:38 GMT 
    server: uvicorn 

    {"detail": "Text not found"}
    
## Delete text by id
For authorised users only 
### Request

Url `http://127.0.0.1:8000/texts/72`


`DELETE /texts/id`

    curl -X 'DELETE' 'http://127.0.0.1:8000/texts/72' -H 'accept: application/json' -H 'Cookie: session_token=149a2637a75198d31584aea83075199198a494f3aa8c68a78604380fb9e17c65'

### Response
    Request Method: DELETE
    Status Code: 200 Ok
    content-length: 9 
    content-type: application/json 
    date: Mon,24 May 2021 17:57:34 GMT 
    server: uvicorn  

    "Deleted"
    
## Delete text by non-existent id
For authorised users only 
### Request

Url `http://127.0.0.1:8000/texts/72098`


`DELETE /texts/id`

    curl -X 'DELETE' 'http://127.0.0.1:8000/texts/72098' -H 'accept: application/json' -H 'Cookie: session_token=149a2637a75198d31584aea83075199198a494f3aa8c68a78604380fb9e17c65'

### Response
    Request Method: DELETE
    Status Code: 404 Not found
    content-length: 27 
    content-type: application/json 
    date: Mon,24 May 2021 18:00:00 GMT 
    server: uvicorn 

    {"detail": "Text not found"}





