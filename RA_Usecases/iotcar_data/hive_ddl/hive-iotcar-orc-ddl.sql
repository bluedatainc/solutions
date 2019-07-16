create database if not exists iotcar_orc;
use iotcar_orc;

drop table if exists iotcar_orc.owner_dim;
create  table iotcar_orc.owner_dim
stored as orc
as select * from iotcar_text.owner_dim;

drop table if exists iotcar_orc.auto_dim;
create  table iotcar_orc.auto_dim
stored as orc
as select * from iotcar_text.auto_dim;

drop table if exists iotcar_orc.iotcar_stream;
create table iotcar_orc.iotcar_stream
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
stored as orc;

SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

insert overwrite table iotcar_orc.iotcar_stream  
select
  cs.EventID ,
  cs.AutoID ,
  cs.EventCategoryID ,
  cs.EventMessage ,
  cs.City ,
  cs.OutsideTemperature ,
  cs.EngineTemperature ,
  cs.Speed ,
  cs.Fuel ,
  cs.EngineOil ,
  cs.TirePressure ,
  cs.Odometer ,
  cs.AcceleratorPedalPosition ,
  cs.ParkingBrakeStatus ,
  cs.HeadlampStatus ,
  cs.BrakePedalStatus ,
  cs.TransmissionGearPosition ,
  cs.IgnitionStatus ,
  cs.WindshieldWiperStatus ,
  cs.Abs ,
  cs.PostalCode ,
  cs.EventTimestamp 
 from iotcar_text.iotcar_stream cs;

analyze table iotcar_orc.auto_dim compute statistics for columns;
analyze table iotcar_orc.owner_dim compute statistics for columns;
analyze table iotcar_orc.iotcar_stream compute statistics for columns;
 