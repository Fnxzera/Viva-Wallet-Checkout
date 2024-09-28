from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Configurações da API Viva Wallet
VIVA_API_URL = "https://demo-api.vivapayments.com"
VIVA_AUTH_URL = "https://demo-accounts.vivapayments.com/connect/token"
CLIENT_ID = 'a98acf6c-0832-4ef1-abe1-b96aaa613c7a'  
CLIENT_SECRET = '2756t6v030z3ycmG1rep61s5GrH0qQ' 

# Rota da página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para criar o pedido de pagamento e redirecionar para o checkout Viva Wallet
@app.route('/checkout', methods=['POST'])
def checkout():
    amount = int(request.form.get('amount' ))  # Valor padrão de 10,00 EUR
    description = request.form.get('description', 'Pagamento na loja')

    # Obter o token de autenticação
    auth_token = token_prov
    print(f"Token obtido: {auth_token}")
    if not auth_token:
        return "Erro ao obter token de autenticação", 500

    # Criar pedido de pagamento
    order_code = create_viva_order(auth_token, amount, description)
    
    
    if not order_code:
        return "Erro ao criar pedido", 500  # Se order_code é None, retorna erro

    # Redirecionar para a página de checkout da Viva Wallet
    checkout_url = f"https://demo.vivapayments.com/web/checkout?ref={order_code}"
    return redirect(checkout_url)
# Função para obter o token de autenticação
def get_viva_token():
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,       # Merchant ID
        'client_secret': CLIENT_SECRET  # API Key
    }

    try:
        response = requests.post(VIVA_AUTH_URL, data=auth_data)
        response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
        return response.json().get('access_token')
    except requests.RequestException as e:
        print(f"Erro ao obter token: {e}")
        print(f"Resposta da API: {response.text}")  # Mostra o conteúdo da resposta para diagnóstico
        return None
# Função para criar o pedido de pagamento no Viva Wallet
def create_viva_order(token, amount, description):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    order_data = {
        "amount": amount,  # Valor em centavos (1000 = 10 EUR)
        "customerTrns": description,  # Descrição da transação
        "paymentTimeout": 300  # Timeout de pagamento em segundos
    }
    print(f"Dados do pedido: {order_data}")
    try:
        response = requests.post(f"{VIVA_API_URL}/checkout/v2/orders", json=order_data, headers=headers)
        response.raise_for_status()
        return response.json().get('orderCode')
    except requests.RequestException as e:
        print(f"Erro ao criar pedido: {e}")
        return None
    

token_prov = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjBEOEZCOEQ2RURFQ0Y1Qzk3RUY1MjdDMDYxNkJCMjMzM0FCNjVGOUZSUzI1NiIsIng1dCI6IkRZLTQxdTNzOWNsLTlTZkFZV3V5TXpxMlg1OCIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2RlbW8tYWNjb3VudHMudml2YXBheW1lbnRzLmNvbSIsIm5iZiI6MTcyNzQzNTgyNiwiaWF0IjoxNzI3NDM1ODI2LCJleHAiOjE3Mjc0Mzk0MjYsImF1ZCI6WyJjb3JlX2FwaSIsImh0dHBzOi8vZGVtby1hY2NvdW50cy52aXZhcGF5bWVudHMuY29tL3Jlc291cmNlcyJdLCJzY29wZSI6WyJ1cm46dml2YTpwYXltZW50czpjb3JlOmFwaTphY3F1aXJpbmciLCJ1cm46dml2YTpwYXltZW50czpjb3JlOmFwaTphY3F1aXJpbmc6Y2FyZHRva2VuaXphdGlvbiIsInVybjp2aXZhOnBheW1lbnRzOmNvcmU6YXBpOmFjcXVpcmluZzp0cmFuc2FjdGlvbnMiLCJ1cm46dml2YTpwYXltZW50czpjb3JlOmFwaTpyZWRpcmVjdGNoZWNrb3V0Il0sImNsaWVudF9pZCI6Ijh4Z2tndnk5N2F6NXYyZnE2cjRzMTQzYzl0ZHF3azFuMDZtd3FkZHR3cjY4Ni5hcHBzLnZpdmFwYXltZW50cy5jb20iLCJ1cm46dml2YTpwYXltZW50czpjbGllbnRfcGVyc29uX2lkIjoiMTgxQkM2NDktRThBNC00M0FCLTk3MEQtN0NCODY3NUQ1NjQ1In0.EjZeiSgGmqUhaLOOi0CAOQmaW8XYzXLFvdE2P15QsVMq4Rs1pij6uGQ_t4EsDm6bPyK_9Vv3SfIk3IFSU6KJto9sP__Rp2V3e4UKS1o-w0LrYTSESPJbT1LTrzY_Y8V5FzPHpZAJIcR85quVVghqJ_LlO7t2DM_KDUguDhXl_WHi2A2FqIT_8GMKbvYEYNAD-O3bPa7ppqLO7zpBlfJgnp7AVYmzCbcB81Tfm_32E0HRRS8sVLzMEbZBhJKYoyRC9gXKIvM7dithrII5BsfwFW0xAfcGUKelQOo-Eua8iqySt794qzAkem_32TXriLaCovYSlHjJsnqCOuG0vbb94w"

# Rota de retorno para exibir sucesso ou falha
@app.route('/success')
def success():
    return "Pagamento realizado com sucesso!"

@app.route('/failure')
def failure():
    return "Falha no pagamento."

if __name__ == '__main__':
    app.run(debug=True)
