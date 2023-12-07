from lib.peep import Peep, PeepRepository

## TESTS FOR PEEP CLASS

def test_peep_init():
    peep = Peep(1, 'Test peep', '2023-12-07 11:09:44.176188', 2)
    assert peep.id == 1
    assert peep.content == 'Test peep'
    # This will come from calling str() on datetime.now()
    assert peep.time_stamp == '2023-12-07 11:09:44.176188'
    assert peep.user_id == 2

def test_equal():
    peep = Peep(1, 'Test peep', '2023-12-07 11:09:44.176188', 2)
    peep2 = Peep(1, 'Test peep', '2023-12-07 11:09:44.176188', 2)
    assert peep == peep2

def test_repr():
    peep = Peep(1, 'Test peep', '2023-12-07 11:09:44.176188', 2)
    assert str(peep) == "Peep(id=1, content='Test peep', time_stamp='2023-12-07 11:09:44.176188', user_id=2)"


## TESTS FOR PEEP REPOSITORY CLASS
def test_all_returns_list_of_all_peeps(db_connection):
    db_connection.seed('seeds/peep.sql')
    peep_repo = PeepRepository(db_connection)
    assert peep_repo.all() == [
        Peep(1, 'Test peep1 from user 1', '2023-12-07 11:09:44.176188', 1),
        Peep(2, 'Test peep2 from user 1', '2023-12-07 11:32:29.716127', 1),
        Peep(3, 'Test peep1 from user 2', '2023-12-07 11:34:13.084608', 2),
        Peep(4, 'Test peep2 from user 2', '2023-12-07 11:44:34.612564', 2),
    ]

def test_get_all_peeps_for_single_user(db_connection):
    db_connection.seed('seeds/peep.sql')
    peep_repo = PeepRepository(db_connection)
    assert peep_repo.all_by_user(2) == [
        Peep(3, 'Test peep1 from user 2', '2023-12-07 11:34:13.084608', 2),
        Peep(4, 'Test peep2 from user 2', '2023-12-07 11:44:34.612564', 2),
    ]

def test_find_by_id(db_connection):
    db_connection.seed('seeds/peep.sql')
    peep_repo = PeepRepository(db_connection)
    assert peep_repo.find_by_id(2) == Peep(2, 'Test peep2 from user 1', '2023-12-07 11:32:29.716127', 1)


def test_create_new_peep(db_connection):
    db_connection.seed('seeds/peep.sql')
    peep_repo = PeepRepository(db_connection)
    peep = Peep(None, 'Test create new peep for user 1', '2023-12-07 12:19:07.595786', 1)
    return_peep_id = peep_repo.create_new(peep)
    assert return_peep_id == 5
    assert peep_repo.all() == [
        Peep(1, 'Test peep1 from user 1', '2023-12-07 11:09:44.176188', 1),
        Peep(2, 'Test peep2 from user 1', '2023-12-07 11:32:29.716127', 1),
        Peep(3, 'Test peep1 from user 2', '2023-12-07 11:34:13.084608', 2),
        Peep(4, 'Test peep2 from user 2', '2023-12-07 11:44:34.612564', 2),
        Peep(5, 'Test create new peep for user 1', '2023-12-07 12:19:07.595786', 1)
    ]
