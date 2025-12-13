import sys
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.services.analytics_service import calcular_metricas_financeiras, calcular_metricas_vendas

def run_test():
    print("="*60)
    print("INICIANDO TESTE DO MÓDULO DE CÁLCULOS (TASK 5)")
    print("="*60)

    # 1. Criar um DataFrame Fictício (Mock)
    dados = {
        "valor_final": [100.0, 200.0, 300.0],  # Total: 600
        "margem_lucro": [20.0, 30.0, 50.0]     # Margens: 20%, 30%, 50%
        # Lucros esperados: 
        # 100 * 0.20 = 20
        # 200 * 0.30 = 60
        # 300 * 0.50 = 150
        # Total Lucro = 230
    }
    df_teste = pd.DataFrame(dados)

    print("DataFrame de Teste:")
    print(df_teste)
    print("-" * 60)

    # 2. Testar Métricas Financeiras
    financas = calcular_metricas_financeiras(df_teste)
    print("Resultados Financeiros:")
    print(f"   > Receita Esperada: 600.0 | Calculada: {financas['receita_liquida']}")
    print(f"   > Lucro Esperado:   230.0 | Calculado: {financas['lucro_bruto']}")
    
    # Validação (Asserts simples)
    if financas['receita_liquida'] == 600.0 and financas['lucro_bruto'] == 230.0:
        print("SUCESSO: Cálculos financeiros corretos.")
    else:
        print("ERRO: Cálculos financeiros divergentes!")

    print("-" * 60)

    # 3. Testar Métricas de Vendas
    vendas = calcular_metricas_vendas(df_teste)
    print("📈 Resultados de Vendas:")
    print(f"   > Nº Transações: 3     | Calculado: {vendas['numero_transacoes']}")
    print(f"   > Ticket Médio:  200.0 | Calculado: {vendas['media_por_transacao']}")

    if vendas['numero_transacoes'] == 3 and vendas['media_por_transacao'] == 200.0:
        print("SUCESSO: Cálculos de vendas corretos.")
    else:
        print("ERRO: Cálculos de vendas divergentes!")

    print("="*60)

if __name__ == "__main__":
    run_test()