create database if not exists iotcar_text;
use iotcar_text;


drop table if exists iotcar_text.owner_dim_hdfs;
create EXTERNAL table iotcar_text.owner_dim_hdfs
(
   PersonID int, 
   FullName string,
   PreferredName string,
   DateOfBirth string,
   PhoneNumber string,
   FaxNumber string,
   EmailAddress string 
)
row format delimited fields terminated by '|' 
location 'dtap://IoTHDFS/user/analyst1/bluedata/usecase/iotcar/data/owners';

drop table if exists iotcar_text.auto_dim_hdfs;
create EXTERNAL table iotcar_text.auto_dim_hdfs
(
  AutoID int,
  OwnerID int,
  VIN string,
  Make string,
  Model string,
  Year int,
  DriveTrain string,
  EngineType string,
  ExteriorColor string,
  InteriorColor string,
  Transmission string
)
row format delimited fields terminated by '|' 
location 'dtap://IoTHDFS/user/analyst1/bluedata/usecase/iotcar/data/autos';

drop table if exists iotcar_text.iotcar_stream_hdfs;
create EXTERNAL table iotcar_text.iotcar_stream_hdfs
(
  EventID bigint,
  AutoID int,
  EventCategoryID int,
  EventMessage string,
  City string,
  OutsideTemperature int,
  EngineTemperature int,
  Speed int,
  Fuel int,
  EngineOil int,
  TirePressure int,
  Odometer int,
  AcceleratorPedalPosition int,
  ParkingBrakeStatus boolean ,
  HeadlampStatus boolean ,
  BrakePedalStatus boolean ,
  TransmissionGearPosition int,
  IgnitionStatus boolean ,
  WindshieldWiperStatus boolean  ,
  Abs boolean ,
  PostalCode string,
  EventTimestamp timestamp
)
row format delimited fields terminated by '|' 
location 'dtap://IoTHDFS/user/analyst1/bluedata/usecase/iotcar/data/iotcar_stream';


drop table if exists iotcar_text.owner_dim_nfs;
create EXTERNAL table iotcar_text.owner_dim_nfs
(
   PersonID int, 
   FullName string,
   PreferredName string,
   DateOfBirth string,
   PhoneNumber string,
   FaxNumber string,
   EmailAddress string 
)
row format delimited fields terminated by '|' 
location 'dtap://NFSIoTData/data/owners';


drop table if exists iotcar_text.auto_dim_nfs;
create EXTERNAL table iotcar_text.auto_dim_nfs
(
  AutoID int,
  OwnerID int,
  VIN string,
  Make string,
  Model string,
  Year int,
  DriveTrain string,
  EngineType string,
  ExteriorColor string,
  InteriorColor string,
  Transmission string
)
row format delimited fields terminated by '|' 
location 'dtap://NFSIoTData/data/autos';

drop table if exists iotcar_text.iotcar_stream_nfs;
create EXTERNAL table iotcar_text.iotcar_stream_nfs
(
  EventID bigint,
  AutoID int,
  EventCategoryID int,
  EventMessage string,
  City string,
  OutsideTemperature int,
  EngineTemperature int,
  Speed int,
  Fuel int,
  EngineOil int,
  TirePressure int,
  Odometer int,
  AcceleratorPedalPosition int,
  ParkingBrakeStatus boolean ,
  HeadlampStatus boolean ,
  BrakePedalStatus boolean ,
  TransmissionGearPosition int,
  IgnitionStatus boolean ,
  WindshieldWiperStatus boolean  ,
  Abs boolean ,
  PostalCode string,
  EventTimestamp timestamp
)
row format delimited fields terminated by '|' 
location 'dtap://NFSIoTData/data/iotcar_stream';



 




