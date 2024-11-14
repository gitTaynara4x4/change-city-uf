import requests

# Defina o URL do seu webhook no Bitrix24
WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/"

# Função para buscar a cidade e UF via API pública (ViaCEP)
def get_city_and_uf(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        cidade = data.get("localidade", "")
        uf = data.get("uf", "")
        return cidade, uf
    else:
        print(f"Erro ao consultar o CEP: {cep}")
        return None, None

# Função para obter o CEP de um registro no Bitrix24
def get_cep_from_bitrix24(record_id):
    # API REST do Bitrix24 para obter os campos de um registro
    url = f"https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.get.json"
    
    params = {
        "ID": record_id
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Pegando o CEP do campo UF_CRM_1700661314351
        cep = data.get('result', {}).get('UF_CRM_1700661314351', '')
        return cep
    else:
        print(f"Erro ao buscar dados do registro no Bitrix24: {response.status_code}")
        return None

# Função para atualizar os campos no Bitrix24
def update_bitrix24_record(record_id, cidade, uf):
    # Dados a serem enviados para o Bitrix24
    payload = {
        'ID': record_id,
        'fields': {
            'UF_CRM_1731588487': cidade,  # Campo Cidade
            'UF_CRM_1731589190': uf,      # Campo UF
        }
    }

    # Enviar a atualização via o webhook
    response = requests.post(WEBHOOK_URL, json=payload)
    
    if response.status_code == 200:
        print(f"Registro atualizado com sucesso para o ID {record_id}")
    else:
        print(f"Erro ao atualizar o registro: {response.status_code}")

# Função principal para pegar o CEP e fazer a atualização
def main():
    # Aqui você pode capturar o ID do registro, por exemplo:
    record_id = 12345  # O ID do registro que você deseja atualizar
    
    # Passo 1: Obter o CEP do Bitrix24
    cep = get_cep_from_bitrix24(record_id)
    
    if cep:
        # Passo 2: Consultar a cidade e UF pelo CEP
        cidade, uf = get_city_and_uf(cep)
        
        if cidade and uf:
            # Passo 3: Atualizar o registro no Bitrix24 com cidade e UF
            update_bitrix24_record(record_id, cidade, uf)
        else:
            print(f"Não foi possível obter dados para o CEP: {cep}")
    else:
        print("Não foi possível obter o CEP do registro.")

if __name__ == "__main__":
    main()
