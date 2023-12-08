from lib.user import User, UserRepository

## TESTS FOR USER CLASS

def test_user_init():
    user = User(1, 'Test name', 'TestUsername', 'test@email.com', 'testpassword')
    assert user.id == 1
    assert user.name == 'Test name'
    assert user.username == 'TestUsername'
    assert user.email == 'test@email.com'
    assert user.password == 'testpassword'

def test_user_equal():
    user = User(1, 'Test name', 'TestUsername', 'test@email.com', 'testpassword')
    user2 = User(1, 'Test name', 'TestUsername', 'test@email.com', 'testpassword')
    print(user2)
    assert user == user2

def test_is_valid_method_with_empty_strs():
    user = User(None, 'Test name', 'TestUsername', 'test@email.com', 'testpassword')
    assert user.is_valid()
    user = User(None, '', 'TestUsername', 'test@email.com', 'testpassword')
    assert not user.is_valid()
    user = User(None, '', '', '', '')
    assert not user.is_valid()

"""
Test username is only valid for letters and numbers and underscore, no spaces
or special chars
"""
def test_is_valid_method_usernames():
    user = User(None, 'Test name', 'TestUsername', 'test@email.com', 'testpassword')
    assert user.is_valid()
    user = User(None, 'Test name', 'Test_Username99', 'test@email.com', 'testpassword')
    assert user.is_valid()
    # space in user name is invalid
    user = User(None, 'Test name', 'Test Username', 'test@email.com', 'testpassword')
    assert not user.is_valid()
    # special char invalid
    user = User(None, 'Test name', 'Test$Username', 'test@email.com', 'testpassword')
    assert not user.is_valid()


def test_is_valid_on_emails():
    valid = [
        'joe_hello@hotmail.com',
        'tony89@gmail.com',
        'joe.hello@email.com',
        'tom.harry@cab.gov.uk',
        'tom.harry@gmail.gov.something.uk',
        'joe.hello.hello@something.com',
        'john@12345.com',
    ]
    invalid = [
        'joe%$@email.com',
        'joe hello@gov.uk',
        'john@hello',
        'joe-89@email.com',
        'hello',
        'hello@',
        '@.com',
        'hello@.com',
        'joe@hello..com',
        'joe.com',
        'joe@email.',
        'joe..hello@mail.com',
        '.hello@mail.com',
        'hello.@hotmail.com',
        'joe@@mail.com',
        'joe@hello.com.',
        'joe_hello@hotmail.co_m',
        'joe_hello@hotmail.1com',
    ]
    valid_tests = []
    for email in valid:
        user = User(None, 'Test name', 'TestUsername', email, 'testpassword')
        valid_tests.append(user.is_valid())
    assert valid_tests == [True]*7

    invalid_tests = []
    for email in invalid:
        user = User(None, 'Test name', 'TestUsername', email, 'testpassword')
        invalid_tests.append(user.is_valid())
    assert invalid_tests == [False]*18


## TESTS FOR USER REPOSITORY CLASS

def test_get_user_by_id(db_connection):
    db_connection.seed('seeds/peep.sql')
    user_repo = UserRepository(db_connection)
    assert user_repo.get_user_by_id(2) == User(2, 'Test name2', 'TestUsername2', 'test2@email.com', 'testpassword2')

def test_create_new_user(db_connection):
    db_connection.seed('seeds/peep.sql')
    user_repo = UserRepository(db_connection)
    user = User(None, 'New test name', 'NewTestUsername', 'newtest@email.com', 'newtestpassword')
    user_id = user_repo.create_user(user)
    assert user_id == 3
    assert user_repo.get_user_by_id(3) == User(3, 'New test name', 'NewTestUsername', 'newtest@email.com', 'newtestpassword')

def test_get_user_by_username(db_connection):
    db_connection.seed('seeds/peep.sql')
    user_repo = UserRepository(db_connection)
    user = user_repo.get_user_by_username('TestUsername2')
    assert user == User(2, 'Test name2', 'TestUsername2', 'test2@email.com', 'testpassword2')


def test_get_all_users(db_connection):
    db_connection.seed('seeds/peep.sql')
    user_repo = UserRepository(db_connection)
    assert user_repo.get_all_users() == [
        User(1, 'Test name1', 'TestUsername1', 'test1@email.com', 'testpassword1'),
        User(2, 'Test name2', 'TestUsername2', 'test2@email.com', 'testpassword2')
    ]

def test_check_user_username_or_email_not_already_used(db_connection):
    db_connection.seed('seeds/peep.sql')
    user_repo = UserRepository(db_connection)
    # Username and email already in use on seed db
    user1 = User(1, 'Test name1', 'TestUsername1', 'test1@email.com', 'testpassword1')
    # email already in use
    user2 = User(2, 'new name', 'NewUser99', 'test2@email.com', 'testpassword2')
    # should be no errors for unique email and username
    user3 = User(None, 'New test name', 'NewTestUsername', 'newtest@email.com', 'newtestpassword')
    assert user_repo.check_user(user1) == [
        'There is already an account registered to test1@email.com',
        'TestUsername1 already in use',
    ]
    assert user_repo.check_user(user2) == [
        'There is already an account registered to test2@email.com'
    ]
    assert not user_repo.check_user(user3)
