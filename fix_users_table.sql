-- ============================================================
--  Fix users table — run this in MySQL Workbench
--  Safely adds missing columns using IF NOT EXISTS (MySQL 8.0+)
-- ============================================================

USE nepal_edu_platform;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS province_id     INT NULL,
    ADD COLUMN IF NOT EXISTS district_id     INT NULL,
    ADD COLUMN IF NOT EXISTS municipality_id INT NULL,
    ADD COLUMN IF NOT EXISTS school_id       INT NULL;

-- ============================================================
--  After running this, run provincial_admins.sql
-- ============================================================
