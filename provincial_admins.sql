-- ══════════════════════════════════════════════════════════════
--  Provincial Sub-Admin Users — Nepal Education Platform
--  Run this in MySQL Workbench after setup_database.sql
--  Default passwords: Province1@Nepal2026 … Province7@Nepal2026
-- ══════════════════════════════════════════════════════════════

USE nepal_edu_platform;

-- Province 1 – Koshi  (password: Province1@Nepal2026)
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, province_id, is_active) VALUES
('prov1_admin', 'prov1@edu.np', 'scrypt:32768:8:1$lQxCxdRkpx8Gf0iW$e674152fd81f5c3b2192ea74e7ab56f76b1d957c5c8dfea177a180a233c683706f0615afec3075f02ff1b6c94488757098dd7fc5e34082fefe691025884558ac', 'Koshi Province Admin', 'provincial', 1, 1);

-- Province 2 – Madhesh  (password: Province2@Nepal2026)
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, province_id, is_active) VALUES
('prov2_admin', 'prov2@edu.np', 'scrypt:32768:8:1$C7yoLE5fD7HkqOg5$a3c9eedc0e350ac3b18ff4ee8963e513011010c8876384e6e4ca7a45e9eaed481622dc614946a4da7930cd46057be6b685d01eefa5a1ac876fe8289bc0802c6b', 'Madhesh Province Admin', 'provincial', 2, 1);

-- Province 3 – Bagmati  (password: Province3@Nepal2026)
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, province_id, is_active) VALUES
('prov3_admin', 'prov3@edu.np', 'scrypt:32768:8:1$D4hkZMzIEu6yTeF9$99f3376e301700cf1738df296bc07f49cb7a017042d82dea65295418ba8bb22704785ce20d18ae7bd437703d9fa6659332fd0e535ae507c0b06d27948ce6a95d', 'Bagmati Province Admin', 'provincial', 3, 1);

-- Province 4 – Gandaki  (password: Province4@Nepal2026)
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, province_id, is_active) VALUES
('prov4_admin', 'prov4@edu.np', 'scrypt:32768:8:1$R3uMFHGe5bcFJqIb$1410e6ffb6fbff4f3001dd2a44adbd0b546ecf30fc4c0786d86dae35756353974bfcfc454d0b1138131deb81982d6f43f81a715cd30e1bd9d5f5b5515cf7ea6c', 'Gandaki Province Admin', 'provincial', 4, 1);

-- Province 5 – Lumbini  (password: Province5@Nepal2026)
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, province_id, is_active) VALUES
('prov5_admin', 'prov5@edu.np', 'scrypt:32768:8:1$KLWWbLxKW3XByqFI$a5f873a2bf0456581ad7a65f06205a28b0873c04305a489a1fd73d65b0bc29eb6fd26636def5d96ecb5ea24f22804fb6fb2dad47d7009a12a3557aaa8d9f07b7', 'Lumbini Province Admin', 'provincial', 5, 1);

-- Province 6 – Karnali  (password: Province6@Nepal2026)
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, province_id, is_active) VALUES
('prov6_admin', 'prov6@edu.np', 'scrypt:32768:8:1$N5tLud559gvt3hrm$322847cf32bcd32736e7ce9f2bb6fcc34ba03b915c1ad9882c33ee7a7559ccaf64c9523093a03cbfa721fa69a78638a84fba229d5a4540e8abe8917fa8cb9cc7', 'Karnali Province Admin', 'provincial', 6, 1);

-- Province 7 – Sudurpashchim  (password: Province7@Nepal2026)
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, province_id, is_active) VALUES
('prov7_admin', 'prov7@edu.np', 'scrypt:32768:8:1$O6xAjPp4e0V1U98a$c6362c55aef78bcf3799fd6ce23a4b71b13f36be9ecb4a7abcfb9c967bd33ca628727fe1445632a437bb8dfa0c6785829ff914008c457564e02500114d1f3a14', 'Sudurpashchim Province Admin', 'provincial', 7, 1);

-- ══════════════════════════════════════════════════════════════
--  Login credentials summary
-- ══════════════════════════════════════════════════════════════
--  Province 1 (Koshi)         prov1_admin / Province1@Nepal2026
--  Province 2 (Madhesh)       prov2_admin / Province2@Nepal2026
--  Province 3 (Bagmati)       prov3_admin / Province3@Nepal2026
--  Province 4 (Gandaki)       prov4_admin / Province4@Nepal2026
--  Province 5 (Lumbini)       prov5_admin / Province5@Nepal2026
--  Province 6 (Karnali)       prov6_admin / Province6@Nepal2026
--  Province 7 (Sudurpashchim) prov7_admin / Province7@Nepal2026
-- ══════════════════════════════════════════════════════════════
