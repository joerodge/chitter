from dataclasses import dataclass

@dataclass
class Peep:
    id: int
    content: str
    time_stamp: str
    user_id: int


class PeepRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM peeps")
        peeps = []
        for row in rows:
            peeps.append(Peep(row['id'], row['content'], str(row['time_stamp']), row['user_id']))
        return peeps
    
    def all_by_user(self, user_id):
        rows = self._connection.execute(
            "SELECT * FROM peeps WHERE user_id = %s", [user_id]
        )
        peeps = []
        for row in rows:
            peeps.append(Peep(row['id'], row['content'], str(row['time_stamp']), row['user_id']))
        return peeps
    
    def find_by_id(self, peep_id):
        rows = self._connection.execute(
            "SELECT * FROM peeps WHERE id = %s", [peep_id]
        )
        return Peep(rows[0]['id'], rows[0]['content'], str(rows[0]['time_stamp']), rows[0]['user_id'])

    def create_new(self, content, time_stamp, user_id):
        rows = self._connection.execute(
            "INSERT INTO peeps(content, time_stamp, user_id) " \
            "VALUES (%s, %s, %s) RETURNING ID", [content, time_stamp, user_id]
        )
        return rows[0]['id']