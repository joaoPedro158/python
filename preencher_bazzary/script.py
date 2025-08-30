
#necessario para roda o script
# pip install sqlalchemy pymysql bcrypt
# pip install pymysql

from sqlalchemy import create_engine, Column, Integer, String,Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import random
import bcrypt


# O formato é: dialeto+driver://usuario:senha@host:porta/nome_do_banco
#mude o nome  banco que esta no phpmyadmin: no meu caso esta bazzary_store
engine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/bazzary_store", echo=False)
Base = declarative_base()
Sessao =sessionmaker(bind=engine)
sessao = Sessao()
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    imagem = Column(String, nullable=True)
    preco = Column(Numeric(10,2), nullable=False)
    descricao = Column(String, nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    

class Usuario(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    
def hash_password_bcrypt(senha):
    salt = bcrypt.gensalt(rounds=10)
    
    hashed_password_bytes = bcrypt.hashpw(senha.encode('utf-8'), salt)
    hashed_password_str = hashed_password_bytes.decode('utf-8')

    if hashed_password_str.startswith('$2b$'):
        return '$2y$' + hashed_password_str[4:]
        
    return hashed_password_str
    
def gerar_usuarios():
    senha_criptografada = hash_password_bcrypt("suasenha")
    usuarios_definidos = [
        Usuario(id = 1 ,name = "joao pedro",email ="joaopedro@email.com", password= senha_criptografada ),
        Usuario(id = 2 ,name = "ana sophia",email ="anasophia@email.com", password=senha_criptografada ),
        Usuario(id = 3 ,name = "jose",email ="jose@email.com", password= senha_criptografada ),
    ]
    
    id_existentes = {u.id for u in sessao.query(Usuario).filter(Usuario.id.in_([1, 2, 3])).all()} 
    novos_usuarios = [u for u in usuarios_definidos if u.id not in id_existentes]
    
    if not novos_usuarios:
        print("✅ Usuários padrão já existem, ignorando criação.")
        return
    
    try:
        sessao.add_all(novos_usuarios)
        sessao.commit()
        print(f"Usuários adicionados com sucesso! ({len(novos_usuarios)} inseridos)")
    except SQLAlchemyError as e:
        sessao.rollback()
        print(f"❌ Erro ao inserir usuários: {e}")
    


   

def gerar_dados_aleatorios(): 
    
    nome_aleatorio = random.choice([
        'Camiseta', 'Calça', 'Tênis', 'Boné', 'Mochila', 'Relógio', 'Óculos de Sol', 'Jaqueta', 'Meias', 'Carteira'
        ])
    imagem_aleatoria = "produtos/" + random.choice(['img_1.jpg', 'img_2.png', 'img_3.png', 'img_4.png', 'img_5.jpeg'])
    preco_aleatorio = round(random.uniform(1,200), 2)
    descricao_aleatoria = random.choice(['Produto de alta qualidade', 'Produto durável e confortável', 'Estilo moderno e elegante', 'Perfeito para todas as ocasiões', 'Design inovador e funcional'])
    estoque_aleatorio = random.randint(1,500)
    user_id_aleatorio = random.choice([1, 2, 3])
    
    print(f"Id: {user_id_aleatorio} Nome: {nome_aleatorio}, imagem: {imagem_aleatoria} ,  Preço: {preco_aleatorio}, Descrição: {descricao_aleatoria} , Estoque: {estoque_aleatorio}")
    
    novo_produto = Produto(
        nome=nome_aleatorio,
        imagem = imagem_aleatoria,
        preco=preco_aleatorio,
        descricao=descricao_aleatoria,
        estoque=estoque_aleatorio,
        user_id=user_id_aleatorio
        
    )
    sessao.add(novo_produto)
    sessao.commit()
    

    




try:
    with engine.connect() as connection:
        print("✅ Conexão com o banco de dados do XAMPP estabelecida com sucesso!")
    Base.metadata.create_all(engine)
    
    gerar_usuarios()
    
    quantidade = input("Quantos produtos deseja inserir? ")
    if quantidade.isdigit() and int(quantidade) > 0:
        for _ in range(int(quantidade)):
            gerar_dados_aleatorios()
    else:
        print("Por favor, insira um número válido maior que zero.")
    
        

except SQLAlchemyError as e:
    print(f"❌ Erro ao conectar ou executar a consulta: {e}")
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {e}")

