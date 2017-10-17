import unittest, copy
import json

import flask

import hospital.resources as resources
import hospital.database

db_path ='db/hospital_test.db'
#For non persistent database
#db = hospital.database.HospitalNonPersistentDatabase()
db = hospital.database.HospitalDatabase(db_path)

class ResourcesAPITestCase(unittest.TestCase):
   
    def setUp(self):
        try:
            db.clean()
        except:
            pass
        resources.app.config['TESTING'] = True
        resources.app.config['DATABASE'] = db
        db.load_init_values()
        self.client = resources.app.test_client()

    def tearDown(self):
        db.clean()

#@unittest.skip("showing class skipping")
class NursesListTestCase (ResourcesAPITestCase):
   
    url = '/hospital/api/nurses/'
    nurse_url = '/hospital/api/nurses/nur-2/'
    new_nurse = {u"name":u"platano", u"surname":u"amarillo", u"phone number":100, u"address":u"canarias, palmera 32"}
    new_nurse_wrong = {u"name":u"irene"}
    
    @classmethod
    def setUpClass(cls):
        print 'Testing NursesListTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        print self.test_url.__doc__
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Nurses_list)
    
    def test_get_nurses(self):
        '''
        Checks that GET nurses_list return correct status code and data format
        '''
        print self.test_get_nurses.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEquals(resp.status_code,200)
            data = json.loads(resp.data)
            nurses_list = data['nurses_list']
            self.assertEquals(len(nurses_list),11)
            nur0 = nurses_list [0]
            self.assertIn('name',nur0)
            self.assertIn('surname',nur0)
            link0 = nur0['link']
            self.assertIn(resources.api.url_for(resources.Nurses_list),link0['href'])

    def test_add_nurse(self):
        '''
        Checks that the nurse is added correctly
        '''
        print '('+self.test_add_nurse.__name__+')', self.test_add_nurse.__doc__
        resp = self.client.post(self.url,
                                data=json.dumps(self.new_nurse),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 201)
        self.assertIn('Location', resp.headers)
        nurse_url = resp.headers['Location']
        resp2 = self.client.get(nurse_url,
                                data=json.dumps(self.new_nurse),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 200)

    def test_add_nurse_wrong(self):
        '''
        Try to add a nurse with wrong format
        '''
        print '('+self.test_add_nurse_wrong.__name__+')', self.test_add_nurse_wrong.__doc__
        resp = self.client.post(self.url,
                                data=json.dumps(self.new_nurse_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 400)

#@unittest.skip("showing class skipping")
class NurseTestCase (ResourcesAPITestCase):
    
    url = '/hospital/api/nurses/nur-1/'
    url_wrong = '/hospital/api/nurses/nur-290/'
    nur_1_request = {u"id":u"nur-1", u"name":u"ciruela", u"surname":u"podrida", u"phone number":91342421, u"address":u"ciruelo, rama 7"}
    nur_1_request_wrong = {u"id":u"nur-394"}

    @classmethod
    def setUpClass(cls):
        print 'Testing NurseTestCase'
      
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        print self.test_url.__doc__
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Nurses_profile)
    
    def test_wrong_url(self):
        '''
        Checks that GET nurse_profile return correct status code if given a wrong url
        '''
        resp = self.client.get(self.url_wrong, data=json.dumps(self.url_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 404)
    
    def test_get_nurse(self):
        '''
        Checks that GET nurse_profile return correct status code and data format
        '''
        print self.test_get_nurse.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url, data=json.dumps(self.nur_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
            self.assertEquals(resp.status_code ,200)
            data = json.loads(resp.data)
            link = data['link']
            self.assertEquals(link['title'],'nurses list')
            self.assertEquals(link['rel'],'related')
            self.assertEquals(link['href'],resources.api.url_for(resources.Nurses_list))
            nurse = data ['nurse']
            for attribute in ('id','name', 'surname', 'phone number', 'address'):
                self.assertIn(attribute, nurse)

    def test_modify_nurse(self):
        '''
        Modify an existing nurse and check that the nurse has been modified correctly in the server
        '''
        print self.test_modify_nurse.__doc__
        resp = self.client.put(self.url,
                                data=json.dumps(self.nur_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url,
                                data=json.dumps(self.nur_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        self.assertDictContainsSubset(self.nur_1_request, data['nurse'])

    def test_modify_wrong_nurse(self):
        '''
        Try to modify a nurse with wrong format
        '''
        print self.test_modify_wrong_nurse.__doc__
        resp = self.client.put(self.url,
                                data=json.dumps(self.nur_1_request_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 400)

    def test_modify_unexisting_nurse(self):
        '''
        Try to modify an unexisting nurse
        '''
        print self.test_modify_unexisting_nurse.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.nur_1_request_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 404)

    def test_delete_nurse(self):
        '''
        Checks that DELETE nurses_profile return correct status code if corrected delete
        '''
        print self.test_delete_nurse.__doc__
        nurse = copy.deepcopy(self.nur_1_request)
        resp = self.client.delete(self.url, data=json.dumps(nurse),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url, data=json.dumps(nurse),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_nurse(self):
        '''
        Checks that DELETE nurses_profile return correct status code if given a wrong address
        '''
        print self.test_delete_unexisting_nurse.__doc__
        nurse = copy.deepcopy(self.nur_1_request_wrong)
        resp = self.client.delete(self.url_wrong, data=json.dumps(nurse),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 404)

#@unittest.skip("showing class skipping")
class PatientsListTestCase (ResourcesAPITestCase):
   
    url = '/hospital/api/nurses/nur-0/patients/'
    
    @classmethod
    def setUpClass(cls):
        print 'Testing PatientsListTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        print self.test_url.__doc__
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Nurses_patient_list)

    def test_get_patients(self):
        '''
        Checks that GET nurses_patient_list return correct status code and data format
        '''
        print self.test_get_patients.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url, data=json.dumps(self.url),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
            self.assertEquals(resp.status_code,200)
            data = json.loads(resp.data)
            link = data['link']
            self.assertEquals(link['title'],'nurse')
            self.assertEquals(link['rel'],'related')
            self.assertEquals(link['href'],resources.api.url_for(resources.Nurses_profile,nurseid='nur-0'))
            patients_list = data['nurses_patient_list']
            self.assertEquals(len(patients_list),6)
            pat0 = patients_list[0]
            self.assertIn('name',pat0)
            self.assertIn('surname',pat0)
            self.assertIn('room',pat0)
            self.assertIn('doctor id',pat0)
            link0 = pat0['link']
            self.assertIn(resources.api.url_for(resources.Nurses_patient_list,nurseid='nur-0'),link0['href'])

#@unittest.skip("showing class skipping")
class PatientTestCase (ResourcesAPITestCase):
    
    url = '/hospital/api/nurses/nur-0/patients/pat-1/'
    url_wrong = '/hospital/api/nurses/nur-0/patients/patient-1/'
    pat_1_request = {u"id":u"pat-1", u"name":u"canco", u"surname":u"rodriguez", u"room":u"3B",u"phone number":42993851, u"address":u"cama 7",u"nurse id":u"nur-0", u"doctor id":u"doc-1"}
    pat_1_request_wrong = {u"id":u"nur-394"}

    @classmethod
    def setUpClass(cls):
        print 'Testing PatientTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        print self.test_url.__doc__
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Nurses_patient_profile)
    
    def test_wrong_url(self):
        '''
        Checks that GET nurses_patient_profile return correct status code if given a wrong url
        '''
        resp = self.client.get(self.url_wrong)
        self.assertEquals(resp.status_code, 404)
    
    def test_get_patient(self):
        '''
        Checks that GET nurses_patient_profile return correct status code and data format
        '''
        print self.test_get_patient.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url, data=json.dumps(self.pat_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
            self.assertEquals(resp.status_code ,200)
            data = json.loads(resp.data)
            link = data['link']
            self.assertEquals(link['title'],'patient list')
            self.assertEquals(link['rel'],'related')
            self.assertEquals(link['href'],resources.api.url_for(resources.Nurses_patient_list,nurseid='nur-0'))
            patient = data ['patient']
            for attribute in ('id','name', 'surname','room', 'phone number', 'address', 'nurse id', 'doctor id'):
                self.assertIn(attribute, patient)

    def test_modify_patient(self):
        '''
        Modify an exsiting patient and check that the patient has been modified correctly in the server
        '''
        print self.test_modify_patient.__doc__
        resp = self.client.put(self.url,
                                data=json.dumps(self.pat_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url,
                                data=json.dumps(self.pat_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        self.assertDictContainsSubset(self.pat_1_request, data['patient'])

    def test_modify_wrong_patient(self):
        '''
        Try to modify a patient with wrong format
        '''
        print self.test_modify_wrong_patient.__doc__
        resp = self.client.put(self.url,
                                data=json.dumps(self.pat_1_request_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 400)

    def test_modify_unexisting_patient(self):
        '''
        Try to modify an unexisting patient
        '''
        print self.test_modify_unexisting_patient.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.pat_1_request_wrong),
                                headers={"Content-Type":"application/json"})
        self.assertEquals(resp.status_code, 404)

    def test_delete_patient(self):
        '''
        Checks that DELETE nurses_patient_profile return correct status code if corrected delete
        '''
        print self.test_delete_patient.__doc__
        resp = self.client.delete(self.url,
                                data=json.dumps(self.pat_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url,
                                data=json.dumps(self.pat_1_request_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_patient(self):
        '''
        Checks that DELETE nurses_patient_profile return correct status code if given a wrong address
        '''
        print self.test_delete_unexisting_patient.__doc__
        resp = self.client.delete(self.url_wrong)
        self.assertEquals(resp.status_code, 404)

#@unittest.skip("showing class skipping")
class MedicationListTestCase (ResourcesAPITestCase):
   
    url = '/hospital/api/nurses/nur-0/patients/pat-1/medication/'
    new_medicament = {u"name":u"aspirina", u"dosage":u"1 pastilla", u"duration":u"1 day",u"hours":u"4 hours", u"bag volume":u"100gr",u"administration":u"oral",u"patient id":0}
    new_medicament_wrong = {u"name":u"tirita"}
    
    @classmethod
    def setUpClass(cls):
        print 'Testing MedicationListTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        print self.test_url.__doc__
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Patient_medication_list)
    
    def test_get_medicaments(self):
        '''
        Checks that GET patient_medication_list return correct status code and data format
        '''
        print self.test_get_medicaments.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url, data=json.dumps(self.url),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
            self.assertEquals(resp.status_code,200)
            data = json.loads(resp.data)
            link = data['link']
            self.assertEquals(link['title'],'patient')
            self.assertEquals(link['rel'],'related')
            self.assertEquals(link['href'],resources.api.url_for(resources.Nurses_patient_profile,nurseid='nur-0',patientid='pat-1'))
            medicaments_list = data['patient_medication_list']
            self.assertEquals(len(medicaments_list),3)
            med0 = medicaments_list [0]
            self.assertIn('name',med0)
            link0 = med0['link']
            self.assertIn(resources.api.url_for(resources.Patient_medication,nurseid='nur-0',patientid='pat-1',medicamentid='med-0'),link0['href'])

    def test_add_medicament(self):
        '''
        Checks that the medicament is added correctly
        '''
        print '('+self.test_add_medicament.__name__+')', self.test_add_medicament.__doc__
        resp = self.client.post(self.url,
                                data=json.dumps(self.new_medicament),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 201)
        self.assertIn('Location', resp.headers)
        medicament_url = resp.headers['Location']
        resp2 = self.client.get(medicament_url,
                                data=json.dumps(self.new_medicament),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 200)

    def test_add_medicament_wrong(self):
        '''
        Try to add a medicament with wrong format
        '''
        print '('+self.test_add_medicament_wrong.__name__+')', self.test_add_medicament_wrong.__doc__
        resp = self.client.post(self.url,
                                data=json.dumps(self.new_medicament_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 400)

#@unittest.skip("showing class skipping")
class MedicamentTestCase (ResourcesAPITestCase):
    
    url = '/hospital/api/nurses/nur-0/patients/pat-1/medication/med-0/'
    url_wrong = '/hospital/api/nurses/nur-0/patients/pat-1/medication/med-45/'
    med_1_request = {u"id":u"med-0", u"name":u"aspirina", u"dosage":u"1 pastilla", u"duration":u"1 day",u"hours":u"4 hours", u"bag volume":u"100gr",u"administration":u"oral"}
    med_1_request_wrong = {u"id":u"med-394"}

    @classmethod
    def setUpClass(cls):
        print 'Testing MedicamentTestCase'
    
    def test_url(self):
        '''
        Checks that the URL points to the right resource
        '''
        print self.test_url.__doc__
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Patient_medication)
    
    def test_wrong_url(self):
        '''
        Checks that GET patient_medication return correct status code if given a wrong url
        '''
        resp = self.client.get(self.url_wrong,
                                data=json.dumps(self.url_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 404)
    
    def test_get_medicament(self):
        '''
        Checks that GET patient_medication return correct status code and data format
        '''
        print self.test_get_medicament.__doc__
        with resources.app.test_client() as client:
            resp = client.get(self.url, data=json.dumps(self.med_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
            self.assertEquals(resp.status_code ,200)
            data = json.loads(resp.data)
            medicament = data ['medicament']
            for attribute in ('id','name', 'dosage','duration', 'hours', 'bag volume', 'administration'):
                self.assertIn(attribute, medicament)

    def test_modify_medicament(self):
        '''
        Modify an exsiting medicament and check that the medicament has been modified correctly in the server
        '''
        print self.test_modify_medicament.__doc__
        resp = self.client.put(self.url,
                                data=json.dumps(self.med_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url,
                                data=json.dumps(self.med_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 200)
        data = json.loads(resp2.data)
        self.assertDictContainsSubset(self.med_1_request, data['medicament'])
        
    def test_modify_wrong_medicament(self):
        '''
        Try to modify a medicament with wrong format
        '''
        print self.test_modify_wrong_medicament.__doc__
        resp = self.client.put(self.url,
                                data=json.dumps(self.med_1_request_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 400)

    def test_modify_unexisting_medicament(self):
        '''
        Try to modify an unexisting medicament
        '''
        print self.test_modify_unexisting_medicament.__doc__
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.med_1_request_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 404)

    def test_delete_medicament(self):
        '''
        Checks that DELETE patient_medication return correct status code if corrected delete
        '''
        print self.test_delete_medicament.__doc__
        resp = self.client.delete(self.url,
                                data=json.dumps(self.med_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 204)
        resp2 = self.client.get(self.url,
                                data=json.dumps(self.med_1_request),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp2.status_code, 404)

    def test_delete_unexisting_medicament(self):
        '''
        Checks that DELETE patient_medication return correct status code if given a wrong address
        '''
        print self.test_delete_unexisting_medicament.__doc__
        resp = self.client.delete(self.url_wrong,
                                data=json.dumps(self.med_1_request_wrong),
                                headers={"Content-Type":"application/json", 'Authorization':'Admin'})
        self.assertEquals(resp.status_code, 404)
   
if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()