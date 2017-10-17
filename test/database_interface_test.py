import unittest, sqlite3, os, copy

import hospital.database

db_path = 'db/hospital_test.db'
db = hospital.database.HospitalDatabase(db_path)

class DatabaseAPITestCase(unittest.TestCase):
   
    def setUp(self):
        if os.path.exists(db_path):
            os.remove(db_path)
        db.load_init_values()

    def tearDown(self):
        db.clean()


class NurseDbAPITestCase(DatabaseAPITestCase):
    nurse1 = {'id':'nur-1','name':'Jussi','surname':'Hiltunen','phone number':912345678,'address':'Roca Geodude N 404'}
    nurse1_id = 'nur-1'
    nurse2 = {'id':'nur-2','name':'Peter','surname':'Languila','phone number':918273645,'address':'Bajo el mar N 97'}
    nurse2_id = 'nur-2'
    no_nurse_id = 'nur-5'
    initial_size = 11

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_nurses_table_created(self):
        '''
        Checks that the table initially contains 11 nurses (check hospital_data_dump.sql)
        '''
        print '('+self.test_nurses_table_created.__name__+')', self.test_nurses_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM nurses_profile'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            nurses = cur.fetchall()
            #Assert
            self.assertEquals(len(nurses), self.initial_size)
        if con:
            con.close()

    def test_create_nurse_object (self):
        '''
        Check that the method create_nurse_object returns adequate values for the first database row.
        '''
        print '('+self.test_create_nurse_object.__name__+')', self.test_create_nurse_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM nurses_profile WHERE nurse_id = 1'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            nurse = db.create_nurse_object(row)
            self.assertDictContainsSubset(nurse,self.nurse1)

    def test_get_nurse (self):
        '''
        Test get_nurse with id nur-1 and nur-2
        '''
        print '('+self.test_get_nurse.__name__+')', self.test_get_nurse.__doc__
        #Test with an existing nurse
        nurse = db.get_nurse(self.nurse1_id)
        self.assertDictContainsSubset(nurse,self.nurse1)
        nurse = db.get_nurse(self.nurse2_id)
        self.assertDictContainsSubset(nurse,self.nurse2)

    def test_get_nurse_malformedid (self):
        '''
        Test get_nurse with id 1 (malformed)
        '''
        print '('+self.test_get_nurse_malformedid.__name__+')', self.test_get_nurse_malformedid.__doc__
        #Test with an existing nurse
        with self.assertRaises(ValueError):
            nurse = db.get_nurse('1')    

    def test_get_nurse_noexistingid (self):
        '''
        Test get_nurse with nur-5 (no-existing)
        '''
        print '('+self.test_get_nurse_noexistingid.__name__+')', self.test_get_nurse_noexistingid.__doc__
        #Test with an existing nurse
        nurse = db.get_nurse(self.no_nurse_id)
        self.assertIsNone(nurse)

    def test_get_nurses_list(self):
        '''
        Test that get_nurses_list works correctly
        '''
        print '('+self.test_get_nurses_list.__name__+')', self.test_get_nurses_list.__doc__
        nurses = db.get_nurses_list()
        #Check that the size is correct
        self.assertEquals(len(nurses), self.initial_size)
        #Iterate throug nurses and checks if the nurses with nurse1_id and nurse2_id are correct:
        for nurse in nurses:
            if nurse['id'] == self.nurse1_id:
                self.assertDictContainsSubset(nurse,self.nurse1)
            elif nurse['id'] == self.nurse2_id:
                self.assertDictContainsSubset(nurse,self.nurse2)

    def test_delete_nurse(self):
        '''
        Test that the nurse nur-1 is deleted
        '''
        print '('+self.test_delete_nurse.__name__+')', self.test_delete_nurse.__doc__
        resp = db.delete_nurse(self.nurse1_id)
        self.assertTrue(resp)
        #Check that the nurse has been really deleted throug a get
        resp2 = db.get_nurse(self.nurse1_id)
        self.assertIsNone(resp2)

    def test_delete_nurse_malformed_id(self):
        '''
        Test that trying to delete nurse with id ='1' raises an error
        '''
        print '('+self.test_delete_nurse_malformed_id.__name__+')', self.test_delete_nurse_malformed_id.__doc__
        #Test with an existing nurse
        with self.assertRaises(ValueError):
            nurse = db.delete_nurse('1') 

    def test_delete_nurse_noexistingid(self):
        '''
        Test delete_nurse with nur-5 (no-existing)
        '''
        print '('+self.test_delete_nurse_noexistingid.__name__+')', self.test_delete_nurse_noexistingid.__doc__
        #Test with an existing nurse
        resp = db.delete_nurse(self.no_nurse_id)
        self.assertFalse(resp)

    def test_modify_nurse(self):
        '''
        Test that the nurse nur-1 is modified
        '''
        print '('+self.test_modify_nurse.__name__+')', self.test_modify_nurse.__doc__
        resp = db.modify_nurse(self.nurse1_id,"new name","new surname","new phone","new address")
        self.assertEquals(resp, self.nurse1_id)
        #Get the expected modified nurse
        modified_nurse = copy.deepcopy(self.nurse1)
        modified_nurse['name'] = 'new name'
        modified_nurse['surname'] = 'new surname'
        modified_nurse['phone number'] = 'new phone'
        modified_nurse['address'] = 'new address'
        #Check that the nurse has been really modified through a get
        resp2 = db.get_nurse(self.nurse1_id)
        self.assertDictContainsSubset(resp2, modified_nurse)

    def test_modify_nurse_malformed_id(self):
        '''
        Test that trying to modify nurse with id ='1' raises an error
        '''
        print '('+self.test_modify_nurse_malformed_id.__name__+')', self.test_modify_nurse_malformed_id.__doc__
        #Test with an existing nurse
        with self.assertRaises(ValueError):
            nurse = db.modify_nurse('1', "new name", "new surname", "new phone","new address") 

    def test_modify_nurse_noexistingid(self):
        '''
        Test modify_nurse with nur-5 (no-existing)
        '''
        print '('+self.test_modify_nurse_noexistingid.__name__+')', self.test_modify_nurse_noexistingid.__doc__
        #Test with an existing nurse
        resp = db.modify_nurse(self.no_nurse_id, "new name", "new surname", "new phone","new address")
        self.assertIsNone(resp)

    def test_append_nurse(self):
        '''
        Test that a new nurse can be created
        '''
        print '('+self.test_append_nurse.__name__+')', self.test_append_nurse.__doc__
        nurseid = db.append_nurse("new name", "new surname", "new phone", "new address")
        self.assertIsNotNone(nurseid)
        #Get the expected modified nurse
        new_nurse = {}
        new_nurse['name'] = 'new name'
        new_nurse['surname'] = 'new surname'
        new_nurse['phone number'] = 'new phone'
        new_nurse['address'] = 'new address'
        #Check that the nurse has been really modified through a get
        resp2 = db.get_nurse(nurseid)
        self.assertDictContainsSubset(new_nurse, resp2)

    def test_not_contains_nurse(self):
        '''
        Check if the database does not contain a nurse with id nur-5
        '''
        print '('+self.test_contains_nurse.__name__+')', self.test_contains_nurse.__doc__
        self.assertFalse(db.contains_nurse(self.no_nurse_id))

    def test_contains_nurse(self):
        '''
        Check if the database contains nurse with id nur-1 and nur-2
        '''
        print '('+self.test_contains_nurse.__name__+')', self.test_contains_nurse.__doc__
        self.assertTrue(db.contains_nurse(self.nurse1_id))
        self.assertTrue(db.contains_nurse(self.nurse2_id))      


class PatientDbAPITestCase(DatabaseAPITestCase):
    patient0 = {'id':'pat-0','name':'Juan Carlos','surname':'Primero','room':1408,'phone number':1,'address':'Palacio de la Zarzuela','nurse id':'nur-1','doctor id':'doc-1'}
    patient0_id = 'pat-0'
    patient1 = {'id':'pat-1','name':'Duquesa', 'surname':'de Alba','room':1409,'phone number':0,'address':'Casa de Alba','nurse id':'nur-0','doctor id':'doc-1'}
    patient1_id = 'pat-1'
    no_patient_id = 'pat-5'
    initial_size = 24

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_patients_table_created(self):
        '''
        Checks that the table initially contains 24 patients(check hospital_data_dump.sql)
        '''
        print '('+self.test_patients_table_created.__name__+')', self.test_patients_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM patients_profile'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            patients = cur.fetchall()
            #Assert
            self.assertEquals(len(patients), self.initial_size)
        if con:
            con.close()

    def test_create_patient_object (self):
        '''
        Check that the method create_patient_object returns adequate values for the first database row.
        '''
        print '('+self.test_create_patient_object.__name__+')', self.test_create_patient_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM patients_profile WHERE patient_id = 0'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            patient = db.create_patient_object(row)
            self.assertDictContainsSubset(patient,self.patient0)

    def test_get_patient (self):
        '''
        Test get_patient with id pat-0 and pat-1
        '''
        print '('+self.test_get_patient.__name__+')', self.test_get_patient.__doc__
        #Test with an existing patient
        patient = db.get_patient(self.patient0_id)
        self.assertDictContainsSubset(patient,self.patient0)
        patient = db.get_patient(self.patient1_id)
        self.assertDictContainsSubset(patient,self.patient1)

    def test_get_patient_malformedid (self):
        '''
        Test get_patient with id 0 (malformed)
        '''
        print '('+self.test_get_patient_malformedid.__name__+')', self.test_get_patient_malformedid.__doc__
        #Test with an existing patient
        with self.assertRaises(ValueError):
            patient = db.get_patient('0')    

    def test_get_patient_noexistingid (self):
        '''
        Test get_patient with pat-5 (no-existing)
        '''
        print '('+self.test_get_patient_noexistingid.__name__+')', self.test_get_patient_noexistingid.__doc__
        #Test with an existing patient
        patient = db.get_patient(self.no_patient_id)
        self.assertIsNone(patient)

    def test_get_nurses_patient_list(self):
        '''
        Test that get_nurses_patient_list works correctly
        '''
        print '('+self.test_get_nurses_patient_list.__name__+')', self.test_get_nurses_patient_list.__doc__
        patients = db.get_nurses_patient_list('nur-1')
        #Check that the size is correct
        self.assertEquals(len(patients), 3)
        #Iterate throug patients and checks if the patients with patient0_id and patient1_id are correct:
        for patient in patients:
            if patient['id'] == self.patient0_id:
                self.assertDictContainsSubset(patient,self.patient0)

    def test_delete_patient(self):
        '''
        Test that the patient pat-0 is deleted
        '''
        print '('+self.test_delete_patient.__name__+')', self.test_delete_patient.__doc__
        resp = db.delete_patient(self.patient0_id)
        self.assertTrue(resp)
        #Check that the patient has been really deleted throug a get
        resp2 = db.get_patient(self.patient0_id)
        self.assertIsNone(resp2)

    def test_delete_patient_malformed_id(self):
        '''
        Test that trying to delete patient with id ='0' raises an error
        '''
        print '('+self.test_delete_patient_malformed_id.__name__+')', self.test_delete_patient_malformed_id.__doc__
        #Test with an existing patient
        with self.assertRaises(ValueError):
            patient = db.delete_patient('0') 

    def test_delete_patient_noexistingid(self):
        '''
        Test delete_patient with pat-5 (no-existing)
        '''
        print '('+self.test_delete_patient_noexistingid.__name__+')', self.test_delete_patient_noexistingid.__doc__
        #Test with an existing patient
        resp = db.delete_patient(self.no_patient_id)
        self.assertFalse(resp)

    def test_modify_patient(self):
        '''
        Test that the patient pat-0 is modified
        '''
        print '('+self.test_modify_patient.__name__+')', self.test_modify_patient.__doc__
        resp = db.modify_patient(self.patient0_id,"new name","new surname","new room","new phone","new address")
        self.assertEquals(resp, self.patient0_id)
        #Get the expected modified patient
        modified_patient = copy.deepcopy(self.patient0)
        modified_patient['name'] = 'new name'
        modified_patient['surname'] = 'new surname'
        modified_patient['room'] = 'new room'
        modified_patient['phone number'] = 'new phone'
        modified_patient['address'] = 'new address'
        #Check that the patient has been really modified through a get
        resp2 = db.get_patient(self.patient0_id)
        self.assertDictContainsSubset(resp2, modified_patient)

    def test_modify_patient_malformed_id(self):
        '''
        Test that trying to modify patient with id ='0' raises an error
        '''
        print '('+self.test_modify_patient_malformed_id.__name__+')', self.test_modify_patient_malformed_id.__doc__
        #Test with an existing patient
        with self.assertRaises(ValueError):
            patient = db.modify_patient('0', "new name", "new surname", "new room", "new phone", "new address") 

    def test_modify_patient_noexistingid(self):
        '''
        Test modify_patient with pat-5 (no-existing)
        '''
        print '('+self.test_modify_patient_noexistingid.__name__+')', self.test_modify_patient_noexistingid.__doc__
        #Test with an existing patient
        resp = db.modify_patient(self.no_patient_id, "new name", "new surname", "new room", "new phone", "new address")
        self.assertIsNone(resp)

    def test_not_contains_patient(self):
        '''
        Check if the database does not contain a patient with id pat-5
        '''
        print '('+self.test_contains_patient.__name__+')', self.test_contains_patient.__doc__
        self.assertFalse(db.contains_patient(self.no_patient_id))

    def test_contains_patient(self):
        '''
        Check if the database contains patient with id pat-0 and pat-1
        '''
        print '('+self.test_contains_patient.__name__+')', self.test_contains_patient.__doc__
        self.assertTrue(db.contains_patient(self.patient0_id))
        self.assertTrue(db.contains_patient(self.patient1_id))     


class MedicamentDbAPITestCase(DatabaseAPITestCase):
    medicament1 = {'id':'med-1','name':'Betadine','dosage':'20 ml','duration':'2 days','hours':'every 6 hours','bag volume':'150 ml','administration':'cutaneous','patient id':'pat-1'}
    medicament1_id = 'med-1'
    medicament2 = {'id':'med-2','name':'Morfina','dosage':'70 gr','duration':'5 days','hours':'every 30 minutes','bag volume':'200 ml','administration':'intravenous','patient id':'pat-0'}
    medicament2_id = 'med-2'
    no_medicament_id = 'med-5'
    initial_size = 12

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_medicaments_table_created(self):
        '''
        Checks that the table initially contains 12 medicaments (check hospital_data_dump.sql)
        '''
        print '('+self.test_medicaments_table_created.__name__+')', self.test_medicaments_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM medicaments'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            medicaments = cur.fetchall()
            #Assert
            self.assertEquals(len(medicaments), self.initial_size)
        if con:
            con.close()

    def test_create_medicament_object (self):
        '''
        Check that the method create_medicament_object returns adequate values for the first database row.
        '''
        print '('+self.test_create_medicament_object.__name__+')', self.test_create_medicament_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM medicaments WHERE medicament_id = 1'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            medicament = db.create_medicament_object(row)
            self.assertDictContainsSubset(medicament,self.medicament1)

    def test_get_medicament (self):
        '''
        Test get_medicament with id med-1 and med-2
        '''
        print '('+self.test_get_medicament.__name__+')', self.test_get_medicament.__doc__
        #Test with an existing medicament
        medicament = db.get_medicament(self.medicament1_id)
        self.assertDictContainsSubset(medicament,self.medicament1)
        medicament = db.get_medicament(self.medicament2_id)
        self.assertDictContainsSubset(medicament,self.medicament2)

    def test_get_medicament_malformedid (self):
        '''
        Test get_medicament with id 1 (malformed)
        '''
        print '('+self.test_get_medicament_malformedid.__name__+')', self.test_get_medicament_malformedid.__doc__
        #Test with an existing medicament
        with self.assertRaises(ValueError):
            medicament = db.get_medicament('1')    

    def test_get_medicament_noexistingid (self):
        '''
        Test get_medicament with med-5 (no-existing)
        '''
        print '('+self.test_get_medicament_noexistingid.__name__+')', self.test_get_medicament_noexistingid.__doc__
        #Test with an existing medicament
        medicament = db.get_medicament(self.no_medicament_id)
        self.assertIsNone(medicament)

    def test_get_patient_medication_list(self):
        '''
        Test that get_patient_medication_list works correctly
        '''
        print '('+self.test_get_patient_medication_list.__name__+')', self.test_get_patient_medication_list.__doc__
        medicaments = db.get_patient_medication_list('pat-0')
        #Check that the size is correct
        self.assertEquals(len(medicaments), 1)
        #Iterate throug medicaments and checks if the medicaments with medicament1_id and medicament2_id are correct:
        for medicament in medicaments:
            if medicament['id'] == self.medicament2_id:
                self.assertDictContainsSubset(medicament,self.medicament2)

    def test_delete_medicament(self):
        '''
        Test that the medicament pat-1 is deleted
        '''
        print '('+self.test_delete_medicament.__name__+')', self.test_delete_medicament.__doc__
        resp = db.delete_medicament(self.medicament1_id)
        self.assertTrue(resp)
        #Check that the medicament has been really deleted throug a get
        resp2 = db.get_medicament(self.medicament1_id)
        self.assertIsNone(resp2)

    def test_delete_medicament_malformed_id(self):
        '''
        Test that trying to delete medicament with id ='1' raises an error
        '''
        print '('+self.test_delete_medicament_malformed_id.__name__+')', self.test_delete_medicament_malformed_id.__doc__
        #Test with an existing medicament
        with self.assertRaises(ValueError):
            medicament = db.delete_medicament('1') 

    def test_delete_medicament_noexistingid(self):
        '''
        Test delete_medicament with med-5 (no-existing)
        '''
        print '('+self.test_delete_medicament_noexistingid.__name__+')', self.test_delete_medicament_noexistingid.__doc__
        #Test with an existing medicament
        resp = db.delete_medicament(self.no_medicament_id)
        self.assertFalse(resp)

    def test_modify_medicament(self):
        '''
        Test that the medicament med-1 is modified
        '''
        print '('+self.test_modify_medicament.__name__+')', self.test_modify_medicament.__doc__
        resp = db.modify_medicament(self.medicament1_id,"new name","new dosage","new duration","new hours","new bag","new administration")
        self.assertEquals(resp, self.medicament1_id)
        #Get the expected modified medicament
        modified_medicament = copy.deepcopy(self.medicament1)
        modified_medicament['name'] = 'new name'
        modified_medicament['dosage'] = 'new dosage'
        modified_medicament['duration'] = 'new duration'
        modified_medicament['hours'] = 'new hours'
        modified_medicament['bag volume'] = 'new bag'
        modified_medicament['administration'] = 'new administration'
        #Check that the medicament has been really modified through a get
        resp2 = db.get_medicament(self.medicament1_id)
        self.assertDictContainsSubset(resp2, modified_medicament)

    def test_modify_medicament_malformed_id(self):
        '''
        Test that trying to modify medicament with id ='1' raises an error
        '''
        print '('+self.test_modify_medicament_malformed_id.__name__+')', self.test_modify_medicament_malformed_id.__doc__
        #Test with an existing medicament
        with self.assertRaises(ValueError):
            medicament = db.modify_medicament('1',"new name","new dosage","new duration","new hours","new bag","new administration") 

    def test_modify_medicament_noexistingid(self):
        '''
        Test modify_medicament with med-5 (no-existing)
        '''
        print '('+self.test_modify_medicament_noexistingid.__name__+')', self.test_modify_medicament_noexistingid.__doc__
        #Test with an existing medicament
        resp = db.modify_medicament(self.no_medicament_id,"new name","new dosage","new duration","new hours","new bag","new administration")
        self.assertIsNone(resp)

    def test_append_medication(self):
        '''
        Test that a new medicament can be created
        '''
        print '('+self.test_append_medication.__name__+')', self.test_append_medication.__doc__
        '''
        The method append_medication will construct the 
        '''
        medicamentid = db.append_medication("new name","new dosage","new duration","new hours","new bag","new administration","0")
        self.assertIsNotNone(medicamentid)
        #Get the expected modified medicament
        new_medicament = {}
        new_medicament['name'] = 'new name'
        new_medicament['dosage'] = 'new dosage'
        new_medicament['duration'] = 'new duration'
        new_medicament['hours'] = 'new hours'
        new_medicament['bag volume'] = 'new bag'
        new_medicament['administration'] = 'new administration'
        new_medicament['patient id'] = 'pat-0'
        #Check that the medicament has been really modified through a get
        resp2 = db.get_medicament(medicamentid)
        self.assertDictContainsSubset(new_medicament, resp2)

    def test_not_contains_medicament(self):
        '''
        Check if the database does not contain a medicament with id med-5
        '''
        print '('+self.test_contains_medicament.__name__+')', self.test_contains_medicament.__doc__
        self.assertFalse(db.contains_medicament(self.no_medicament_id))

    def test_contains_medicament(self):
        '''
        Check if the database contains medicament with id med-1 and med-2
        '''
        print '('+self.test_contains_medicament.__name__+')', self.test_contains_medicament.__doc__
        self.assertTrue(db.contains_medicament(self.medicament1_id))
        self.assertTrue(db.contains_medicament(self.medicament2_id))     
if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()