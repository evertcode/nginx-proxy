drop table if exists logs;

create table logs (
    id serial primary key,
    time_local timestamp with time zone default now(),
    client text,
    method text,
    request text,
    request_length integer,
    status integer,
    bytes_sent integer,
    body_bytes_sent integer,
    referer text,
    user_agent text,
    upstream_addr text,
    request_time real,
    upstream_response_time real,
    upstream_connect_time real
);
