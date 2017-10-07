PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS nurses_profile(
  nurse_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  surname TEXT,
  phone_number INTEGER,
  address TEXT);

CREATE TABLE IF NOT EXISTS doctors_profile(
  doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  surname TEXT,
  phone_number INTEGER,
  address TEXT);

CREATE TABLE IF NOT EXISTS patients_profile(
  patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  surname TEXT,
  room INTEGER,
  phone_number INTEGER,
  address TEXT,
  p_nurse INTEGER,
  p_doctor INTEGER,
  FOREIGN KEY(p_nurse) REFERENCES nurses_profile(nurse_id) ON DELETE CASCADE,
  FOREIGN KEY(p_doctor) REFERENCES doctors_profile(doctor_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS medicaments(
  medicament_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  dosage TEXT,
  duration TEXT,
  hours TEXT,
  bag_volume TEXT,
  administration TEXT,
  m_patient INTEGER,
  FOREIGN KEY(m_patient) REFERENCES patients_profile(patient_id) ON DELETE CASCADE);

COMMIT;
PRAGMA foreign_keys=ON;