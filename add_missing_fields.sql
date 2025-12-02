-- Add missing fields to Transporter Agreement table
-- This script adds the branch and district ForeignKey fields that are missing

-- Add branch_id field
ALTER TABLE dashboard_transporteragreement 
ADD COLUMN branch_id INT NULL,
ADD CONSTRAINT fk_transporter_branch 
FOREIGN KEY (branch_id) REFERENCES dashboard_masstatebranch(id);

-- Add district_id field  
ALTER TABLE dashboard_transporteragreement 
ADD COLUMN district_id INT NULL,
ADD CONSTRAINT fk_transporter_district 
FOREIGN KEY (district_id) REFERENCES dashboard_masdistrict(id);

-- Add district_code field if it doesn't exist
ALTER TABLE dashboard_transporteragreement 
ADD COLUMN district_code VARCHAR(20) NULL;

-- Update the state field to be a ForeignKey to MasState
-- First, we need to check if there are existing records and handle the data migration
-- For now, let's just add the field and we can handle data migration separately

-- Note: This script assumes the table structure is compatible
-- You may need to adjust based on your specific database setup
