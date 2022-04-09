from Halanweb import app
#from werkzeug.serving import run_simple


if __name__ == '__main__':
    #run_simple('localhost', 8050, app, use_reloader=True, use_debugger=True)
    app.run(debug=True)