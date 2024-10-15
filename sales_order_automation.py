from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# inicializar o navegador
def iniciar_navegador():
    """configura e retorna o navegador."""
    service = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=service)
    return navegador

# função de login no sistema
def login_community(navegador, email, senha):
    """realiza o login na plataforma de sales order."""
    navegador.get('https://pathfinder.automationanywhere.com/challenges/salesorder-applogin.html#')
    sleep(3)
    
    # aceitar cookies e fazer login
    navegador.find_element('id', 'onetrust-accept-btn-handler').click()
    navegador.find_element('id', 'button_modal-login-btn__iPh6x').click()
    sleep(1)
    navegador.find_element('id', '43:2;a').send_keys(email)
    navegador.find_element('xpath', '//button[text()="Next"]').click()
    sleep(1)
    navegador.find_element('id', '10:150;a').send_keys(senha)
    navegador.find_element('xpath', '//button[text()="Log in"]').click()
    sleep(2)

# função para login no sales order
def login_sales_order(navegador, usuario, senha):
    """faz login no sistema sales order."""
    navegador.find_element('id', 'salesOrderInputEmail').send_keys(usuario)
    navegador.find_element('id', 'salesOrderInputPassword').send_keys(senha)
    navegador.find_element('xpath', '/html/body/div/div[1]/div/div/div/div/div[2]/div/form/a').click()
    sleep(1)

# função para acessar a página de pedidos
def acessar_pagina_sales_order(navegador):
    """navega até a página de sales order e ajusta a visualização para 50 linhas."""
    navegador.find_element('xpath', '//*[@id="accordionSidebar"]/li[6]/a').click()
    navegador.find_element('xpath', '//*[@id="salesOrderDataTable_length"]/label/select').send_keys('50')
    sleep(2)

# função para processar a tabela de pedidos
def processar_tabela(navegador):
    """processa as linhas da tabela de pedidos e verifica status e tracking."""
    total_linhas = len(navegador.find_elements('xpath', '//*[@id="salesOrderDataTable"]/tbody/tr'))
    print(f"total de linhas: {total_linhas}")

    for i in range(1, total_linhas + 1):
        try:
            processar_linha(navegador, i)
        except Exception as e:
            print(f"erro ao processar a linha {i}: {str(e)}")

# função para processar uma linha individual
def processar_linha(navegador, i):
    """processa uma linha da tabela de sales order."""
    row = navegador.find_element('xpath', f'//*[@id="salesOrderDataTable"]/tbody/tr[{i}]')
    order_status = row.find_element('xpath', './/td[5]').text
    print(f"linha {i} com status: {order_status}")

    if order_status in ["Confirmed", "Delivery Outstanding"]:
        expandir_detalhes_pedido(navegador, i)

# função para expandir os detalhes de um pedido e verificar os tracking numbers
def expandir_detalhes_pedido(navegador, i):
    """expande a linha da tabela e verifica os tracking numbers."""
    navegador.find_element('xpath', f'//*[@id="salesOrderDataTable"]/tbody/tr[{i}]/td[1]').click()
    sleep(1)
    
    tracking_numbers = navegador.find_elements('xpath', f'//*[@id="salesOrderDataTable"]/tbody/tr[{i+1}]//td/table/tbody/tr/td[2]')
    tracking_list = [tn.text for tn in tracking_numbers]
    print(f"tracking numbers: {tracking_list}")

    all_delivered = verificar_tracking_numbers(navegador, tracking_list)
    
    if all_delivered:
        gerar_fatura(navegador, i)
    else:
        navegador.close()
        navegador.switch_to.window(navegador.window_handles[0])
        cancelar_pedido(navegador, i)

# função para verificar o status dos tracking numbers
def verificar_tracking_numbers(navegador, tracking_list):
    """verifica o status de cada tracking number e retorna se todos estão 'delivered'."""
    all_delivered = True

    for tracking_number in tracking_list:
        navegador.execute_script("window.open('');")
        navegador.switch_to.window(navegador.window_handles[1])
        navegador.get("https://pathfinder.automationanywhere.com/challenges/salesorder-tracking.html")
        sleep(2)

        navegador.find_element('id', 'inputTrackingNo').send_keys(tracking_number)
        navegador.find_element('id', 'btnCheckStatus').click()
        sleep(2)

        try:
            delivery_status = navegador.find_element('xpath', '//*[@id="shipmentStatus"]/tr[3]/td[2]').text
            print(f"status de {tracking_number}: {delivery_status}")
            if delivery_status != "Delivered":
                all_delivered = False
                break
        except:
            print(f"erro ao verificar o status de {tracking_number}.")
            all_delivered = False
            break

        navegador.close()
        navegador.switch_to.window(navegador.window_handles[0])

    return all_delivered

# função para gerar a fatura
def gerar_fatura(navegador, i):
    """gera a fatura se todos os pacotes forem entregues."""
    navegador.find_element('xpath', f'//*[@id="salesOrderDataTable"]/tbody/tr[{i+1}]/td/table/tfoot/tr/td/button[1]').click()
    print("fatura gerada.")
    sleep(2)

# função para cancelar o pedido
def cancelar_pedido(navegador, i):
    """cancela o pedido caso nem todos os pacotes tenham sido entregues."""
    navegador.find_element('xpath', f'//*[@id="salesOrderDataTable"]/tbody/tr[{i+1}]/td/table/tfoot/tr/td/button[2]').click()
    print("pedido cancelado.")
    sleep(2)
