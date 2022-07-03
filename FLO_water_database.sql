CREATE DATABASE FLO_water;
USE FLO_water;

CREATE TABLE water_usage (id INT AUTO_INCREMENT primary key NOT NULL, timestamp timestamp, psi decimal(15,5), gpm decimal(15,5));
ALTER TABLE water_usage ALTER psi SET DEFAULT 0;
ALTER TABLE water_usage ALTER gpm SET DEFAULT 0;
