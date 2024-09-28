import requests
import base64

def get_viva_wallet_token():
    # Substitua pelas suas credenciais
    client_id = 'a98acf6c-0832-4ef1-abe1-b96aaa613c7a'
    client_secret = '2756t6v030z3ycmG1rep61s5GrH0qQ'

    # Codificando o client_id e client_secret em Base64
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # URL de autenticação do Viva Wallet (sandbox)
    auth_url = 'https://demo-accounts.vivapayments.com/connect/token'

    # Cabeçalhos
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }

    # Corpo da requisição
    data = {
        'grant_type': 'client_credentials'
    }

    # Fazendo a requisição
    response = requests.post(auth_url, headers=headers, data=data)

    # Verificando a resposta
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

# Chamando a função para obter o token
token = get_viva_wallet_token()

if token:
    print(f"Token de Acesso: {token}")