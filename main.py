import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Defina o URL do seu webhook no Bitrix24
WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/"

# Função para buscar a cidade e UF via API pública (ViaCEP)
def get_city_and_uf(cep):
    print(f"Consultando o CEP: {cep}")  # Log: indicando que estamos consultando o CEP
    cep = cep.replace("-", "")  # Remover o traço do CEP
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cidade = data.get("localidade", "")
        uf = data.get("uf", "")
        print(f"Resposta da API ViaCEP - Cidade: {cidade}, UF: {uf}")  # Log: mostrando a cidade e UF retornados
        return cidade, uf
    else:
        print(f"Erro ao consultar o CEP {cep}: {response.status_code}")  # Log de erro
        return None, None

# Função para atualizar os campos no Bitrix24
def update_bitrix24_record(record_id, cidade, uf):
    print(f"Atualizando o Bitrix24 com Cidade: {cidade}, UF: {uf} para o registro {record_id}...")  # Log
    # O endpoint correto para atualizar um "deal" no Bitrix24 é o "crm.deal.update"
    url = f"{WEBHOOK_URL}crm.deal.update.json"

    # Estrutura do payload para a atualização
    payload = {
        'ID': record_id,  # ID do registro do "deal" que queremos atualizar
        'FIELDS': {
            'UF_CRM_1731588487': cidade,  # Campo Cidade
            'UF_CRM_1731589190': uf,      # Campo UF
        }
    }

    # Realizando a requisição POST para o Bitrix24
    response = requests.post(url, json=payload)
    
    # Log detalhado da resposta da API Bitrix24
    print(f"Resposta da API Bitrix24: {response.status_code} - {response.text}")  # Log detalhado da resposta

    if response.status_code == 200:
        # Confirmando a atualização
        print(f"Registro {record_id} atualizado com sucesso!")
    else:
        # Caso contrário, log de erro detalhado
        print(f"Erro ao atualizar o registro no Bitrix24: {response.status_code} - {response.text}")

# Endpoint da API para atualizar cidade e UF a partir de um CEP
@app.route('/atualizar_cidade_uf', methods=['POST'])
def atualizar_cidade_uf():
    try:
        # Recupera os dados da requisição
        data = request.json
        print(f"Dados recebidos: {data}")  # Log: mostrando os dados recebidos
        record_id = data.get("record_id")
        cep = data.get("cep")

        # Verifica se ambos os parâmetros foram fornecidos
        if not record_id or not cep:
            print(f"Parâmetros inválidos: record_id={record_id}, cep={cep}")  # Log de erro
            return jsonify({"erro": "Parâmetros obrigatórios não fornecidos"}), 400

        # Passo 1: Consultar a cidade e UF pelo CEP
        cidade, uf = get_city_and_uf(cep)

        if cidade and uf:
            # Passo 2: Atualizar o registro no Bitrix24 com cidade e UF
            update_bitrix24_record(record_id, cidade, uf)
            return jsonify({"sucesso": f"Registro {record_id} atualizado com sucesso!"}), 200
        else:
            print("Erro ao obter cidade e UF para o CEP!")  # Log de erro
            return jsonify({"erro": "Não foi possível obter dados para o CEP"}), 400

    except Exception as e:
        print(f"Erro inesperado: {e}")  # Log de erro inesperado
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7964)
