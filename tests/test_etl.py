import sys
import os
import pandas as pd

# Garantindo que o python encontre o módulo
current_dir = os.path.dirname(os.path.abspath(__file__))
# sobe um nível para achar a raiz do projeto (hanami_api)
project_root = os.path.dirname(current_dir)
# Adiciona a raiz ao Python, para ele enxergar a pasta 'src'
sys.path.append(project_root)

try:
    from src.services.data_processor import process_dataset
    from src.utils.constants import REQUIRED_COLUMNS
except ImportError as e:
    print(f"❌ ERRO CRÍTICO DE IMPORTAÇÃO: {e}")
    print(f"O Python está procurando em: {sys.path}")
    sys.exit(1)

ARQUIVO_TESTE = os.path.join(project_root, "data", "vendas_ficticias.csv")

def run_test():
    print("="*60)
    print("INICIANDO TESTE DE ETL (EXTRAÇÃO E LIMPEZA)")
    print("="*60)

    #Verificar se o arquivo existe
    if not os.path.exists(ARQUIVO_TESTE):
        print(f"ERRO: Arquivo não encontrado em: {ARQUIVO_TESTE}")
        return

    print(f"Lendo arquivo: {ARQUIVO_TESTE}...")
    
    with open(ARQUIVO_TESTE, "rb") as f:
        conteudo = f.read()
        nome_arquivo = os.path.basename(ARQUIVO_TESTE)

    try:
        #Executar o Processamento
        df = process_dataset(conteudo, nome_arquivo)
        
        print("\nPROCESSAMENTO CONCLUÍDO SEM ERROS!")
        
        # Validação de Nulos
        total_nulos = df.isnull().sum().sum()
        if total_nulos == 0:
            print("SUCESSO: Zero valores nulos encontrados.")
        else:
            print(f"FALHA: Encontrados {total_nulos} valores nulos!")
            print(df.isnull().sum()[df.isnull().sum() > 0])

        # Validação de Colunas
        cols_presentes = all(col in df.columns for col in REQUIRED_COLUMNS)
        if cols_presentes:
            print("SUCESSO: Todas as 25 colunas obrigatórias estão presentes.")
        else:
            missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
            print(f"FALHA: Faltando colunas: {missing}")

        # Retorno da padronização p/ teste
        print("-" * 60)
        print("VERIFICAÇÃO VISUAL:")
        print(f"   > Canal (Minúsculo):   '{df['canal_venda'].iloc[0]}'")
        print(f"   > Cliente (Title):     '{df['nome_cliente'].iloc[0]}'")
        print(f"   > Estado (Maiúsculo):  '{df['estado_cliente'].iloc[0]}'")
        print("-" * 60)

    except Exception as e:
        print(f"\nERRO DURANTE O PROCESSO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()