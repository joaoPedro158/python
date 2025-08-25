import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base,sessionmaker

# Configuração do banco (SQLite local)
engine = create_engine('sqlite:///banco_de_dados.db', echo=True)

Sessao =sessionmaker(engine)

# Criação do modelo base
Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Integer, nullable=False)
    descricao = Column(String, nullable=False)
    estoque = Column(Integer, nullable=False)


def inserir_produto(nome_inserido, preco_inserido, descricao_inserido, estoque_inserido):
    sessao = Sessao() 
    try:
        if nome_inserido and preco_inserido >= 0 and descricao_inserido and estoque_inserido >= 0:
            novo_produto = Produto(nome=nome_inserido, preco=preco_inserido, descricao=descricao_inserido, estoque=estoque_inserido)
            sessao.add(novo_produto)
            sessao.commit()
            print(f"Produto {nome_inserido} inserido com sucesso!")
        else:
            print("Dados inválidos. Verifique os valores inseridos.")
    except Exception as e:
        sessao.rollback()
        print(f"Erro ao inserir produto: {nome_inserido}: {e}")

    finally:
        sessao.close()


def selecionar_produto(nome_inserido = ''):
    sessao = Sessao()
    try:
        if nome_inserido:
            dados = sessao.query(Produto).filter(Produto.nome == nome_inserido)
        else:
            dados = sessao.query(Produto).all()
        
        for i  in dados:
            print(f"ID: {i.id} | Nome: {i.nome} | Preço: {i.preco} | Descrição: {i.descricao} | Estoque: {i.estoque}")
                
    except Exception as e:
        print("Erro ao selecionar produto:")
    finally:
        sessao.close() 

def atualizar_produto(id_inserido,nome_inserido):
    sessao = Sessao()
    try:
        if(all([id_inserido,nome_inserido])):
            produto = sessao.query(Produto).filter(Produto.id == id_inserido).first()
            produto.nome = nome_inserido
            sessao.commit()
            print(f"Produto {id_inserido} atualizado com sucesso!")
        else:
            print("Dados inválidos. Verifique os valores inseridos.")
    except Exception as e:
        sessao.rollback()
        print(f"Erro ao atualizar produto: {e}")
        
    finally:
        sessao.close()
        
def deletar_produto(id_inserido):
    sessao = Sessao()
    try:
        if id_inserido:
            produto = sessao.query(Produto).filter(Produto.id == id_inserido).first()
            sessao.delete(produto)
            sessao.commit()
            print(f"Produto {id_inserido} deletado com sucesso!")
        else:
            sessao.rollback()
            print("ID inválido. Verifique o valor inserido.")
    except Exception as e:
        sessao.rollback()
        print(f"Erro ao deletar produto: {e}")      
        
    finally:
        sessao.close()
    
        
if __name__ == '__main__':
    os.system('cls')
    Base.metadata.create_all(engine)
    # selecionar_produto("jeans")
    # atualizar_produto(3, "chapeu")
    # deletar_produto(3)

