import os
import webapp2
import jinja2
import hashlib

#Initialize Jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
class TestPage(Handler):
    def get(self):
        # Using Google App Engine for Python to render a html webpage called testpage.html
        self.render("testpage.html")
        
        # Set our secret code to 'h@ll0', username to "william" and password to "jackson"
        username, password = "william", "jackson"
        
        # Create a hash using keyword "william", "jackson" using a function called make_hash()
        hashed_pw = make_hash(username,password)
        
        # Set cookie to store a username value of william, and a hashed password value
        self.response.headers.add_header('Set-Cookie', "username=william")
        self.response.headers.add_header('Set-Cookie', "hashed_pw=" + str(hashed_pw))
        
        # Display the cookie's username and hashed password in browser's page
        self.response.out.write("cookie's = " + str(self.request.cookies.get('username')))
        self.response.out.write("<br    self.response.out.write(\"cookie'sw = " + str(self.request.cookies.get('hashed_pw')))
                
def make_hash(username, password, secret_code=None):
    if secret_code == None:
        secret_code = 'h@ll0'
    s = str(username) + str(password) + str(secret_code)
    hashed_pw = hashlib.sha256(s).hexdigest()
    return hashed_pw

app = webapp2.WSGIApplication([
                               ('/test', TestPage)
                                ], debug=True)
