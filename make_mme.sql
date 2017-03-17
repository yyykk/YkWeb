create database demo char(20)acter set gbk;

use demo;

select * from mme_all;
grant all on *.* to 'root'@'localhost';
select user,host from mysql.user;

show variables like '%secure_file_priv%';

select RequestTime,EndTime,EndTime-RequestTime from mme_all
where XDRID = "16048321a1dd9c00";

select * from http_test;

alter table http_test
add constraint pk_orderinfo PRIMARY KEY(XDRID, RequestTime, ProcedureEndTime);

load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/http.txt' 
into table `http_test`
fields terminated by ',';

load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/http10/http2.txt' 
into table `http_test`
fields terminated by ',';

load data infile 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/http10/http6.txt' 
into table `http_test`
fields terminated by ',';

select RequestTime from http_test ;
select FROM_UNIXTIME('1464973385.641','%Y-%m-%d %H:%i:%s');
SELECT FROM_UNIXTIME(1468239342.226);

select MSISDN , count(MSISDN) from http_test #where Browser != 0
group by MSISDN
order by count(MSISDN) ;

select ECI,  sum(OperDelay) / count(ECI) as value from http_test 
group by ECI
order by value;

select count(*) from http_test;

select * from http_test;

#alter table http_test engine=innodb;

SHOW PROCESSLIST;

alter table http_test engine = myisam;

alter table http_test modify HOST char(200) null;
alter table http_test modify HTTP_content_type char(200) null;

select left(from_unixtime(left(RequestTime, 10)), 19) from http_test;

create view counttemp as
select count(*) as c from http_test
group by left(from_unixtime(left(RequestTime, 10)), 19);

select sum(c) from counttemp;

select
ECI, 
left(from_unixtime(left(RequestTime, 10)), 16) as '起始时间',
sum(ULTraffic) + sum(DLTraffic) as '流量', 
sum(ULTCPOoOPacket)+sum(DLTCPOoOPacket)+sum(ULTCPRetransPacket)+sum(DLTCPRetransPacket) as 'TCP重传',
(sum(ULTCPOoOPacket)+sum(DLTCPOoOPacket)+sum(ULTCPRetransPacket)+sum(DLTCPRetransPacket))*1000000
/
(sum(ULTraffic) + sum(DLTraffic))as 'TCP质量',
sum(TCPSYNAtteDelay)+sum(FirstReqToFirstResDelay) as 'TCP延时',
sum(FirstHTTPResPacketDelay)+sum(LastHTTPPacketDelay) as 'HTTP延时'
from http_test
group by left(from_unixtime(left(RequestTime, 10)), 16);

drop table EciTimeStream;

create table EciTimeStream as
select
ECI, 
left(from_unixtime(left(RequestTime, 10)), 19) as 'Time',
sum(ULTraffic) + sum(DLTraffic) as 'Stream'
from http_test
group by left(from_unixtime(left(RequestTime, 10)), 19);

create table EciTimeStream as
select
ECI, 
left(from_unixtime(left(RequestTime, 10)), 19) as 'Time',
ULTraffic + DLTraffic as 'Stream'
from http_test
group by left(from_unixtime(left(RequestTime, 10)), 19);

select * from http_test;

select count() from EciTimeStream;

select HTTP_content_type
from http_test
group by HTTP_content_type;

select max(left(RequestTime, 8)), min(left(RequestTime, 8))
from http_test;

select 
from_unixtime(max(RequestTime)/1000), 
from_unixtime(min(RequestTime)/1000)
from http_test;

select left(RequestTime, 8)+'00000' as Time from http_test;

select * from http_test;



select 
substring(from_unixtime(left(RequestTime, 7) * 1000), 11, 19) as 'begin',
substring(from_unixtime((left(RequestTime, 7) + 1) * 1000), 11, 19) as 'end',
cast((sum(ULTraffic) + sum(DLTraffic)) / max((sum(ULTraffic) + sum(DLTraffic)) * 100) as decimal) 'count' , ECI
from http_test
group by substring(from_unixtime(left(RequestTime, 7) * 1000), 11, 19);



select t.lng, t.lat, e.count
from  tac as t, ecicounter as e
where t.ECI = e.ECI;

select t.lng, t.lat, cast(e.count as decimal) from  tac as t, ecicounter as e where t.ECI = e.ECI;

select ECI from tac;

select t.lng, t.lat, e.Stream from ecihourstream as e, tac as t where e.ECI = '117608449' and e.ECI = t.ECI;



select t.lng, t.lat, e.Stream / m.MStream * 100 as count
from ecihourstream as e , MaxStream as m, tac as t
where t.ECI = e.ECI and e.ECI = m.ECI and e.Time = '2016-06-26 00';

alter view MaxStream as 
select ECI, max(Stream) as MStream from ecihourstream 
group by ECI;

select * from ecihourstream;

select t.lng, t.lat, e.Stream as count from EciTimeStream as e , MaxStream as m, tac as t where t.ECI = e.ECI and e.ECI = m.ECI and e.Time = '2016-06-26 19:00:00';

select t.ECI, t.lng, t.lat, e.Stream as count from EciTimeStream as e, tac as t where t.ECI = e.ECI and e.Time = '2016-06-26 19:00:01';

select t.ECI, t.lng, t.lat, e.Stream, e.Time as count from EciTimeStream as e, tac as t where t.ECI = e.ECI and e.ECI = '252406148';

select Stream from EciTimeStream order by Stream desc;

select count(distinct Time) from EciTimeStream;

select * from EciTimeStream;

show global variables like 'sql_select_limit';

show global variables like 'innodb_buffer_pool_size';

set global innodb_buffer_pool_size = 256M;



