REQUIRED_COLUMNS = [
    # Vendas
    "id_transacao", "data_venda", "valor_final", "subtotal", 
    "desconto_percent", "canal_venda", "forma_pagamento",
    # Clientes
    "cliente_id", "nome_cliente", "idade_cliente", "genero_cliente", 
    "cidade_cliente", "estado_cliente", "renda_estimada",
    # Produtos
    "produto_id", "nome_produto", "categoria", "marca", 
    "preco_unitario", "quantidade", "margem_lucro",
    # Logística
    "regiao", "status_entrega", "tempo_entrega_dias", "vendedor_id"
]

# Colunas Críticas (Se for nulo, a linha é descartada)
CRITICAL_COLUMNS = ["id_transacao", "valor_final", "data_venda"]

# Colunas para padronizar como maiúsculas (Códigos e Siglas)
UPPERCASE_COLUMNS = [
    "genero_cliente", "estado_cliente", "regiao", 
    "id_transacao", "cliente_id", "produto_id", "vendedor_id"
]

# Colunas para padronizar como minúsculas (Categorias fixas)
LOWERCASE_COLUMNS = [
    "canal_venda", "forma_pagamento", "categoria", "status_entrega"
]

# Colunas para Title Case (com primeira letra maiúscula em cada palavra, pra ser melhor exibido em relatórios)
TITLECASE_COLUMNS = [
    "nome_cliente", "cidade_cliente", "nome_produto", "marca"
]