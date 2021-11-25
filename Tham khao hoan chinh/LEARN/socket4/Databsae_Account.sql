create Database Socket_Account
go

use Socket_Account
go


create table Account(
	username varchar(10) NOT NULL,
	pass varchar(10) NOT NULL,
)
go

insert Account values ('duchieuvn', '123456')
insert Account values ('a', '1')
insert Account values ('admin', '123456')