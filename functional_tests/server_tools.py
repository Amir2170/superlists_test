from fabric.api import run
from fabric.context_managers import settings

def  _get_manage_dot_py(host):
	return f'~/sites/{host}/virtualenv/bin/python3.8 ~/sites/{host}/source/superlists_test/manage.py'
	
def reset_database(host):
	manage_dot_py = _get_manage_dot_py(host)
	with settings(host_string=f'elspeth@{host}'):
		run(f'{manage_dot_py} flush --noinput')

def create_session_on_server(host, email):
	manage_dot_py = _get_manage_dot_py
	with settings(host_string=f'elspeth{host}'):
		session_key = run(f'{manage_dot_py} create_session {email}')
		return session_key.strip()
