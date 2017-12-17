import json
import os.path

import cherrypy
import jinja2
import jinja2plugin
import jinja2tool
from cherrypy.lib.static import serve_file


class SiteWeb:
    """Web application of the ShareYourLinks (SYL) application."""

    def __init__(self):
        self.memes = self.loadmeme()
        self.users = self.loadusers()

    def loadusers(self):
        """Load links' database from the 'users.json' file."""
        try:
            with open('users.json', 'r') as file:
                content = json.loads(file.read())
                return content['users']
        except:
            cherrypy.log('Loading database failed.')
            return []

    def saveusers(self):
        """Save users' database to the 'users.json' file."""
        try:
            with open('users.json', 'w') as file:
                file.write(json.dumps({
                    'users': self.users
                }, ensure_ascii=False, indent=3))
        except:
            cherrypy.log('Saving database failed.')

    def savememes(self):
        """Save links' database to the 'db.json' file."""
        try:
            with open('db.json', 'w') as file:
                file.write(json.dumps({
                    'memes': self.memes
                }, ensure_ascii=False, indent=3))
        except:
            cherrypy.log('Saving database failed.')

    def loadmeme(self):
        """Load links' database from the 'db.json' file."""
        try:
            with open('db.json', 'r') as file:
                content = json.loads(file.read())
                return content['memes']
        except:
            cherrypy.log('Loading database failed.')
            return []

    def user_session(self):
        user_session = ''
        if cherrypy.session.get('user') is None:
            user_session = '''<li><a href="logincall">login</a></li>   
                <li><a href="createuserscall">New users</a></li>'''

        if cherrypy.session.get('user') is not None:
            user_session = '''<li><a href="user_profile">user profile : {}</a></li>
                <li><a href="logout">logout</a></li>'''.format(cherrypy.session.get('user'))
        return user_session

    def change_autor(self, old_user):
        for i in range(len(self.memes)):
            memes_db = self.memes[i]
            if old_user == memes_db['users']:
                memes_db['users'] = cherrypy.session.get('user')

    @cherrypy.expose
    def index(self, tag_filter=''):
        """Main page of the SYL's application."""
        if len(self.memes) == 0:
            mains = '<p>No memes in the database.</p>'
        else:
            mains = '<ol>'
            for i in range(len(self.memes)):
                datamemes = self.memes[i]
                tags_strings = str(datamemes['tags'])[1:-1]

                if tag_filter in datamemes['tags'] or tag_filter == "":
                    img = datamemes['img_ref']

                    mains += '''
                    <div>
                    <ul class="memes_list">
                        <h2 >{}</h2>
                        <img src="{}" class="img">
                        <p class="description">description:</p>
                        <p class="description">{}</p>
                        <p class="tags">{}</p>
                        <p class="tags">{}</p>
                    </ul>
                    </div>'''.format(datamemes['title'], img, datamemes['description'],
                                     tags_strings, datamemes['users'])
                    mains += '</ol>'
        return {'links': mains, 'user': self.user_session()}

    @cherrypy.expose
    def user_profile(self):
        user_profile = ''
        user_img = ''
        if cherrypy.session.get('user') is not None:

            if len(self.memes) == 0:
                user_profile = '<p>No memes in database</p>'
            else:
                for i in range(len(self.users)):
                    users_db = self.users[i]
                    if cherrypy.session.get('user') == users_db['username']:
                        user_img += '''<img src= "{}" alt="" style="width:100%">
                       <h1>{}</h1>
                            '''.format(users_db['user_img'], cherrypy.session.get('user'))

                for i in range(len(self.memes)):
                    data_memes = self.memes[i]
                    tags_strings = str(data_memes['tags'])[1:-1]

                    if cherrypy.session.get('user') == data_memes['users']:
                        img = data_memes['img_ref']
                        user_profile += '''
                        <div>
                        <ul class="memes_list">
                            <h2 >{}</h2>
                            <img src="{}" class="img">
                            <p class="description">{}</p>
                            <p class="tags">{}</p>
                            <p class="tags">{}</p>
                        </ul>
                        </div>'''.format(data_memes['title'], img, data_memes['description'],
                                         tags_strings, data_memes['users'])
                        user_profile += '</ol>'
                        if cherrypy.session.get('user') != data_memes['users']:
                            user_profile = '<p>No memes link to the user</p>'

            return {'user_profile': user_profile, 'user_card': user_img, 'user': self.user_session()}

    @cherrypy.expose
    def Edit_profile_call(self):
        for i in range(len(self.users)):
            usersdb = self.users[i]
            if cherrypy.session.get('user') == usersdb['username']:
                user_psw = usersdb['password']
                #user_img = usersdb['user_img']
                return {'user_name': cherrypy.session.get('user'),'user_psw': user_psw, 'user': self.user_session()}

    @cherrypy.expose
    def edit_profile(self, uname, psw, img='img/user_img.jpg'):

        for i in range(len(self.users)):
            usersdb = self.users[i]
            if cherrypy.session.get('user') == usersdb['username']:
                utilisateur = usersdb['username']
                mdp = usersdb['password']
                uimg = usersdb['user_img']

                if uname != utilisateur:
                    usersdb.update({'username': uname})
                    cherrypy.session['user'] = uname
                    self.change_autor(utilisateur)

                if psw != mdp:
                    usersdb['password'] = psw

                if img != uimg and img !='':
                    print(img)
                    upload_path = os.path.join(CURDIR, 'img/' + img.filename)
                    with open(upload_path, 'wb') as ufile:
                        while True:
                            data = img.file.read(8192)
                            if not data:
                                break
                            ufile.write(data)
                    usersdb['user_img'] = 'img/' + img.filename


        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def add(self):
        print(cherrypy.session.get('user'))
        if cherrypy.session.get('user') is not None:
            print("if")
            return {'user': self.user_session()}
        else:
            print("else")
            raise cherrypy.HTTPRedirect('/logincall')

    @cherrypy.expose
    def logincall(self):
        """Page with a form to add a new link."""
        return {'user': self.user_session()}

    @cherrypy.expose
    def createuserscall(self):
        """Page with a form to add a new link."""
        return {'user': self.user_session()}

    @cherrypy.expose
    def addmeme(self, title, memesimg, description, tags):
        """POST route to add a new link to the database."""
        if title != '' and memesimg:
            upload_path = os.path.join(CURDIR, 'img/' + memesimg.filename)
            with open(upload_path, 'wb') as ufile:
                while True:
                    data = memesimg.file.read(8192)
                    if not data:
                        break
                    ufile.write(data)
            self.memes.append({
                'title': title,
                'img_ref': 'img/' + memesimg.filename,
                'description': description,
                'users': cherrypy.session.get('user'),
                'tags': tags.split(','),
            })
            self.savememes()
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def createusers(self, uname, psw, img='img/user_img.jpg'):
        if len(self.users) == 0:
            cherrypy.session['user'] = uname
            self.users.append({
                'username': uname,
                'password': psw,
                'user_img': img,
            })
            self.saveusers()
            raise cherrypy.HTTPRedirect('/')

        for i in range(len(self.users)):
            usersdb = self.users[i]
            if uname == usersdb['username'] and psw == usersdb['password']:
                user_error = '<h2 style="text-color: Red">Utilisateur existant</h2>'
                print(user_error)
                return {'user_error': user_error}

        cherrypy.session['user'] = uname
        self.users.append({
            'username': uname,
            'password': psw,
            'user_img': img,
        })
        self.saveusers()
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def login(self, uname, psw):
        for i in range(len(self.users)):
            usersdb = self.users[i]
            if uname == usersdb['username'] and psw == usersdb['password']:
                cherrypy.session['user'] = uname
                raise cherrypy.HTTPRedirect('/')

        raise cherrypy.HTTPRedirect('/createuserscall')

    @cherrypy.expose
    def logout(self):
        del (cherrypy.session['user'])
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def getmeme(self):
        """GET route to get all the memes."""
        return json.dumps({
            'memes': self.memes
        }, ensure_ascii=False).encode('utf-8')

    @cherrypy.expose
    def deletememe(self, i):
        """GET route to delete a link."""
        result = 'KO'
        i = int(i)
        if 0 <= i < len(self.memes):
            del (self.memes[i])
            result = 'OK'
        return result.encode('utf-8')

    @cherrypy.expose
    def getusers(self):
        """GET route to get all the memes."""
        return json.dumps({
            'users': self.users
        }, ensure_ascii=False).encode('utf-8')

    @cherrypy.expose
    def deleteusers(self, i):
        """GET route to delete a link."""
        result = 'KO'
        i = int(i)
        if 0 <= i < len(self.users):
            del (self.users[i])
            result = 'OK'
        return result.encode('utf-8')


if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('./html'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()

    # Launch web server
    CURDIR = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(SiteWeb(), '', 'server.conf')

