from copy import deepcopy
import sqlite3
import sys
import re
import os

class HospitalDatabaseInterface(object):
    '''
    Interface to access the database. The structure of input and output depends
    on the implementation. User and Model are data structures (dictionaries or 
    customized objects)
    '''
    
    def clean(self):
        '''
        Clean the database
        '''
        raise NotImplementedError("")

    def load_init_values(self):
        '''
        Load default values in the database. Create tables and load testing
        values.
        ''' 
        raise NotImplementedError("")
    
    # NURSES
    def get_nurse(self, nurseid):
        '''
        Return a nurse with id equals nurseid or None if there is no 
        such nurse. Raises a value error if nurseid is not well formed.
        '''
        raise NotImplementedError("")

    def get_nurses_list(self):
        '''
        Return a list of all the nurses.
        '''
        raise NotImplementedError("")

    def modify_nurse(self, nurseid, nursename, nursesurname, nursepn, nurseaddress):
        '''
        Modify the data of the nurse with id=nurseid.
        raises HospitalDatabaseError if the database could not be modified.
        raises ValueError if the nurseid has a wrong format.
        returns the id of the edited nurse or None if the nurse was not found.
        '''
        raise NotImplementedError("")

    def append_nurse(self, nursename, nursesurname, nursepn, nurseaddress):
        '''
        Creates a new nurse.
        raises HospitalDatabaseError if the if the database could not be modified.
        raises ValueError if the nurseid has a wrong format.
        returns the id of the new nurse or None if nurseid does not exist.
        '''
        raise NotImplementedError("")

    def delete_nurse(self, nurseid):
        '''
        Deletes the nurse that has the id passed as argument. Returns the
        id of the deleted nurse or None if the nurse was not found.
        '''
        raise NotImplementedError("")

    def contains_nurse (self, nurseid):
        '''
        Returns true if the nurse is in the database. False otherwise.
        '''
        raise NotImplementedError("")

    # PATIENTS
    def get_patient(self, patientid):
        '''
        Return a patient with id equals patientid or None if there is no 
        such patient. Raises a value error if patientid is not well formed.
        '''
        raise NotImplementedError("")

    def get_nurses_patient_list(self, nurseid):
        '''
        Return a list of all the patients of the nurse with Id=nurseid.
        '''
        raise NotImplementedError("")

    def modify_patients(self, patientid, patientname, patientsurname, patientroom, patientpn, patientaddress):
        '''
        Modify the data of the patient with id=patientid.
        raises HospitalDatabaseError if the database could not be modified.
        raises ValueError if the patientid has a wrong format.
        returns the id of the edited patient or None if the patient was not found.
        '''
        raise NotImplementedError("")

    def delete_patient(self, patientid):
        '''
        Deletes the patient that has the id passed as argument. Returns the
        id of the deleted patient or None if the patient was not found.
        '''
        raise NotImplementedError("")

    def contains_patient (self, patientid):
        '''
        Returns true if the patient is in the database. False otherwise.
        '''
        raise NotImplementedError("")

    # MEDICAMENTS
    def get_medicament(self, medicamentid):
        '''
        Return a medicament with id equals medicamentid or None if there is no 
        such medicament. Raises a value error if medicamentid is not well formed.
        '''
        raise NotImplementedError("")

    def get_patient_medication_list(self, patientid):
        '''
        Return a list of all the medicaments of the patient with Id=patientid.
        '''
        raise NotImplementedError("")

    def modify_medicament(self, medid, medname, meddosage, medduration, medhours, medbag, medadmin):
        '''
        Modify the data of the medicament with id=medicamentid.
        raises HospitalDatabaseError if the database could not be modified.
        raises ValueError if the medicamentid has a wrong format.
        returns the id of the edited medicament or None if the medicament was not found.
        '''
        raise NotImplementedError("")

    def append_medication(self, medname, meddosage, medduration, medhours, medbag, medadmin, medpatient):
        '''
        Creates a new medicament.
        raises HospitalDatabaseError if the if the database could not be modified.
        raises ValueError if the medicamentid has a wrong format.
        returns the id of the new medicament or None if medicamentid does not exist.
        '''
        raise NotImplementedError("")

    def delete_medicament(self, medicamentid):
        '''
        Deletes the medicament that has the id passed as argument. Returns the
        id of the deleted medicament or None if the medicament was not found.
        '''
        raise NotImplementedError("")

    def contains_medicament(self, medicamentid):
        '''
        Returns true if the medicament is in the database. False otherwise.
        '''
        raise NotImplementedError("")

class HospitalNonPersistentDatabase(HospitalDatabaseInterface):

    NURSES = {}

    PATIENTS = {}

    MEDICAMENTS = {}

    def __init__(self):
        super(HospitalNonPersistentDatabase, self).__init__()

    def clean(self):
        self.NURSES.clear()
        self.PATIENTS.clear()
        self.MEDICAMENTS.clear()

    def load_init_values(self):
        nurse0_id = "nur-0"
        nurse_0 = {"id":nurse0_id, "name":"Mateo","surname":"Gil","phone number":987654321,"address":"Bahia Pikachu N 4"}

        nurse1_id = "nur-1"
        nurse_1 = {"id":nurse1_id, "name":"Jussi","surname":"Hiltunen","phone number":92345678,"address":"Roca Geodude N 404"}
    
        patient0_id = "pat-0"
        patient_0 = {"id":patient0_id,"name":"Juan Carlos", "surname":"Primero","room":1408,"phone number":1,"address":"Palacio de la Zarzuela","nurse id":nurse1_id,"doctor id":"doc-1"}
    
        patient1_id = "pat-1"
        patient_1 = {"id":patient1_id,"name":"Duquesa", "surname":"de Alba","room":2402,"phone number":0,"address":"Casa de Alba","nurse id":nurse0_id,"doctor id":"doc-1"}

        medicament0_id = "med-0"
        medicament_0 = {"id":medicament0_id,"name":"Paracetamol", "dosage":"1gr","duration":"1 week","hours":"every 8 hours","bag volume":"100 ml","administration":"intravenous","patient id":patient1_id}
    
        medicament1_id = "med-1"
        medicament_1 = {"id":medicament1_id,"name":"Betadine", "dosage":"20ml","duration":"2 days","hours":"every 6 hours","bag volume":"150 ml","administration":"cutaneous","patient id":patient1_id}

        self.NURSES[nurse0_id] = nurse_0
        self.NURSES[nurse1_id] = nurse_1
        self.PATIENTS[patient0_id] = patient_0
        self.PATIENTS[patient1_id] = patient_1
        self.MEDICAMENTS[medicament0_id] = medicament_0
        self.MEDICAMENTS[medicament1_id] = medicament_1
    
        self.lastnurse = 2
        self.lastmedicament = 2

    # NURSES
    def get_nurse(self, nurseid):
        # Make a copy in case the caller wants to modify it
        return deepcopy(self.NURSES.get(nurseid))
            
    def get_nurses_list(self):
        # Get the list of nurses
        return self.NURSES.values()

    def modify_nurse(self, nurseid, nursename, nursesurname, nursepn, nurseaddress):
        nurse = self.NURSES.get(nurseid)
        if nurse:
            nurse["name"] = nursename
            nurse["surname"] = nursesurname
            nurse["phone number"] = nursepn
            nurse["address"] = nurseaddress
        return nurseid if nurse else None
            
    def append_nurse(self, nursename, nursesurname, nursepn, nurseaddress):
        # Check that the nurseid exist otherwise return None
        global lastnurse
        newid = "nur-"+ str(lastnurse)
        lastnurse += 1 
        nurse = {"id":newid,"name":nursename, "surname":nursesurname, "phone number":nursepn, "address": nurseaddress}
        self.NURSES[newid] = nurse
        return newid

    def delete_nurse(self, nurseid):
        nurse = self.NURSES.pop(nurseid, None)
        return nurseid if nurse else None

    def contains_nurse (self, nurseid):
        return self.NURSES.get(nurseid, None) is not None

    # PATIENTS
    def get_patient(self, patientid):
        # Make a copy in case the caller wants to modify it
        return deepcopy(self.PATIENTS.get(patientid))
            
    def get_nurses_patient_list(self, nurseid):
        # Get the list of the patients of a nurse
        patient_list = []
        patient_list = [patient for patient in self.PATIENTS.values() if patient.get("nurse id") == nurseid]
        return patient_list

    def modify_patient(self, patientid, patientname, patientsurname, patientroom, patientpn, patientaddress):
        patient = self.PATIENTS.get(patientid)
        if patient:
            patient["name"] = patientname
            patient["surname"] = patientsurname
            patient["room"] = patientroom
            patient["phone number"] = patientpn
            patient["address"] = patientaddress
        return patientid if patient else None

    def delete_patient(self, patientid):
        patient = self.PATIENTS.pop(patientid, None)
        return patientid if patient else None

    def contains_patient (self, patientid):
        return self.PATIENTS.get(patientid, None) is not None

    # MEDICAMENTS
    def get_medicament(self, medicamentid):
        # Make a copy in case the caller wants to modify it
        return deepcopy(self.MEDICAMENTS.get(medicamentid))
            
    def get_patient_medication_list(self, patientid):
        # Get the list of the medication of a patient
        medication_list = []
        medication_list = [medicament for medicament in self.MEDICAMENTS.values() if medicament.get("patient id") == patientid]
        return medication_list

    def modify_medicament(self, medid, medname, meddosage, medduration, medhours, medbag, medadmin):
        medicament = self.MEDICAMENTS.get(medid)
        if medicament:
            medicament["name"] = medname
            medicament["dosage"] = meddosage
            medicament["duration"] = medduration
            medicament["hours"] = medhours
            medicament["bag volume"] = medbag
            medicament["administration"] = medadmin
        return medid if medicament else None
            
    def append_medication(self, medname, meddosage, medduration, medhours, medbag, medadmin, medpatient):
        # Check that the nurseid exist otherwise return None
        global lastmedicament
        newid = "med-" + str(lastmedicament)
        lastmedicament += 1 
        medicament = {"id": newid, "name": medname, "dosage": meddosage, "duration": medduration, "hours": medhours, "bag volume": medbag, "administration": medadmin, "patient id": medpatient}
        self.MEDICAMENTS[newid] = medicament
        return newid

    def delete_medicament(self, medicamentid):
        medicament = self.MEDICAMENTS.pop(medicamentid, None)
        return medicamentid if medicament else None

    def contains_medicament(self, medicamentid):
        return self.MEDICAMENTS.get(medicamentid, None) is not None


class HospitalDatabase(HospitalDatabaseInterface):
    '''
    This class defines the interface for a persistent database.
    '''
    def __init__(self, db_path):
        super(HospitalDatabase, self).__init__()
        self.db_path = db_path

    # SETUP AND DELETE THE DATABASE
    def clean(self):
        '''
        Clean the database
        '''
        os.remove(self.db_path)

    def load_init_values(self):
        '''
        Load default values in the database. Create tables and load testing
        values.
        ''' 
        self.create_tables_from_dump()
        self.load_table_values_from_dump()

    # MANAGING THE CONNECTIONS:
    def check_foreign_keys_status(self):
        '''
        Checks the status of foreign keys
        '''
        con = None
        try:
            # Connects to the database.
            con = sqlite3.connect(self.db_path)
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            # Execute the pragma command
            cur.execute('PRAGMA foreign_keys')
            # I know I retrieve just one record: use fetchone()
            data = cur.fetchone()
            data_text = 'ON' if data == (1,) else 'OFF'            
            print "Foreign Keys status: %s" % data_text                
            
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
            
        finally:
            if con:
                con.close()
        return data

    def set_and_check_foreign_keys_status(self):
        '''
        Sets and checks the status of foreign keys
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        con = None
        try:
            # connects to the database.
            con = sqlite3.connect(self.db_path)
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            # execute the pragma command, ON
            cur.execute(keys_on)
            # execute the pragma check command
            cur.execute('PRAGMA foreign_keys')
            # I know I retrieve just one record: use fetchone()
            data = cur.fetchone()
            data_text = 'ON' if data == (1,) else 'OFF'            
            print "Foreign Keys status: %s" % data_text
            
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
            
        finally:
            if con:
                con.close()
        return data

    # CREATE THE TABLES
    def create_nurses_profile_table(self):
        '''creates nurses_profile table'''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE nurses_profile(nurse_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, phone_number INTEGER, address TEXT)' 
        con = sqlite3.connect(self.db_path)
        with con:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                # execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, e:
                print "Error %s:" % e.args[0]
        return None
        
    def create_doctors_profile_table(self):
        '''creates doctors_profile table'''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE doctors_profile(doctor_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, phone_number INTEGER, address TEXT)' 
        con = sqlite3.connect(self.db_path)
        with con:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)
                # execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, e:
                print "Error %s:" % e.args[0]
        return None

    def create_patients_profile_table(self):
        '''creates patients_profile table'''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE patients_profile(patient_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, room INTEGER,\
                            phone_number INTEGER, address TEXT, p_nurse INTEGER, p_doctor INTEGER,\
                            FOREIGN KEY(p_nurse) REFERENCES nurses_profile(nurse_id) ON DELETE CASCADE\
                            FOREIGN KEY(p_doctor) REFERENCES doctors_profile(doctor_id) ON DELETE CASCADE)'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = con.cursor()
            try:
                cur.execute(keys_on)        
                # execute the statement
                cur.execute(stmnt)
            except sqlite3.Error,e:
                print "Error %s:" % e.args[0]
        return None
    
    def create_medicaments_table(self):
        """creates medicaments table"""
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE medicaments(medicament_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, dosage TEXT, duration TEXT, hours TEXT,\
                            bag_volume TEXT, administration TEXT, m_patient INTEGER, \
                            FOREIGN KEY(m_patient) REFERENCES patients_profile(patient_id) ON DELETE CASCADE)'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Get the cursor object.
            # It allows to execute SQL code and traverse the result set
            cur = con.cursor() 
            try:
                cur.execute(keys_on)        
                # execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, e:
                print "Error %s:" % e.args[0]
        return None

    def create_all_tables(self):
        '''
        Create all tables programmatically
        '''
        self.create_nurses_profile_table()
        self.create_doctors_profile_table()
        self.create_patients_profile_table()
        self.create_medicaments_table()

    def create_tables_from_dump(self):
        '''
        Create programmatically the tables from a dump file
        '''
        con = sqlite3.connect(self.db_path)
        with open('db/hospital_schema_dump.sql') as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)

    def load_table_values_from_dump(self):
        '''
        Fill programmatically the tables from a dump file
        '''
        con = sqlite3.connect(self.db_path)
        with open('db/hospital_data_dump.sql') as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)

    # RETURN OBJECTS

    def create_nurse_object(self, row):
        '''
        It takes a database Row for a nurse and transform it into a dictionary.
        '''
        nurse_id = 'nur-' + str(row['nurse_id'])
        nurse_name = row['name']
        nurse_surname = row['surname']
        nurse_phone_number = row['phone_number']
        nurse_address = row['address']
        nurse = {'id': nurse_id, 'name': nurse_name, 'surname': nurse_surname, 'phone number': nurse_phone_number, 'address': nurse_address}
        return nurse

    def create_doctor_object(self, row):
        '''
        It takes a database Row for a doctor and transform it into a dictionary.
        '''
        doctor_id = 'doc-' + str(row['doctor_id'])
        doctor_name = row['name']
        doctor_surname = row['surname']
        doctor_phone_number = row['phone_number']
        doctor_address = row['address']
        doctor = {'id': doctor_id, 'name': doctor_name, 'surname': doctor_surname, 'phone number': doctor_phone_number, 'address': doctor_address}
        return doctor

    def create_patient_object(self, row):
        '''
        It takes a database Row for a patient and transform it into a dictionary.
        '''
        patient_id = 'pat-' + str(row['patient_id'])
        patient_name = row['name']
        patient_surname = row['surname']
        patient_room = row['room']
        patient_phone_number = row['phone_number']
        patient_address = row['address']
        patient_nurse = 'nur-' + str(row['p_nurse'])
        patient_doctor = 'doc-' + str(row['p_doctor'])
        patient = {'id': patient_id, 'name': patient_name, 'surname': patient_surname, 'room': patient_room , 'phone number': patient_phone_number, 'address': patient_address, 'nurse id': patient_nurse, 'doctor id': patient_doctor}
        return patient

    def create_medicament_object(self, row):
        '''
        It takes a database Row for a medicament and transform it into a dictionary.
        '''
        medicament_id = 'med-' + str(row['medicament_id'])
        medicament_name = row['name']
        medicament_dosage = row['dosage']
        medicament_duration = row['duration']
        medicament_hours = row['hours']
        medicament_bag_volume = row['bag_volume']
        medicament_administration = row['administration']
        medicament_patient = 'pat-' + str(row['m_patient'])
        medicament = {'id': medicament_id, 'name': medicament_name, 'dosage': medicament_dosage, 'duration': medicament_duration, 'hours': medicament_hours, 'bag volume': medicament_bag_volume, 'administration': medicament_administration, 'patient id': medicament_patient}
        return medicament
    
    # NURSE
    def get_nurse(self, nurseid):
        '''
        Return a Nurse given its id (nurseid) or None if there is no 
        such nurse. Raises a value error if nurseid is not well formed.
        nurseid format: nur-\d{1,3}
        '''
        # Extracts the int which is the id for a nurse in the database
        match = re.match(r'nur-(\d{1,3})', nurseid)
        if match is None:
            raise ValueError("The nurseid is malformed")
        nurseid = int(match.group(1))

        # Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM nurses_profile WHERE nurse_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute main SQL Statement
            pvalue = (nurseid,)
            cur.execute(query, pvalue)
            # Process the response.
            # Just one row is expected
            row = cur.fetchone()
            if row is None:
                return None
            # Build the return object
            return self.create_nurse_object(row)
            
    def get_nurses_list(self):
        '''
        Return a list of all the nurses.
        '''
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM nurses_profile'
        # Connects to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query)
            # Get results
            rows = cur.fetchall()
            if rows is None:
                return None
            # Build the return object
            nurses = []    
            for row in rows:
                nurse = self.create_nurse_object(row)
                nurses.append(nurse)
            return nurses

    def modify_nurse(self, nurseid, nursename, nursesurname, nursepn, nurseaddress):
        '''
        Modify the information of the nurse with id=nurseid
        raises HospitalDatabaseError if the DB could not be modified.
        raises ValueError if the nurseid has a wrong format
        returns the id of the edited nurse or None if the nurse was 
        not found
        '''
        # Extracts the int which is the id for a nurse in the database
        match = re.match(r'nur-(\d{1,3})', nurseid)
        if match is None:
            raise ValueError("The nurseid is malformed")
        nurseid = int(match.group(1))
        
        # SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement to update the user_profile table
        query = 'UPDATE nurses_profile SET name = ?,surname = ?, phone_number = ?, address = ?\
                                           WHERE nurse_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute the statement to extract the id associated to a nickname
            pvalue = (nursename, nursesurname, nursepn, nurseaddress, nurseid)
            cur.execute(query, pvalue)
            # Extract the id of the added nurse
            if cur.rowcount < 1:
                return None
            return 'nur-' + str(nurseid)
            
    def append_nurse(self, nursename, nursesurname, nursepn, nurseaddress):
        '''
        Create a new nurse. 
        raises HospitalDatabaseError if the DB could not be modified.
        raises ValueError if the nurse_id has a wrong format
        returns the id of the new nurse or None if it could not be created
        '''
        # SQL STATMENTS FOR KEYS
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement for inserting the data
        stmnt = 'INSERT INTO nurses_profile (name,surname,phone_number,address)\
                         VALUES(?,?,?,?)'
        # Connects  to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Extract nurse id
            row = cur.fetchone()
            if row is not None:
                nurse_id = 'nur-' + str(row["nurse_id"])
            # Generate the values for SQL statement
            pvalue = (nursename,nursesurname,nursepn,nurseaddress)
            cur.execute(stmnt,pvalue)
            # Extract the id of the added nurse
            lid = cur.lastrowid
            # Return the id in
            return 'nur-' + str(lid) if lid is not None else None
    
    def delete_nurse(self, nurseid):
        '''
        Delete a nurse in the Hospital.
        raises ValueError if the nurseId has a wrong format
        return True if the nurse has been deleted False otherwise
        '''
        # Extracts the int which is the id for a nurse in the database
        match = re.match(r'nur-(\d{1,3})', nurseid)
        if match is None:
            raise ValueError("The nurseid is malformed")
        nurseid = int(match.group(1))
        
        # SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement for deleting the user information
        query = 'DELETE FROM nurses_profile WHERE nurse_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute the statement to delete
            pvalue = (nurseid,)
            cur.execute(query, pvalue)
            # Check that it has been deleted
            if cur.rowcount < 1:
                return False
            return True

    def contains_nurse(self, nurseid):
        '''
        Returns true if the nurse is in the database. False otherwise.
        '''
        return self.get_nurse(nurseid) is not None

    # PATIENT
    def get_patient(self, patientid):
        '''
        Return a Patient given its id (patientid) or None if there is no 
        such patient. Raises a value error if patientid is not well formed.
        patientid format: pat-\d{1,3}
        '''
        # Extracts the int which is the id for a patient in the database
        match = re.match(r'pat-(\d{1,3})', patientid)
        if match is None:
            raise ValueError("The patientid is malformed")
        patientid = int(match.group(1))

        # Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM patients_profile WHERE patient_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute main SQL Statement
            pvalue = (patientid,)
            cur.execute(query, pvalue)
            # Process the response.
            # Just one row is expected
            row = cur.fetchone()
            if row is None:
                return None
            # Build the return object
            return self.create_patient_object(row)
            
    def get_nurses_patient_list(self, nurseid):
        '''
        Return a list of all the patients.
        '''
        match = re.match(r'nur-(\d{1,3})', nurseid)
        if match is None:
            raise ValueError("The nurseid is malformed")
        nurseid = int(match.group(1))

        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM patients_profile WHERE p_nurse = ?'
        # Connects to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            pvalue = (nurseid,)        
            cur.execute(query,pvalue)
            # Get results
            rows = cur.fetchall()
            if rows is None:
                return None
            # Build the return object
            patients = []    
            for row in rows:
                patient = self.create_patient_object(row)
                patients.append(patient)
            return patients

    def modify_patient(self, patientid, patientname, patientsurname, patientroom, patientpn, patientaddress):
        '''
        Modify the information of the patient with id=patientid
        raises HospitalDatabaseError if the DB could not be modified.
        raises ValueError if the patientid has a wrong format
        returns the id of the edited patient or None if the patient was 
        not found
        '''
        # Extracts the int which is the id for a patient in the database
        match = re.match(r'pat-(\d{1,3})', patientid)
        if match is None:
            raise ValueError("The patientid is malformed")
        patientid = int(match.group(1))
        
        # SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement to update the user_profile table
        query = 'UPDATE patients_profile SET name = ?,surname = ?, room = ?, phone_number = ?, address = ?\
                                           WHERE patient_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute the statement to extract the id associated to a nickname
            pvalue = (patientname, patientsurname, patientroom, patientpn, patientaddress, patientid)
            cur.execute(query, pvalue)
            # Extract the id of the added patient
            if cur.rowcount < 1:
                return None
            return 'pat-' + str(patientid)
    
    def delete_patient(self, patientid):
        '''
        Delete a patient in the Hospital.
        raises ValueError if the patientId has a wrong format
        return True if the patient has been deleted False otherwise
        '''
        # Extracts the int which is the id for a patient in the database
        match = re.match(r'pat-(\d{1,3})', patientid)
        if match is None:
            raise ValueError("The patientid is malformed")
        patientid = int(match.group(1))
        
        # SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement for deleting the user information
        query = 'DELETE FROM patients_profile WHERE patient_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute the statement to delete
            pvalue = (patientid,)
            cur.execute(query, pvalue)
            # Check that it has been deleted
            if cur.rowcount < 1:
                return False
            return True

    def contains_patient (self, patientid):
        '''
        Returns true if the patient is in the database. False otherwise.
        '''
        return self.get_patient(patientid) is not None

    # MEDICAMENT
    def get_medicament(self, medicamentid):
        '''
        Return a Medicament given its id (medicamentid) or None if there is no 
        such medicament. Raises a value error if medicamentid is not well formed.
        medicamentid format: med-\d{1,3}
        '''
        # Extracts the int which is the id for a medicament in the database
        match = re.match(r'med-(\d{1,3})', medicamentid)
        if match is None:
            raise ValueError("The medicamentid is malformed")
        medicamentid = int(match.group(1))

        # Create the SQL Query
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM medicaments WHERE medicament_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute main SQL Statement
            pvalue = (medicamentid,)
            cur.execute(query, pvalue)
            # Process the response.
            # Just one row is expected
            row = cur.fetchone()
            if row is None:
                return None
            # Build the return object
            return self.create_medicament_object(row)
            
    def get_patient_medication_list(self, patientid):
        '''
        Return a list of all the medicaments of a patient.
        '''
        match = re.match(r'pat-(\d{1,3})', patientid)
        if match is None:
            raise ValueError("The patientid is malformed")
        patientid = int(match.group(1))

        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM medicaments WHERE m_patient = ?'
        # Connects to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            pvalue = (patientid,)        
            cur.execute(query, pvalue)
            # Get results
            rows = cur.fetchall()
            if rows is None:
                return None
            # Build the return object
            medicaments = []
            for row in rows:
                medicament = self.create_medicament_object(row)
                medicaments.append(medicament)
            return medicaments

    def modify_medicament(self, medicamentid, medicamentname, medicamentdosage, medicamentduration, medicamenthours, medicamentbag, medicamentadministration):
        '''
        Modify the information of the medicament with id=medicamentid
        raises HospitalDatabaseError if the DB could not be modified.
        raises ValueError if the medicamentid has a wrong format
        returns the id of the edited medicament or None if the medicament was 
        not found
        '''
        # Extracts the int which is the id for a medicament in the database
        match = re.match(r'med-(\d{1,3})', medicamentid)
        if match is None:
            raise ValueError("The medicamentid is malformed")
        medicamentid = int(match.group(1))
        
        # SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement to update the user_profile table
        query = 'UPDATE medicaments SET name = ?,dosage = ?, duration = ?, hours = ?, bag_volume = ?, administration = ?\
                                           WHERE medicament_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute the statement to extract the id associated to a nickname
            pvalue = (medicamentname, medicamentdosage, medicamentduration, medicamenthours, medicamentbag, medicamentadministration, medicamentid)
            cur.execute(query, pvalue)
            # Extract the id of the added medicament
            if cur.rowcount < 1:
                return None
            return 'med-' + str(medicamentid)
            
    def append_medication(self, medicamentname, medicamentdosage, medicamentduration, medicamenthours, medicamentbag, medicamentadministration, medicamentpatient):
        '''
        Create a new medicament. 
        raises HospitalDatabaseError if the DB could not be modified.
        raises ValueError if the medicament_id has a wrong format
        returns the id of the new medicament or None if it could not be created
        '''
        # SQL STATMENTS FOR KEYS
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement for inserting the data
        stmnt = 'INSERT INTO medicaments (name,dosage,duration,hours,bag_volume,administration,m_patient)\
                         VALUES(?,?,?,?,?,?,?)'
        # Connects  to the database.
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Extract medicament id
            row = cur.fetchone()
            if row != None:
                medicament_id = 'med-' + str(row["medicament_id"])
            # Generate the values for SQL statement
            pvalue = (medicamentname,medicamentdosage,medicamentduration,medicamenthours,medicamentbag,medicamentadministration,medicamentpatient)
            cur.execute(stmnt,pvalue)
            # Extract the id of the added medicament
            lid = cur.lastrowid
            # Return the id in
            return 'med-' + str(lid) if lid is not None else None
    
    def delete_medicament(self, medicamentid):
        '''
        Delete a medicament in the Hospital.
        raises ValueError if the medicamentId has a wrong format
        return True if the medicament has been deleted False otherwise
        '''
        # Extracts the int which is the id for a medicament in the database
        match = re.match(r'med-(\d{1,3})', medicamentid)
        if match is None:
            raise ValueError("The medicamentid is malformed")
        medicamentid = int(match.group(1))
        
        # SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
        # SQL Statement for deleting the user information
        query = 'DELETE FROM medicaments WHERE medicament_id = ?'
        # Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)        
            # Execute the statement to delete
            pvalue = (medicamentid,)
            cur.execute(query, pvalue)
            # Check that it has been deleted
            if cur.rowcount < 1:
                return False
            return True

    def contains_medicament (self, medicamentid):
        '''
        Returns true if the medicament is in the database. False otherwise.
        '''
        return self.get_medicament(medicamentid) is not None
