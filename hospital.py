from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from hospital.resources import app as hospital
from hospital_admin.application import app as hospital_admin

application = DispatcherMiddleware(hospital, {
    '/hospital_admin': hospital_admin
})
if __name__ == '__main__':
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)
