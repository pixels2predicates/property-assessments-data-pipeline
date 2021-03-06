CREATE TABLE "GIS_DS"."OFFPROP_EXT" 
(
  "OBJECTID" NUMBER(*,0), 
  "OPARCEL" NVARCHAR2(255), 
  "OCAREOF" NVARCHAR2(255), 
  "O1STADD" NVARCHAR2(255), 
  "O2NDADD" NVARCHAR2(255), 
  "OSTNAME" NVARCHAR2(255), 
  "OCITYST" NVARCHAR2(255), 
  "OZIP" NVARCHAR2(255), 
  "OFILL" NVARCHAR2(255)
)
ORGANIZATION EXTERNAL 
(
  TYPE ORACLE_LOADER
  DEFAULT DIRECTORY "GIS_DIR"
  ACCESS PARAMETERS
  (
    RECORDS DELIMITED BY NEWLINE
    SKIP 1
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    MISSING FIELD VALUES ARE NULL
    (
      OPARCEL,
      OCAREOF,
      O1STADD,
      O2NDADD,
      OSTNAME,
      OCITYST,
      OZIP
    )
  )
  LOCATION ('off_property.csv')
);
