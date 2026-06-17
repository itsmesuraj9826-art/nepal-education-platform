-- ================================================================
-- Nepal National Education Platform — MySQL Schema
-- Run: mysql -u root -p < schema.sql
-- ================================================================

CREATE DATABASE IF NOT EXISTS nepal_edu_platform
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE nepal_edu_platform;

-- ── Geography ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS provinces (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  name     VARCHAR(100) NOT NULL,
  name_np  VARCHAR(100),
  code     VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS districts (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  province_id INT NOT NULL,
  name        VARCHAR(100) NOT NULL,
  name_np     VARCHAR(100),
  code        VARCHAR(10),
  FOREIGN KEY (province_id) REFERENCES provinces(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS municipalities (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  district_id INT NOT NULL,
  name        VARCHAR(150) NOT NULL,
  name_np     VARCHAR(150),
  mun_type    VARCHAR(30),
  code        VARCHAR(10),
  FOREIGN KEY (district_id) REFERENCES districts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Schools ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS schools (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  school_code      VARCHAR(20) UNIQUE NOT NULL,
  emis_id          VARCHAR(30) UNIQUE,
  name_en          VARCHAR(255) NOT NULL,
  name_np          VARCHAR(255),
  school_type      VARCHAR(50),
  school_level     VARCHAR(50),
  academic_streams TEXT,
  province_id      INT,
  district_id      INT,
  municipality_id  INT,
  ward_number      INT,
  address          TEXT,
  latitude         DOUBLE,
  longitude        DOUBLE,
  phone            VARCHAR(20),
  email            VARCHAR(120),
  website          VARCHAR(200),
  principal_name   VARCHAR(150),
  num_teachers     INT DEFAULT 0,
  num_students     INT DEFAULT 0,
  status           VARCHAR(20) DEFAULT 'active',
  established_year INT,
  last_synced_at   DATETIME,
  data_source      VARCHAR(50),
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_school_code (school_code),
  INDEX idx_emis_id (emis_id),
  INDEX idx_province (province_id),
  INDEX idx_district (district_id),
  FOREIGN KEY (province_id) REFERENCES provinces(id),
  FOREIGN KEY (district_id) REFERENCES districts(id),
  FOREIGN KEY (municipality_id) REFERENCES municipalities(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Users ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  username         VARCHAR(80) UNIQUE NOT NULL,
  email            VARCHAR(120) UNIQUE NOT NULL,
  password_hash    VARCHAR(255) NOT NULL,
  full_name        VARCHAR(150),
  phone            VARCHAR(20),
  role             VARCHAR(30) NOT NULL DEFAULT 'teacher',
  province_id      INT,
  district_id      INT,
  municipality_id  INT,
  school_id        INT,
  is_active        TINYINT(1) DEFAULT 1,
  last_login       DATETIME,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (school_id) REFERENCES schools(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Teachers ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS teachers (
  id                       INT AUTO_INCREMENT PRIMARY KEY,
  teacher_id               VARCHAR(30) UNIQUE NOT NULL,
  govt_employee_no         VARCHAR(30) UNIQUE,
  first_name               VARCHAR(80) NOT NULL,
  last_name                VARCHAR(80) NOT NULL,
  gender                   VARCHAR(10),
  date_of_birth            DATE,
  citizenship_no           VARCHAR(30),
  photo_url                VARCHAR(255),
  face_encoding            TEXT,
  phone                    VARCHAR(20),
  email                    VARCHAR(120),
  permanent_address        TEXT,
  temporary_address        TEXT,
  subject_specialization   VARCHAR(150),
  highest_qualification    VARCHAR(100),
  university               VARCHAR(150),
  teaching_license_no      VARCHAR(50),
  service_start_date       DATE,
  service_type             VARCHAR(30),
  school_id                INT,
  designation              VARCHAR(80),
  tpdi_score               FLOAT DEFAULT 0,
  tpdi_category            VARCHAR(30),
  attendance_score         FLOAT DEFAULT 0,
  punctuality_score        FLOAT DEFAULT 0,
  student_performance_score FLOAT DEFAULT 0,
  is_active                TINYINT(1) DEFAULT 1,
  created_at               DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at               DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_teacher_id (teacher_id),
  FOREIGN KEY (school_id) REFERENCES schools(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS teacher_transfers (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  teacher_id     INT NOT NULL,
  from_school_id INT,
  to_school_id   INT,
  transfer_date  DATE,
  reason         TEXT,
  order_no       VARCHAR(50),
  approved_by    VARCHAR(150),
  created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (teacher_id) REFERENCES teachers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Students ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
  id                   INT AUTO_INCREMENT PRIMARY KEY,
  student_id           VARCHAR(30) UNIQUE NOT NULL,
  emis_number          VARCHAR(30) UNIQUE,
  first_name           VARCHAR(80) NOT NULL,
  last_name            VARCHAR(80) NOT NULL,
  gender               VARCHAR(10),
  date_of_birth        DATE,
  nationality          VARCHAR(30) DEFAULT 'Nepali',
  ethnicity            VARCHAR(50),
  religion             VARCHAR(50),
  photo_url            VARCHAR(255),
  father_name          VARCHAR(150),
  mother_name          VARCHAR(150),
  guardian_name        VARCHAR(150),
  guardian_phone       VARCHAR(20),
  guardian_email       VARCHAR(120),
  address              TEXT,
  school_id            INT,
  current_grade        VARCHAR(10),
  section              VARCHAR(10),
  roll_number          INT,
  academic_year        VARCHAR(10),
  dropout_risk_score   FLOAT DEFAULT 0,
  performance_trend    VARCHAR(20),
  learning_gaps        TEXT,
  is_active            TINYINT(1) DEFAULT 1,
  created_at           DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at           DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (school_id) REFERENCES schools(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS student_enrollments (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  student_id    INT NOT NULL,
  school_id     INT NOT NULL,
  grade         VARCHAR(10),
  academic_year VARCHAR(10),
  enrolled_on   DATE,
  left_on       DATE,
  left_reason   VARCHAR(150),
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (school_id)  REFERENCES schools(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Attendance ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS teacher_attendance (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  teacher_id       INT NOT NULL,
  school_id        INT NOT NULL,
  date             DATE NOT NULL,
  check_in_time    TIME,
  check_out_time   TIME,
  status           VARCHAR(20) DEFAULT 'present',
  method           VARCHAR(20),
  check_in_lat     DOUBLE,
  check_in_lon     DOUBLE,
  check_out_lat    DOUBLE,
  check_out_lon    DOUBLE,
  geo_valid        TINYINT(1) DEFAULT 1,
  fraud_flag       TINYINT(1) DEFAULT 0,
  fraud_reason     VARCHAR(255),
  fraud_score      FLOAT DEFAULT 0,
  check_in_photo   VARCHAR(255),
  face_match_score FLOAT,
  notes            TEXT,
  recorded_by      INT,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_teacher_date (teacher_id, date),
  INDEX idx_date (date),
  INDEX idx_fraud (fraud_flag),
  FOREIGN KEY (teacher_id) REFERENCES teachers(id),
  FOREIGN KEY (school_id)  REFERENCES schools(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS student_attendance (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  student_id  INT NOT NULL,
  school_id   INT NOT NULL,
  date        DATE NOT NULL,
  status      VARCHAR(20) DEFAULT 'present',
  reason      VARCHAR(255),
  recorded_by INT,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_student_date (student_id, date),
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (school_id)  REFERENCES schools(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Examinations ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS exams (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  title            VARCHAR(255) NOT NULL,
  subject          VARCHAR(100) NOT NULL,
  grade            VARCHAR(10) NOT NULL,
  academic_year    VARCHAR(10),
  exam_type        VARCHAR(50),
  difficulty       VARCHAR(20),
  total_marks      INT DEFAULT 100,
  pass_marks       INT DEFAULT 40,
  duration_minutes INT DEFAULT 180,
  exam_date        DATE,
  school_id        INT,
  created_by       INT,
  ai_generated     TINYINT(1) DEFAULT 0,
  curriculum_src   TEXT,
  status           VARCHAR(20) DEFAULT 'draft',
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (school_id)  REFERENCES schools(id),
  FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS questions (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  exam_id       INT NOT NULL,
  question_no   INT,
  question_type VARCHAR(30),
  question_text TEXT NOT NULL,
  options       TEXT,
  correct_answer TEXT,
  marks         FLOAT DEFAULT 1,
  difficulty    VARCHAR(20),
  chapter       VARCHAR(150),
  topic         VARCHAR(150),
  bloom_level   VARCHAR(30),
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS exam_papers (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  exam_id        INT NOT NULL,
  paper_url      VARCHAR(255),
  answer_key_url VARCHAR(255),
  generated_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (exam_id) REFERENCES exams(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS student_results (
  id                INT AUTO_INCREMENT PRIMARY KEY,
  student_id        INT NOT NULL,
  exam_id           INT NOT NULL,
  school_id         INT,
  marks_obtained    FLOAT,
  total_marks       FLOAT,
  percentage        FLOAT,
  grade             VARCHAR(5),
  rank_in_class     INT,
  ai_evaluated      TINYINT(1) DEFAULT 0,
  evaluator_id      INT,
  remarks           TEXT,
  subject_breakdown TEXT,
  created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_student (student_id),
  INDEX idx_exam    (exam_id),
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (exam_id)    REFERENCES exams(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS answer_sheets (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  result_id      INT NOT NULL,
  image_urls     TEXT,
  ocr_text       LONGTEXT,
  ai_marks_json  TEXT,
  ocr_confidence FLOAT,
  processed_at   DATETIME,
  created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (result_id) REFERENCES student_results(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Audit Log ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_logs (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  user_id     INT,
  action      VARCHAR(50) NOT NULL,
  entity_type VARCHAR(50),
  entity_id   INT,
  old_value   LONGTEXT,
  new_value   LONGTEXT,
  ip_address  VARCHAR(45),
  user_agent  VARCHAR(255),
  notes       TEXT,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_created (created_at),
  INDEX idx_action  (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Seed: 7 Provinces of Nepal ───────────────────────────
INSERT IGNORE INTO provinces (id, name, name_np, code) VALUES
  (1, 'Koshi Province',       'कोशी प्रदेश',        'P1'),
  (2, 'Madhesh Province',     'मधेश प्रदेश',        'P2'),
  (3, 'Bagmati Province',     'बागमती प्रदेश',      'P3'),
  (4, 'Gandaki Province',     'गण्डकी प्रदेश',      'P4'),
  (5, 'Lumbini Province',     'लुम्बिनी प्रदेश',    'P5'),
  (6, 'Karnali Province',     'कर्णाली प्रदेश',     'P6'),
  (7, 'Sudurpashchim Province','सुदूरपश्चिम प्रदेश', 'P7');

-- ── Default admin user (password: Admin@1234) ────────────
-- Change immediately after first login!
INSERT IGNORE INTO users (username, email, password_hash, full_name, role) VALUES
  ('admin', 'admin@nepal-edu.gov.np',
   'pbkdf2:sha256:600000$placeholder$hash_change_on_first_run',
   'System Administrator', 'federal');
