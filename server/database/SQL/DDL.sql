create schema bb_test;
create table brokerbot_configuration_users (
user_id		bigint primary key,
username	text,
password_	text
);
CREATE TABLE BrokerBot_configuration_Bots (
bot_id bigint PRIMARY KEY,
user_id bigint,
alpaca_key VARCHAR(225));