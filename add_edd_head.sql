USE nepal_edu_platform;

ALTER TABLE provinces
    ADD COLUMN IF NOT EXISTS edd_head VARCHAR(150) NULL;

SELECT 'edd_head column added.' AS status;
