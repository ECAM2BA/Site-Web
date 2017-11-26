import cherrypy

class Root:
    @cherrypy.expose
    def index(self):
        return """
            <html>
               <head></head>
               <body>
                  <a href = "admin">Admin </a>
               </body>
            </html>
            """

class Admin:

    @cherrypy.expose
    def index(self):
        return "This is a private area"

if __name__ == '__main__':
    def get_users():
        # 'test': 'test'
        return {'test': 'test'}

    conf = {'/admin': {
            'tools.basic_auth.on': True,
            'tools.basic_auth.realm': 'Website name',
            'tools.basic_auth.users': get_users,
                       }}

    root = Root()
    root.admin = Admin()
    cherrypy.quickstart(root, '/', config=conf)