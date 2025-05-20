# tests/unit/test_user.py
import pytest
from fastapi import HTTPException
from app.services.user import create_user
from app.models.user import UserCreate

# Dummy SQLAlchemy-like user só para “retornar algo” no mock
class DummyUser:
    def __init__(self, email): 
        self.email = email

class MockDBSession:
    def __init__(self, duplicate: bool):
        self._dup = duplicate

    def query(self, model):
        return self

    def filter(self, condition):
        return self

    def first(self):
        return DummyUser("foo@bar.com") if self._dup else None

    def add(self, instance):    pass
    def commit(self):           pass
    def refresh(self, instance):pass

@pytest.mark.parametrize("user_data, should_succeed", [
    ({"nome":"John Doe","email":"foo@bar.com","senha":"pwd4545454clearcle"},  False),  # duplica
    ({"nome":"Jane Doe","email":"jane@bar.com","senha":"pwd454545"}, True),
])
def test_create_user(user_data, should_succeed):
    db = MockDBSession(duplicate=(not should_succeed))
    user_create = UserCreate(**user_data)

    if should_succeed:
        u = create_user(user_create, db)
        assert u.email == user_data["email"]
    else:
        with pytest.raises(HTTPException):
            create_user(user_create, db)
