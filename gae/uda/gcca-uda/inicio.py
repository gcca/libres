from webapp2 import RequestHandler, WSGIApplication
import re
import cgi

def escape_html(s):
	return cgi.escape(s, quote=True)


# ------------------------------------------------------------------------
# U2 1 ROT13
# ------------------------------------------------------------------------
u21form='''
<form method="post">
  <h2>2ROT13</h2>

  <textarea name="p" style="height:200px;width:324px">%s</textarea>

  <br>

  <input type="submit">
</form>
'''

class U21ROT13(RequestHandler):
	def get(self):
		self.response.out.write(u21form % '')

	def post(self):
		p = self.request.get('p')
		self.response.out.write(u21form % p.encode('rot13'))


# ------------------------------------------------------------------------
# U2 2 Validation Form
# ------------------------------------------------------------------------
u22form='''
<form method="post">

<table>
  <tr>
    <td>Username</td>
    <td><input type="text" name="username" value="%(username)s"></td>
    <td><span style="color:red">%(error_username)s</span></td>
  </tr>
  <tr>
    <td>Password</td>
    <td><input type="password" name="password"></td>
    <td><span style="color:red">%(error_password)s</span></td>
  </tr>

  <tr>
    <td>Verify Password</td>
    <td><input type="password" name="verify"></td>
    <td><span style="color:red">%(error_verify)s</span></td>
  </tr>

  <tr>
    <td>Email (optional)</td>
    <td><input type="text" name="email" value="%(email)s"></td>
    <td><span style="color:red">%(error_email)s</span></td>
  </tr>
</table>

  <input type="submit">
</form>
'''

u22welcome = '''
<h2>Welcome, %s!</h2>
'''

USR_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PWD_RE = re.compile(r'^.{3,20}$')
EM_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(username):
	return username and USR_RE.match(username)

def valid_password(password):
	return password and PWD_RE.match(password)

def valid_verify(password, verify):
	if password == verify:
		return verify

def valid_email(email):
	return not email or EM_RE.match(email)

class U22ValidationForm(RequestHandler):

	def get(self):
		self.write_form()

	def post(self):
		have_error = False
		usr_username = self.request.get('username')
		usr_password = self.request.get('password')
		usr_verify   = self.request.get('verify')
		usr_email    = self.request.get('email')

		params = dict(username = usr_username, email=usr_email)

		if not valid_username(usr_username):
			params['error_username'] = \
				'That\'s not a valid username.'
			have_error = True

		if not valid_password(usr_password):
			params['error_password'] = \
				'That\'s not a valid password.'
			have_error = True
		elif not valid_verify(usr_password, usr_verify):
			params['error_verify'] = \
				'Your passwords didn\'t match.'
			have_error = True

		if not valid_email(usr_email):
			params['error_email'] = \
				'That\'s not a valid email.'
			have_error = True

		if have_error:
			self.write_form(**params)

		else:
			self.redirect('/u2/2/welcome?username=%s' % usr_username)

	def write_form(self, username='', email='',
		error_username='',
		error_password='',
		error_verify='',
		error_email=''):

		self.response.out.write(u22form % {
			'username': username,
			'email': email,
			'error_username': error_username,
			'error_password': error_password,
			'error_verify': error_verify,
			'error_email': error_email
			})



class U22Welcome(RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write(u22welcome % username)


# ------------------------------------------------------------------------
# U3 0 Validation Form
# ------------------------------------------------------------------------
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(template_dir),
	autoescape=True)

class U30Handler(RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Art(db.Model):
	title   = db.StringProperty(required = True)
	art     = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class U30MainPage(U30Handler):
	def render_front(self, title='', art='', error=''):
		arts = db.GqlQuery('SELECT * FROM Art ORDER BY created DESC')
		self.render('u30_front.html',
			title=title, art=art, error=error, arts=arts)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get('title')
		art   = self.request.get('art')

		if title and art:
			a = Art(title = title, art = art)
			a.put()
			self.redirect('/u3/0')
		else:
			error = 'we need both a title and some artwork!'
			self.render_front(title, art, error)


# ------------------------------------------------------------------------
# U3 1 Blog
# ------------------------------------------------------------------------
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(template_dir),
	autoescape=True)

class U31Handler(RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class U31Blog(U31Handler):
	def get(self):
		posts = db.GqlQuery(
			'SELECT * FROM Post ORDER BY created  DESC')
		self.render('u31_blog.html', posts=posts)

class U31BlogPost(U31Handler):
	def get(self, post_id):
		#posts = db.GqlQuery('SELECT * FROM Post WHERE id = %s' % id)
		p = Post.get_by_id(int(post_id))

		if not p:
			self.error(404)
			return

		self.render('u31_blog.html', posts=[p])


class U31Newpost(U31Handler):
	def render_newpost(self, subject='', content='', error=''):
		self.render('u31_newpost.html',
			subject=subject, content=content, error=error)

	def get(self):
		self.render('u31_newpost.html')

	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')

		if subject and content:
			p = Post(subject=subject, content=content)
			p = p.put()
			self.redirect('/u3/1/blog/%d' % p.id())
		else:
			error = 'subject and content, please!'
			self.render_newpost(subject, content, error)


# ------------------------------------------------------------------------
# U4 1 Users
# ------------------------------------------------------------------------


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(template_dir),
	autoescape=True)

class U4UserHandler(RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def set_secure_cookie(self, name, val):
		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie',
			'user_id=; Path=/')

	def initialize(self, *a, **kw):
		RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

import hashlib
# def hash_str(s):
# 	return hashlib.md5(s).hexdigest()
import hmac

SECRET = 'gcca'
def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
	return '%s|%s' % (s, hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

import random
import string

def make_salt(length = 5):
	return ''.join(
		random.choice(string.letters) for _ in xrange(length))

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (salt, h)

def valid_pw(name, pw, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, pw, salt)

def users_key(group = 'default'):
	return db.Key.from_path('users', group)

class User(db.Model):
	username = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	email    = db.StringProperty() # db.EmailProperty()
	created  = db.DateTimeProperty(auto_now_add = True)

	@classmethod
	def by_id(cls, uid):
		return User.get_by_id(uid, parent=users_key())

	@classmethod
	def by_name(cls, name):
		u = User.all().filter('name =', name).get()
		return u

	@classmethod
	def register(cls, name, pw, email = None):
		pw_hash = make_pw_hash(name, pw)
		return User(parent = users_key(),
			name = name,
			pw_hash = pw_hash,
			email = email)

	@classmethod
	def login(cls, name, pw):
		u . cls.by_name(name)
		if u and valid_pw(name, pw, u.pw_hash):
			return u

def get_user(u):
	return User.all().filter('username =', u).get()

exists_user = get_user

def valid_user(name, pw):
	user = get_user(name)
	if user and user.password == pw:
		return user

class U41Signup(U4UserHandler):
	def get(self):
		self.write_form()

	def post(self):
		have_error = False
		username = self.request.get('username')
		password = self.request.get('password')
		verify   = self.request.get('verify')
		email    = self.request.get('email')

		params = dict(username=username, email=email)

		if not valid_username(username):
			params['error_username'] = \
				'That\'s not a valid username.'
			have_error = True
		elif exists_user(username):
			params['error_username'] = \
				'That user already exists.'
			have_error = True

		if not valid_password(password):
			params['error_password'] = \
				'That\'s not a valid password.'
			have_error = True
		elif not valid_verify(password, verify):
			params['error_verify'] = \
				'Your passwords didn\'t match.'
			have_error = True

		if not valid_email(email):
			params['error_email'] = \
				'That\'s not a valid email.'
			have_error = True

		if have_error:
			self.write_form(**params)

		else:
			password = make_pw_hash(username, password)
			params = dict(username=username, password=password)
			if email:
				params['email'] = db.Email(email)

			u = User(**params)
			u.put()

			secure_val = make_secure_val(username)

			self.response.headers.add_header('Set-Cookie',
				('name=%s; Path=/' % secure_val)
					.encode('utf-8'))
			self.redirect('/u4/1/welcome')

	def write_form(self, username='', email='',
		error_username='', error_password='',
		error_verify='', error_email=''):

		self.render('u41_signup.html',
			username=username,
			email=email,
			error_username=error_username,
			error_password=error_password,
			error_verify=error_verify,
			error_email=error_email)

class U41Welcome(U4UserHandler):
	def get(self):
		val = check_secure_val(self.request.cookies.get('name'))

		if val:
			self.response.out.write(
				'<h2>Welcome, %s.</h2>' % val)
		else:
			self.redirect('/u4/1/signup')

class U41Login(U4UserHandler):
	def write_form(self, username='', error=''):
		self.render('u41_login.html',
			username=username, error=error)

	def get(self):
		username = self.request.get('username')
		self.write_form(username)

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')

		u = get_user(username)

		if u and valid_pw(username, password, u.password):
			secure_val = make_secure_val(username)
			self.response.headers.add_header('Set-Cookie',
				('name=%s; Path=/' % secure_val)
					.encode('utf-8'))
			self.redirect('/u4/1/welcome')


		self.write_form(username=username,
			error='Invalid login')

class U41Logout(U4UserHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie',
			'name=;Path=/')
		self.redirect('/u4/1/signup')


# ------------------------------------------------------------------------
# U5 Blog JSON
# ------------------------------------------------------------------------
import json

class U5BlogJSON(RequestHandler):
	def get(self):
		self.response.headers.add_header('Content-Type',
			'application/json; charset=UTF-8')
		self.response.out.write(
			json.dumps([{
				'subject': p.subject,
				'content': p.content,
				'created': p.created.strftime('%b %d, %Y')}
			for p in Post.all()]))

class U5BlogPostJSON(RequestHandler):
	def get(self, postid):
		p = Post.get_by_id(int(postid))
		if not p:
			self.error(404)
			return

		self.response.out.write(json.dumps({
			'subject': p.subject,
			'content': p.content,
			'created': p.created.strftime('%b %d, %Y')}))


# ------------------------------------------------------------------------
# Main Page
# ------------------------------------------------------------------------
class MainPage(RequestHandler):
	def get(self):
		self.response.out.write('''
			<ul>
			<li> <a href="/u1/1"></a>
			<li> <a href="/u2/1">ROT13</a>
			<li> <a href="/u2/2">Validation Form</a>
			<li> <a href="/u3/0">ASCII Chain</a>
			<li> <a href="/u3/1/blog">/gcca - Blog/</a>
			<li> <a href="/u4/1/signup">Users - Signup</a>
			<li> <a href="/u4/1/login">Users - Login</a>
			<li> <a href="/u4/1/logout">Users - Logout</a>
			<li> <a href="/u5/blog.json">Blog JSON</a>
			</ul>
			''')


# ------------------------------------------------------------------------
# URLs
# ------------------------------------------------------------------------
app = WSGIApplication([
	('/',				MainPage),
	('/u2/1',			U21ROT13),
	('/u2/2',			U22ValidationForm),
	('/u2/2/welcome',		U22Welcome),
	('/u3/0',			U30MainPage),
	('/u3/1/blog',			U31Blog),
	('/u3/1/blog/(\d+)',		U31BlogPost),
	('/u3/1/blog/newpost',		U31Newpost),
	('/u4/1/signup',		U41Signup),
	('/u4/1/welcome',		U41Welcome),
	('/u4/1/login',			U41Login),
	('/u4/1/logout',		U41Logout),
	('/u5/blog.json',		U5BlogJSON),
	('/u5/blog/(\d+).json',		U5BlogPostJSON),
	('/u5/blog/newpost',		U31Newpost)
	], debug=True)