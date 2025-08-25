# -*- coding: utf-8 -*-

# PASSO 1: INSTALAR AS BIBLIOTECAS NECESSÁRIAS
# Abra o seu terminal e instale o SQLAlchemy e o driver do MySQL.
# O PyMySQL é recomendado por ser em puro Python e mais fácil de instalar.
#
# pip install sqlalchemy
# pip install PyMySQL
#

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# --- CONFIGURAÇÃO DA CONEXÃO ---

# Estes são os dados do seu banco de dados no XAMPP.
# Altere o 'DB_NOME' para o nome do banco que você quer conectar.
DB_DIALETO = "mysql"
DB_DRIVER = "pymysql"
DB_USUARIO = "root"
DB_SENHA = ""  # A senha padrão do XAMPP é vazia
DB_HOST = "127.0.0.1"
DB_PORTA = "3306"
DB_NOME = "bazzary_store"  # <-- MUDE AQUI para o nome do seu banco de dados

# --- PASSO 2: MONTAR A STRING DE CONEXÃO ---

# O SQLAlchemy usa uma URL especial para se conectar.
# O formato é: dialeto+driver://usuario:senha@host:porta/nome_do_banco
string_de_conexao = f"{DB_DIALETO}+{DB_DRIVER}://{DB_USUARIO}:{DB_SENHA}@{DB_HOST}:{DB_PORTA}/{DB_NOME}"

print(f"Tentando conectar ao banco de dados: {DB_NOME}")

# --- PASSO 3: CRIAR O "MOTOR" E TESTAR A CONEXÃO ---

try:
    # A função create_engine() cria o objeto principal de conexão.
    engine = create_engine(string_de_conexao)

    # Vamos tentar fazer uma conexão para verificar se tudo está certo.
    with engine.connect() as connection:
        print("✅ Conexão com o banco de dados do XAMPP estabelecida com sucesso!")
        
        # --- PASSO 4 (EXTRA): EXECUTANDO UMA CONSULTA SIMPLES ---
        print("\nExecutando uma consulta de teste...")
        
        # O text() é usado para dizer ao SQLAlchemy que isso é um comando SQL seguro.
        query = text("SELECT version();") # Pede a versão do MySQL
        
        # Executa a consulta
        result = connection.execute(query)
        
        # Pega o primeiro resultado
        versao_mysql = result.scalar()
        
        print(f"Versão do MySQL/MariaDB: {versao_mysql}")

except SQLAlchemyError as e:
    print(f"❌ Erro ao conectar ou executar a consulta: {e}")
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {e}")

