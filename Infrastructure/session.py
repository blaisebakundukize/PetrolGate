import os
import webapp2
import jinja2
from webapp2_extras import sessions
from Models.modelFetch import Model
from Infrastructure import filters


def user_required(handler):
    """
            Decorator for checking if there's a user associated with the current session.
            Will also fail if there's no session present.
    """
    def check_login(self, *args, **kwargs):
        user = self.get_user()
        if not user:
            # If handler has no login_url specified invoke a 403 error
            try:
                print('log in first!!!!!!!!!!!! ')
                self.redirect('/login')
            except (AttributeError, KeyError), e:
                self.abort(403)
        else:
            self.user = user
            return handler(self, *args, **kwargs)

    return check_login


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        if self.session_store.get_session().new:
            # modified session will be re-sent
            self.session_store.get_session().update({})

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def get_user(self):
        if "user_id" in self.session and self.session["user_id"] is not None:
            return self.session["user_id"]

    def get_connection(self):
        user = self.get_user()
        conn = Model(user['user'], user['pass'])
        connection = conn.connect
        return connection

    def get_user_id(self):
        user = self.get_user()
        user_id = user['employee_id']
        return user_id

    def get_user_company_id(self):
        user = self.get_user()
        company_id = user['company_id']
        return company_id

    @webapp2.cached_property
    def jinja2(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/../views/'),
            extensions=['jinja2.ext.autoescape'],
            autoescape=True)
        env.filters["add_hash"] = filters.add_hash
        return env

    def render_template(self, filename, **template_args):
        env = self.jinja2
        template = env.get_template(filename)
        self.response.write(template.render(**template_args))
























