# WAR

## Getting Started

Essas instruções vão permitir preparar o ambiente para rodar o programa programa, para desenvolvimento ou teste

### Pré requisitos

Espera-se que o Python e pip ja estejam instalados.

```
pip install -r requirements.txt
```

## Executando o jogo:

### Banco de dados

É necessário ter o docker e o docker-compose instalados antes. Com ambos instalados e o docker executando, rodar, dentro da pasta `backend`:

```
docker-compose up
```

Feito isso, utilizar os arquivos `migration_up.sql` e `seed_up.sql` para subir as tabelas e popular o banco com os dados necessários para a lógica de salvamento funcionar. Podem ser usadas ferramentas de banco de dados, como o DBeaver, para executar os scripts SQL.

### Executando o jogo

Para rodar o jogo:

```
python .\main.py
```

## Autores

* **Marcelo Valentino** - *UFF* 
* **Gustavo Lauria**  - *UFF* 
* **Gabriel Ripper**  - *UFF* 
* **Henrique Martine**  - *UFF* 

