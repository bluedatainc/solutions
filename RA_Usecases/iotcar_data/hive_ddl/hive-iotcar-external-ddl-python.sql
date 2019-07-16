create database if not exists iotcar_text;
use iotcar_text;

drop table if exists iotcar_text.owner_dim;
create EXTERNAL table iotcar_text.owner_dim
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
location '<iotloc>/bluedata/usecase/iotcar/data/owners';

drop table if exists iotcar_text.auto_dim;
create EXTERNAL table iotcar_text.auto_dim
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
location '<iotloc>/bluedata/usecase/iotcar/data/autos';

drop table if exists iotcar_text.iotcar_stream;
create EXTERNAL table iotcar_text.iotcar_stream
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
location '<iotloc>/bluedata/usecase/iotcar/data/iotcar_stream';

analyze table iotcar_text.auto_dim compute statistics for columns;
analyze table iotcar_text.owner_dim compute statistics for columns;
analyze table iotcar_text.iotcar_stream compute statistics for columns;


