create table if not exists salaJogo (
	id serial primary key,
	estadoPartida varchar(255) default 'esperando jogadores'

);

create table if not exists jogador (
	id serial primary key,
	nome varchar(255) not null
);

create table if not exists regiao (
	id serial primary key,
	bonusDeTropa int,
	nome varchar(255)
);

create table if not exists salajogador (
	id serial primary key,
	idjogador int not null references jogador(id),
	idsala int not null references salajogo(id),
	vez int not null,
	ehdono bool not null,
	naPartida bool default true,
	ehIA bool not null,
	cor varchar(15)
);

create table if not exists territorio (
	id serial primary key,
	idRegiao int not null references regiao(id),
	nome varchar(255) not null
);

create table if not exists territoriosvizinhos(
	id serial primary key,
	idterritorio1 int not null references territorio(id),
	idterritorio2 int not null references territorio(id)
);

create table if not exists territoriosalajogador (
	id serial primary key,
	idsalajogador int not null references salajogador(id),
	idterritorio int not null references territorio(id),
	contagemtropas int
);

create table if not exists cartaterritorio(
	id serial primary key,
	formato varchar(255) default 'joker',
	idsalajogador int not null references salajogador(id)
);