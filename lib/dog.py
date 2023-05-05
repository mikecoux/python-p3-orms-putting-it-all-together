import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all_dogs = []

    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
    
    #Ask david why we need save & create methods
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    """ABOVE: PUSH TO DB, BELOW: RECEIVE FROM DB"""

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()
        cls.all_dogs = [cls.new_from_db(row) for row in all]
        return cls.all_dogs
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    """EXTRAS"""

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT *
            FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """
        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid
            )
        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
        

Dog.drop_table()
Dog.create_table()
spruce = Dog.create("spruce", "husky")
spruce.name = "sprucey"
spruce.update()
print(spruce.name)
print(Dog.find_by_id(1).name)
def find_spruce():
    try:
        Dog.find_by_name("spruce")
    except TypeError:
        print("Spruce not here.")
find_spruce()
