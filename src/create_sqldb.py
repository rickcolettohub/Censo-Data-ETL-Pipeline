import pandas as pd
import sqlalchemy as sqla
import os


db_path = os.path.join('data', 'censo_escolar.db')

# 🔹Deleta o db antigo se existir
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Arquivo antigo removido: {db_path}")

# 🔹Cria engine
engine = sqla.create_engine(f'sqlite:///{db_path}', echo=True)

# 🔹Cria o arquivo fisico
with engine.connect() as conn:
    pass

print(f"Novo banco criado em: {db_path}")
