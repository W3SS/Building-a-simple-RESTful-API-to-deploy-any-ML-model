#{'x':2,'y':5,'z':4,'details':{'info':6}}
import cherrypy
from paste.translogger import TransLogger
from app import create_app
#import app


def run_server(app):

    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 8777,
        'server.socket_host': '0.0.0.0' # .24
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    # Init spark context and load libraries
    
    
    app = create_app()
    
    
    

    # start web server
    #run_server(app)
    app.run(host='0.0.0.0',port='8777') # .24
