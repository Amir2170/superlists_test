from django.conf import settings
from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server


class MyListsTest(FunctionalTest):
	
	def create_pre_authenticated_session(self, email):
		if self.staging_server:
			session_key = create_session_on_server(self.staging_server, email)
		else:
			session_key = create_pre_authenticated_session(email)
		# now we setup the cookie
		self.browser.get(self.live_server_url + '/404_no_such_url/')
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/',
		))
	
	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		email = 'amirrezaamp2170@gmail.com'
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_out(email)
		
		self.create_pre_authenticated_session(email)
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_in(email)
		
