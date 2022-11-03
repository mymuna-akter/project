### About
This project is about doing some simple CRUD operations following DDD(Domain Driven Design) and TDD(Test Driven Design) architecture.
I have used Python's Flask restful framework with database sqlite.

### Installation

#### Pre-Requisites:
- Python 3.9.6
- Sqlite 3.11.1

To run the project, at first create virtual environment and activate it and follow below commands:

environment set-up
```python
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
export Flask_APP=App.py
```
database set up:
```python
flask db init
flask db migrate
flask db upgrade
```
run the project
```python
flask run
```

### Features
- create user. user can be parent user or child user
- create child user belongs to a parent user. Will not allow a child user with address
- delete parent user. Will be deleted all child user of this parent user
- delete child user without deleting corresponded parent user
- update user's basic info
- find user info
- find list of users
- find list of parent IDs
- find list of child IDs
- find child user info with parent 
- find parent user info with child

### API URL
``` 
{{base_url}}/user 
{{base_url}}/user/{id} 
{{base_url}}/parent-ids
{{base_url}}/parent/{id}
{{base_url}}/child-ids
{{base_url}}/child/{id}
```
### Sample request
sample 1
```
curl --location --request POST 'http://127.0.0.1:5000/user' \
--header 'Content-Type: application/json' \
--data-raw '{
 "first_name":"X",
 "last_name":"Y",
 "user_type":"parent",
 "address":{
     "street":"a",
     "state":"b",
     "city":"c",
     "zip":"4000"
 }
}'
```
sample 2
```
curl --location --request POST 'http://127.0.0.1:5000/user' \
--header 'Content-Type: application/json' \
--data-raw '{

 "first_name":"z",
 "last_name":"y",
 "user_type":"child",
 "parent_id": 1
}'
```
sample 3
```
curl --location --request PUT 'http://127.0.0.1:5000/user' \
--header 'Content-Type: application/json' \
--data-raw '{
  
  "user_id":1,
 "first_name":"z"

}'
```

## Testing



