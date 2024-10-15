from sales_order_automation import iniciar_navegador, login_community, login_sales_order, acessar_pagina_sales_order, processar_tabela

def main():
    # inicializa o navegador
    navegador = iniciar_navegador()

    # faz login na plataforma
    email = 'hevila.thereza@gmail.com'
    senha = 'cji!mN0402'
    login_community(navegador, email, senha)

    # faz login no sales order
    usuario = 'douglasmcgee@catchycomponents.com'
    senha_sales_order = 'i7D32S&37K*W'
    login_sales_order(navegador, usuario, senha_sales_order)

    # acessa a página de sales orders
    acessar_pagina_sales_order(navegador)

    # processa a tabela de pedidos
    processar_tabela(navegador)

    # finaliza o navegador
    navegador.quit()

# executa o main
if __name__ == "__main__":
    main()
