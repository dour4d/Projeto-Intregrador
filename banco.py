import pymysql.connections
from pymysql.connections import err, ER

print("Conexão a ser estabelecida...")
try:
      conn = pymysql.connections.Connection(
            host='127.0.0.1',
            user='root',
            password='root' #mudar a senha dependendo de onde estiver
      )
except pymysql.connections.Error as err:
      if err.errno == err.ER_ACCESS_DENIED_ERROR:
            print('Usuário ou senha inválida')
      else:
            print(err)

cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `dados`;")
cursor.execute("CREATE DATABASE `dados`;")
cursor.execute("USE `dados`;")

TABLES = {}
TABLES['Compra'] = ('''
      CREATE TABLE `compra` (
      `id` int(9) NOT NULL AUTO_INCREMENT,
      `n_user` varchar(50) NOT NULL,
      `c_comprado` varchar(50) NOT NULL,
      `valor_pago` varchar(50) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Carros'] = ('''
      CREATE TABLE `carros` (
      `id` int(9) NOT NULL AUTO_INCREMENT,
      `modelo` varchar(50) NOT NULL,
      `cor` varchar(40) NOT NULL,
      `ano` int(4) NOT NULL,
      `preco` varchar(50) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['User'] = ('''
      CREATE TABLE `user` (
      `id` int(11) NOT NULL AUTO_INCREMENT,                     
      `nome` varchar(20) NOT NULL,
      `senha` varchar(20) NOT NULL,
      `cpf` varchar(11) NOT NULL,
      `cidade` varchar(20) NOT NULL,
      `bairro` varchar(20) NOT NULL,
      `rua` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabelaNome in TABLES:
      tabelaSQL = TABLES[tabelaNome]
      try:
            print('Criação da tabela {}:'.format(tabelaNome), end=' ')
            cursor.execute(tabelaSQL)
      except pymysql.connections.Error as err:
            if err.errno == err.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# Inserção de Usuário
usuarioSQL = 'INSERT INTO user (nome, senha, cpf, cidade, bairro, rua) VALUES (%s, %s, %s, %s, %s, %s)'
usuarios = []
cursor.executemany(usuarioSQL, usuarios)
cursor.execute('select * from dados.user')
print(' -------------  Usuários:  -------------')
for usuario in cursor.fetchall():
    print(usuario[1])

#relação user carro


# Inserção de clube
carrosSQL = 'INSERT INTO carros (modelo, cor, ano, preco) VALUES (%s, %s, %s, %s)'
carros = [
    ('Fusca', 'Preto', '1990','70,000,00'),
    ('Ferrari', 'Amarelo', '2000','1,500,000,00'),
    ('Uno com escada', 'Branco', '1990','100,000,00'),
    ('celta', 'Preto', '2000','150,000,00'),
    ('Bugatti Veyron', 'Vermelho e Preto', '1980','5,000,000,00'),
    ('chevette-junior', 'Vermelho', '1970','300,000,00'),
    ('Gol', 'branco', '1990','40,000,00'),
]
cursor.executemany(carrosSQL, carros)
cursor.execute('select * from dados.carros')
print(' -------------  carros:  -------------')
for carros in cursor.fetchall():
    print(carros[1])

conn.commit()
cursor.close()
conn.close()