create table if not exists sessaoJogo (
	id serial primary key,
	estadoPartida varchar(25) default 'ativa',
	criada_em TIMESTAMPTZ default NOW()
);

create table if not exists regiao (
	id serial primary key,
	bonusDeTropa int,
	nome varchar(30)
);

create table if not exists sessaojogador (
	id serial primary key,
	idjogador int not null,
	idsessao int not null references sessaojogo(id),
	vez bool not null,
	naPartida bool default true,
	ehIA bool not null,
	cor varchar(15)
);

create table if not exists territorio (
	id serial primary key,
	idRegiao int not null references regiao(id),
	nome varchar(30) not null
);

create table if not exists territoriosvizinhos(
	id serial primary key,
	idterritorio1 int not null references territorio(id),
	idterritorio2 int not null references territorio(id)
);

create table if not exists territoriosessaojogador (
	id serial primary key,
	idsessaojogador int not null references sessaojogador(id),
	idterritorio int not null references territorio(id),
	contagemtropas int
);

create table if not exists cartaterritorio(
	id serial primary key,
	formato varchar(25) default 'joker',
	idsessaojogador int not null references sessaojogador(id)
);