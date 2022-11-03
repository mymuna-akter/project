import pytest

from app import create_app
from db_connections import db
from models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()


def test_create_user(client):
    rv = client.post('/user', json={
        "first_name":"X",
        "last_name":"y",
        "user_type":"parent",
        "address":{
            "street":"a",
            "state":"b",
            "city":"c",
            "zip":"4000"
        }
    })
    assert rv.status_code == 200

    data= rv.get_json()
    user = User.query.filter(User.id==1).first()
    assert user.first_name == "X"






