import pytest
import fla
import unittest

@pytest.fixture
def client():
	fla.app.secret_key = "testkey"
	fla.app.config['SESSION_TYPE'] = 'filesystem'
	fla.mongo = MongoClient('localhost',27017)
	fla.app.config['TESTING'] = True
	client = fla.app.test_client()
	yield client



class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		self.app = fla.app.test_client()

	def login(self, username, password):
		return self.app.post('/login', data={'email':username,'pass':password}, follow_redirects=True)

	@pytest.fixture
	#Test case one
	def test_login(self):
		rv = self.login('prashanth.flassh98@gmail.com','Iamking1!')
		self.assert_equal(session['logged_in'],True)


if __name__ == '__main__':
    unittest.main()
