from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='ramesh')
        u.set_password('testpass')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('testpass'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_starred(self):
        u1 = User(username='ramesh', email='ramesh@example.com')
        u2 = User(username='suresh', email='suresh@example.com')
        p1 = Post(book_name='Maths', cost='450')
        p2 = Post(book_name='Science', cost='300')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        self.assertEqual(u1.starred, [])
        self.assertEqual(u2.starred, [])
        self.assertEqual(list(p1.starrers), [])
        self.assertEqual(list(p2.starrers), [])

        u1.star(p1)
        db.session.commit()
        self.assertTrue(u1.is_starred(p1))
        self.assertEqual(len(u1.starred), 1)
        self.assertEqual(u1.starred[0].book_name, 'Maths')
        self.assertEqual(p1.starrers.first().username, 'ramesh')
        self.assertEqual(p1.starrers.count(), 1)

        u1.unstar(p1)
        db.session.commit()
        self.assertFalse(u1.is_starred(p1))
        self.assertEqual(len(u1.starred), 0)
        self.assertEqual(p1.starrers.count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
