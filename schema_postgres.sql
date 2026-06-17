-- ================================================================
-- Nepal National Education Platform — PostgreSQL Schema
-- For Vercel Postgres (or any Postgres instance)
-- Run via: psql $DATABASE_URL -f schema_postgres.sql
-- ================================================================

-- ── Geography ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS provinces (
  id      SERIAL PRIMARY KEY,
  name    VARCHAR(100) NOT NULL,
  name_np VARCHAR(100),
  code    VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS districts (
  id          SERIAL PRIMARY KEY,
  province_id INT NOT NULL REFERENCES provinces(id),
  name        VARCHAR(100) NOT NULL,
  name_np     VARCHAR(100),
  code        VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS municipalities (
  id          SERIAL PRIMARY KEY,
  district_id INT NOT NULL REFERENCES districts(id),
  name        VARCHAR(150) NOT NULL,
  name_np     VARCHAR(150),
  mun_type    VARCHAR(30),
  code        VARCHAR(10)
);

-- ── Users ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
  id              SERIAL PRIMARY KEY,
  username        VARCHAR(80)  UNIQUE NOT NULL,
  email           VARCHAR(120) UNIQUE NOT NULL,
  password_hash   VARCHAR(255) NOT NULL,
  full_name       VARCHAR(150),
  phone           VARCHAR(20),
  role            VARCHAR(30)  NOT NULL DEFAULT 'teacher',
  province_id     INT,
  district_id     INT,
  municipality_id INT,
  school_id       INT,
  is_active       BOOLEAN DEFAULT TRUE,
  last_login      TIMESTAMP,
  created_at      TIMESTAMP DEFAULT NOW(),
  updated_at      TIMESTAMP DEFAULT NOW()
);

-- ── Schools ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS schools (
  id               SERIAL PRIMARY KEY,
  school_code      VARCHAR(20) UNIQUE NOT NULL,
  emis_id          VARCHAR(30) UNIQUE,
  name_en          VARCHAR(255) NOT NULL,
  name_np          VARCHAR(255),
  school_type      VARCHAR(50),
  school_level     VARCHAR(50),
  academic_streams TEXT,
  province_id      INT REFERENCES provinces(id),
  district_id      INT REFERENCES districts(id),
  municipality_id  INT REFERENCES municipalities(id),
  ward_number      INT,
  address          TEXT,
  latitude         DOUBLE PRECISION,
  longitude        DOUBLE PRECISION,
  phone            VARCHAR(20),
  email            VARCHAR(120),
  website          VARCHAR(200),
  principal_name   VARCHAR(150),
  num_teachers     INT DEFAULT 0,
  num_students     INT DEFAULT 0,
  status           VARCHAR(20) DEFAULT 'active',
  established_year INT,
  last_synced_at   TIMESTAMP,
  data_source      VARCHAR(50),
  created_at       TIMESTAMP DEFAULT NOW(),
  updated_at       TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_schools_code     ON schools(school_code);
CREATE INDEX IF NOT EXISTS idx_schools_province ON schools(province_id);
CREATE INDEX IF NOT EXISTS idx_schools_district ON schools(district_id);

-- ── Teachers ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS teachers (
  id                        SERIAL PRIMARY KEY,
  teacher_id                VARCHAR(30) UNIQUE NOT NULL,
  govt_employee_no          VARCHAR(30) UNIQUE,
  first_name                VARCHAR(80) NOT NULL,
  last_name                 VARCHAR(80) NOT NULL,
  gender                    VARCHAR(10),
  date_of_birth             DATE,
  citizenship_no            VARCHAR(30),
  photo_url                 VARCHAR(255),
  face_encoding             TEXT,
  phone                     VARCHAR(20),
  email                     VARCHAR(120),
  permanent_address         TEXT,
  temporary_address         TEXT,
  subject_specialization    VARCHAR(150),
  highest_qualification     VARCHAR(100),
  university                VARCHAR(150),
  teaching_license_no       VARCHAR(50),
  service_start_date        DATE,
  service_type              VARCHAR(30),
  school_id                 INT REFERENCES schools(id),
  designation               VARCHAR(80),
  tpdi_score                FLOAT DEFAULT 0,
  tpdi_category             VARCHAR(30),
  attendance_score          FLOAT DEFAULT 0,
  punctuality_score         FLOAT DEFAULT 0,
  student_performance_score FLOAT DEFAULT 0,
  is_active                 BOOLEAN DEFAULT TRUE,
  created_at                TIMESTAMP DEFAULT NOW(),
  updated_at                TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS teacher_transfers (
  id             SERIAL PRIMARY KEY,
  teacher_id     INT NOT NULL REFERENCES teachers(id),
  from_school_id INT REFERENCES schools(id),
  to_school_id   INT REFERENCES schools(id),
  transfer_date  DATE,
  reason         TEXT,
  order_no       VARCHAR(50),
  approved_by    VARCHAR(150),
  created_at     TIMESTAMP DEFAULT NOW()
);

-- ── Students ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
  id                   SERIAL PRIMARY KEY,
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
  school_id            INT REFERENCES schools(id),
  current_grade        VARCHAR(10),
  section              VARCHAR(10),
  roll_number          INT,
  academic_year        VARCHAR(10),
  dropout_risk_score   FLOAT DEFAULT 0,
  performance_trend    VARCHAR(20),
  learning_gaps        TEXT,
  is_active            BOOLEAN DEFAULT TRUE,
  created_at           TIMESTAMP DEFAULT NOW(),
  updated_at           TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS student_enrollments (
  id            SERIAL PRIMARY KEY,
  student_id    INT NOT NULL REFERENCES students(id),
  school_id     INT NOT NULL REFERENCES schools(id),
  grade         VARCHAR(10),
  academic_year VARCHAR(10),
  enrolled_on   DATE,
  left_on       DATE,
  left_reason   VARCHAR(150),
  created_at    TIMESTAMP DEFAULT NOW()
);

-- ── Attendance ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS teacher_attendance (
  id               SERIAL PRIMARY KEY,
  teacher_id       INT NOT NULL REFERENCES teachers(id),
  school_id        INT NOT NULL REFERENCES schools(id),
  date             DATE NOT NULL,
  check_in_time    TIME,
  check_out_time   TIME,
  status           VARCHAR(20) DEFAULT 'present',
  method           VARCHAR(20),
  check_in_lat     DOUBLE PRECISION,
  check_in_lon     DOUBLE PRECISION,
  check_out_lat    DOUBLE PRECISION,
  check_out_lon    DOUBLE PRECISION,
  geo_valid        BOOLEAN DEFAULT TRUE,
  fraud_flag       BOOLEAN DEFAULT FALSE,
  fraud_reason     VARCHAR(255),
  fraud_score      FLOAT DEFAULT 0,
  check_in_photo   VARCHAR(255),
  face_match_score FLOAT,
  notes            TEXT,
  recorded_by      INT REFERENCES users(id),
  created_at       TIMESTAMP DEFAULT NOW(),
  updated_at       TIMESTAMP DEFAULT NOW(),
  UNIQUE(teacher_id, date)
);

CREATE INDEX IF NOT EXISTS idx_ta_date  ON teacher_attendance(date);
CREATE INDEX IF NOT EXISTS idx_ta_fraud ON teacher_attendance(fraud_flag);

CREATE TABLE IF NOT EXISTS student_attendance (
  id          SERIAL PRIMARY KEY,
  student_id  INT NOT NULL REFERENCES students(id),
  school_id   INT NOT NULL REFERENCES schools(id),
  date        DATE NOT NULL,
  status      VARCHAR(20) DEFAULT 'present',
  reason      VARCHAR(255),
  recorded_by INT REFERENCES users(id),
  created_at  TIMESTAMP DEFAULT NOW(),
  UNIQUE(student_id, date)
);

-- ── Examinations ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS exams (
  id               SERIAL PRIMARY KEY,
  title            VARCHAR(255) NOT NULL,
  subject          VARCHAR(100) NOT NULL,
  grade            VARCHAR(10)  NOT NULL,
  academic_year    VARCHAR(10),
  exam_type        VARCHAR(50),
  difficulty       VARCHAR(20),
  total_marks      INT DEFAULT 100,
  pass_marks       INT DEFAULT 40,
  duration_minutes INT DEFAULT 180,
  exam_date        DATE,
  school_id        INT REFERENCES schools(id),
  created_by       INT REFERENCES users(id),
  ai_generated     BOOLEAN DEFAULT FALSE,
  curriculum_src   TEXT,
  status           VARCHAR(20) DEFAULT 'draft',
  created_at       TIMESTAMP DEFAULT NOW(),
  updated_at       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS questions (
  id            SERIAL PRIMARY KEY,
  exam_id       INT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
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
  created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS exam_papers (
  id             SERIAL PRIMARY KEY,
  exam_id        INT NOT NULL REFERENCES exams(id),
  paper_url      VARCHAR(255),
  answer_key_url VARCHAR(255),
  generated_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS student_results (
  id                SERIAL PRIMARY KEY,
  student_id        INT NOT NULL REFERENCES students(id),
  exam_id           INT NOT NULL REFERENCES exams(id),
  school_id         INT REFERENCES schools(id),
  marks_obtained    FLOAT,
  total_marks       FLOAT,
  percentage        FLOAT,
  grade             VARCHAR(5),
  rank_in_class     INT,
  ai_evaluated      BOOLEAN DEFAULT FALSE,
  evaluator_id      INT REFERENCES users(id),
  remarks           TEXT,
  subject_breakdown TEXT,
  created_at        TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS answer_sheets (
  id             SERIAL PRIMARY KEY,
  result_id      INT NOT NULL REFERENCES student_results(id),
  image_urls     TEXT,
  ocr_text       TEXT,
  ai_marks_json  TEXT,
  ocr_confidence FLOAT,
  processed_at   TIMESTAMP,
  created_at     TIMESTAMP DEFAULT NOW()
);

-- ── Audit Log ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_logs (
  id          SERIAL PRIMARY KEY,
  user_id     INT REFERENCES users(id),
  action      VARCHAR(50) NOT NULL,
  entity_type VARCHAR(50),
  entity_id   INT,
  old_value   TEXT,
  new_value   TEXT,
  ip_address  VARCHAR(45),
  user_agent  VARCHAR(255),
  notes       TEXT,
  created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at);

-- ── Seed: 7 Provinces ────────────────────────────────────
INSERT INTO provinces (id, name, name_np, code) VALUES
  (1, 'Koshi Province',        'कोशी प्रदेश',         'P1'),
  (2, 'Madhesh Province',      'मधेश प्रदेश',         'P2'),
  (3, 'Bagmati Province',      'बागमती प्रदेश',       'P3'),
  (4, 'Gandaki Province',      'गण्डकी प्रदेश',       'P4'),
  (5, 'Lumbini Province',      'लुम्बिनी प्रदेश',     'P5'),
  (6, 'Karnali Province',      'कर्णाली प्रदेश',      'P6'),
  (7, 'Sudurpashchim Province','सुदूरपश्चिम प्रदेश',  'P7')
ON CONFLICT (id) DO NOTHING;

-- ── Default admin (password hash is a placeholder — set via app) ──
INSERT INTO users (username, email, password_hash, full_name, role)
VALUES ('admin', 'admin@nepal-edu.gov.np', 'placeholder', 'System Administrator', 'federal')
ON CONFLICT (username) DO NOTHING;
