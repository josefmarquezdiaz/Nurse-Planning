from flask import Flask, request, Response, make_response, json, g
from flask.ext.restful import Resource, Api, reqparse, abort
from werkzeug.exceptions import NotFound, UnsupportedMediaType

import database
from utils import RegexConverter

# Define the application and the api
app = Flask(__name__, static_url_path = "", static_folder = "images")
api = Api(app)

DEFAULT_DB_PATH = 'db/hospital.db'

# Define the application and the api
app = Flask(__name__)
app.debug = True
# Set the database
app.config.update({'DATABASE': database.HospitalDatabase(DEFAULT_DB_PATH)})
api = Api(app)

# Associates an instance of the database before each request
@app.before_request
def set_database():
    g.db = app.config['DATABASE']


# Define the resources
class Nurses_list(Resource):
    # GET
    def get(self):

        nurses_list_db = g.db.get_nurses_list()

        nurses_list = []
        for nurse in nurses_list_db:
            _nurseid = nurse["id"]
            _nursename = nurse["name"]
            _nursesurname = nurse["surname"]
            _nurseurl = api.url_for(Nurses_profile, nurseid=_nurseid)
            print _nurseurl
            nurse = {}
            nurse['name'] = _nursename
            nurse['surname'] = _nursesurname
            nurse['link'] = {'rel': 'self', 'href': _nurseurl, 'rel': 'self'}
            nurses_list.append(nurse)
        # Create the envelope
        envelope = {}
        envelope['nurses_list'] = nurses_list

        return envelope

    # POST
    def post(self):

        nurse = request.get_json()
        if not nurse:
            raise UnsupportedMediaType()
        nursename, nursesurname, nursepn, nurseaddress = None, None, None, None
        try:
            nursename = nurse['name']
            nursesurname = nurse['surname']
            nursepn = nurse['phone_number']
            nurseaddress = nurse['address']
        except Exception:
            abort(400)
        newnurseid = g.db.append_nurse(nursename, nursesurname, nursepn, nurseaddress)
        if not newnurseid:
            abort(500)
        url = api.url_for(Nurses_profile, nurseid=newnurseid)

        return None, 201, {'Location': url}


class Nurses_profile(Resource):
    # GET
    def get(self, nurseid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        nurse = g.db.get_nurse(nurseid)
        if not nurse:
            abort(404)
        nurse['link'] = {'title': 'patient list', 'rel': 'related',
                         'href': api.url_for(Nurses_patient_list, nurseid=nurseid)}

        envelope = {}
        envelope['link'] = {'title': 'nurses list', 'rel': 'related', 'href': api.url_for(Nurses_list)}
        envelope['nurse'] = nurse

        return envelope

    # PUT
    def put(self, nurseid):

        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        if not g.db.contains_nurse(nurseid):
            abort(404)

        nurse = request.get_json()
        if not nurse:
            raise UnsupportedMediaType()

        try:
            nursename = nurse['name']
            nursesurname = nurse['surname']
            nursepn = nurse['phone_number']
            nurseaddress = nurse['address']
            g.db.modify_nurse(nurseid, nursename, nursesurname, nursepn, nurseaddress)
        except Exception:
            abort(400)

        return None, 204, {"name": nursename, "surname": nursesurname, "phone number": nursepn, "address": nurseaddress}

    # DELETE
    def delete(self, nurseid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if self._isauthorized(nurseid, authorization):
            if g.db.delete_nurse(nurseid):
                return None,204
            else:
                abort(404)
        else:
            return {'message': "No permission to access the data."},401
        '''
        if g.db.delete_nurse(nurseid):
            return None, 204
        else:
            abort(404)

    def _isauthorized(self, nurseid, authorization):
        if authorization is not None and (authorization.lower() == "admin" or authorization.lower() == nurseid.lower()):
            return True
        return False


class Nurses_patient_list(Resource):
    # GET
    def get(self, nurseid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        nurses_patient_list_db = g.db.get_nurses_patient_list(nurseid)

        nurses_patient_list = []
        for patient in nurses_patient_list_db:
            _patientid = patient["id"]
            _patientname = patient["name"]
            _patientsurname = patient["surname"]
            _patientroom = patient["room"]
            _patientdoctor = patient["doctor id"]
            args = {'patientid': _patientid, 'nurseid': nurseid}
            _patienturl = api.url_for(Nurses_patient_profile, **args)
            print _patienturl
            patient = {}
            patient['name'] = _patientname
            patient['surname'] = _patientsurname
            patient['room'] = _patientroom
            patient['doctor id'] = _patientdoctor
            patient['link'] = {'rel': 'related', 'href': _patienturl, 'rel': 'related'}
            nurses_patient_list.append(patient)
        # Create the envelope
        envelope = {}
        envelope['link'] = {'title': 'nurse', 'rel': 'related', 'href': api.url_for(Nurses_profile, nurseid=nurseid)}
        envelope['nurses_patient_list'] = nurses_patient_list

        return envelope

    def _isauthorized(self, nurseid, authorization):
        if authorization is not None and (authorization.lower() == "admin" or authorization.lower() == nurseid.lower()):
            return True
        return False


class Nurses_patient_profile(Resource):
    # GET
    def get(self, nurseid, patientid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        patient = g.db.get_patient(patientid)
        if not patient:
            abort(404)
        patient['link'] = {'title': 'patient medication', 'rel': 'related',
                           'href': api.url_for(Patient_medication_list, nurseid=nurseid, patientid=patientid)}

        envelope = {}
        envelope['link'] = {'title': 'patient list', 'rel': 'related',
                            'href': api.url_for(Nurses_patient_list, nurseid=nurseid)}
        envelope['patient'] = patient

        return envelope

    # PUT
    def put(self, nurseid, patientid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        if not g.db.contains_patient(patientid):
            abort(404)

        patient = request.get_json()
        if not patient:
            raise UnsupportedMediaType()

        try:
            patientname = patient['name']
            patientsurname = patient['surname']
            patientroom = patient['room']
            patientpn = patient['phone_number']
            patientaddress = patient['address']
            g.db.modify_patient(patientid, patientname, patientsurname, patientroom, patientpn, patientaddress)
        except Exception:
            abort(400)

        return None, 204, {"name": patientname, "surname": patientsurname, "room": patientroom,
                           "phone number": patientpn, "address": patientaddress}

    # DELETE
    def delete(self, nurseid, patientid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if self._isauthorized(nurseid, authorization):
            if g.db.delete_patient(patientid):
                return None,204
            else:
                abort(404)
        else:
            return {'message': "No permission to access the data."},401
        '''
        if g.db.delete_patient(patientid):
            return None, 204
        else:
            abort(404)

    def _isauthorized(self, nurseid, authorization):
        if authorization is not None and (authorization.lower() == "admin" or authorization.lower() == nurseid.lower()):
            return True
        return False


class Patient_medication_list(Resource):
    # GET
    def get(self, nurseid, patientid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        patient_medication_list_db = g.db.get_patient_medication_list(patientid)

        patient_medication_list = []
        for medicament in patient_medication_list_db:
            _medicamentid = medicament["id"]
            _medicamentname = medicament["name"]
            args = {'nurseid': nurseid, 'patientid': patientid, 'medicamentid': _medicamentid}
            _medicamenturl = api.url_for(Patient_medication, **args)
            print _medicamenturl
            medicament = {}
            medicament['name'] = _medicamentname
            medicament['link'] = {'rel': 'self', 'href': _medicamenturl, 'rel': 'self'}
            patient_medication_list.append(medicament)
        # Create the envelope
        envelope = {}
        envelope['link'] = {'title': 'patient', 'rel': 'related',
                            'href': api.url_for(Nurses_patient_profile, nurseid=nurseid, patientid=patientid)}
        envelope['patient_medication_list'] = patient_medication_list

        return envelope

    # POST
    def post(self, nurseid, patientid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        medicament = request.get_json()
        if not medicament:
            raise UnsupportedMediaType()
        medicamentname, medicamentdosage, medicamentduration, medicamenthours, medicamentbag, medicamentadministration, medicationpatient = None, None, None, None, None, None, None
        try:
            medicamentname = medicament['name']
            medicamentdosage = medicament['dosage']
            medicamentduration = medicament['duration']
            medicamenthours = medicament['hours']
            medicamentbag = medicament['bag_volume']
            medicamentadministration = medicament['administration']
            medicamentpatient = medicament['patientid']
        except Exception:
            abort(400)
        newmedicamentid = g.db.append_medication(medicamentname, medicamentdosage, medicamentduration, medicamenthours,
                                                 medicamentbag, medicamentadministration, medicamentpatient)
        if not newmedicamentid:
            abort(500)
        url = api.url_for(Patient_medication, nurseid=nurseid, patientid=patientid, medicamentid=newmedicamentid)

        return None, 201, {'Location': url}

    def _isauthorized(self, nurseid, authorization):
        if authorization is not None and (authorization.lower() == "admin" or authorization.lower() == nurseid.lower()):
            return True
        return False


class Patient_medication(Resource):
    # GET
    def get(self, nurseid, patientid, medicamentid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        medicament = g.db.get_medicament(medicamentid)
        if not medicament:
            abort(404)

        envelope = {}
        envelope['link'] = {'title': 'medication list', 'rel': 'related',
                            'href': api.url_for(Patient_medication_list, nurseid=nurseid, patientid=patientid)}
        envelope['medicament'] = medicament

        return envelope

    # PUT
    def put(self, nurseid, patientid, medicamentid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if not self._isauthorized(nurseid, authorization):
            return {'message': "No permission to access the data."},401
        '''
        if not g.db.contains_medicament(medicamentid):
            abort(404)

        medicament = request.get_json()
        if not medicament:
            raise UnsupportedMediaType()

        try:
            medicamentname = medicament['name']
            medicamentdosage = medicament['dosage']
            medicamentduration = medicament['duration']
            medicamenthours = medicament['hours']
            medicamentbag = medicament['bag_volume']
            medicamentadministration = medicament['administration']
            g.db.modify_medicament(medicamentid, medicamentname, medicamentdosage, medicamentduration, medicamenthours,
                                   medicamentbag, medicamentadministration)
        except Exception:
            abort(400)

        return None, 204, {"name": medicamentname, "dosage": medicamentdosage, "duration": medicamentduration,
                           "hours": medicamenthours, "bag_volume": medicamentbag,
                           "administration": medicamentadministration}

    # DELETE
    def delete(self, nurseid, patientid, medicamentid):
        '''
        authorization = None
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            pass
        if self._isauthorized(nurseid, authorization):
            if g.db.delete_medicament(medicamentid):
                return None,204
            else:
                abort(404)
        else:
            return {'message': "No permission to access the data."},401
        '''
        if g.db.delete_medicament(medicamentid):
            return None, 204
        else:
            abort(404)

    def _isauthorized(self, nurseid, authorization):
        if authorization is not None and (authorization.lower() == "admin" or authorization.lower() == nurseid.lower()):
            return True
        return False


app.url_map.converters['regex'] = RegexConverter

# define the routes
api.add_resource(Nurses_list, '/hospital/api/nurses/', endpoint='nurses')
api.add_resource(Nurses_profile, '/hospital/api/nurses/<regex("nur-\d+"):nurseid>/', endpoint='nurse')
api.add_resource(Nurses_patient_list, '/hospital/api/nurses/<regex("nur-\d+"):nurseid>/patients/', endpoint='npatients')
api.add_resource(Nurses_patient_profile,
                 '/hospital/api/nurses/<regex("nur-\d+"):nurseid>/patients/<regex("pat-\d+"):patientid>/',
                 endpoint='npatient')
api.add_resource(Patient_medication_list,
                 '/hospital/api/nurses/<regex("nur-\d+"):nurseid>/patients/<regex("pat-\d+"):patientid>/medication/',
                 endpoint='npmedication')
api.add_resource(Patient_medication,
                 '/hospital/api/nurses/<regex("nur-\d+"):nurseid>/patients/<regex("pat-\d+"):patientid>/medication/<regex("med-\d+"):medicamentid>/',
                 endpoint='npmedicament')

# Start the application
# DATABASE SHOULD BE POPULATED PREVIOUSLY
if __name__ == '__main__':
    print "Populating the database"
    # Debug true activates automatic code reloading and improved error messages
    app.run(debug=True)
