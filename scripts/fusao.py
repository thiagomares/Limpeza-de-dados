import json
import csv
from typing import List

# Função para leitura de dados


def leitura_dados(path: str, tipo_arquivo: str) -> List[dict]:
    if tipo_arquivo == 'json':
        with open(path, 'r') as f:
            dados = json.load(f)
        return dados
    elif tipo_arquivo == 'csv':
        with open(path, 'r') as arquivo:
            spamreader = csv.DictReader(arquivo, delimiter=',')
            dados = []
            for linha in spamreader:
                dados.append(linha)
        return dados
    else:
        print('Tipo de arquivo não suportado')
        return None


def get_columns(dados: str) -> List[str]:
    return list(dados[0].keys())


def rename_colums(dados: List[dict], keymap: dict) -> List[dict]:
    new_dados = []

    for linha in dados:
        new_linha = {}
        for key, value in linha.items():
            new_linha[keymap[key]] = value
        new_dados.append(new_linha)
    return new_dados


def combinando_dados(**kwargs: List[dict]) -> List[dict]:
    registros = []
    for value in kwargs.values():
        registros.extend(value)
    return registros


def tratamento_colunas(dados: List[dict]) -> List[dict]:
    nome_colunas = list(dados[0].keys())

    tabela = [nome_colunas]

    for linhas in dados:
        linha = []
        for coluna in nome_colunas:
            linha.append(linhas.get(coluna, 'indisponível'))
        tabela.append(linha)
    return tabela


def insere_dados(dados: List[dict], nome_arquivo: str) -> None:
    with open(nome_arquivo, 'w') as arquivo:
        spamwriter = csv.writer(arquivo, delimiter=',')
        for linha in dados:
            spamwriter.writerow(linha)


# Carregando os dados
if __name__ == '__main__':
    path_json = 'data_raw/dados_empresaA.json'
    path_csv = 'data_raw/dados_empresaB.csv'
    dados_json = leitura_dados(path_json, 'json')
    dados_csv = leitura_dados(path_csv, 'csv')
    print(dados_json)
    print(dados_csv)
    print(get_columns(dados_csv))

    keymap = {  # nota mental: a chave é a lista que queremos mudar, a chave é o valor que entrará no lugar
        'Nome do Item': 'Nome do Produto',
        'Classificação do Produto': 'Categoria do Produto',
        'Valor em Reais (R$)': 'Preço do Produto (R$)',
        'Quantidade em Estoque': 'Quantidade em Estoque',
        'Nome da Loja': 'Filial',
        'Data da Venda': 'Data da Venda'}

    # Renomeando as colunas
    dados_csv = rename_colums(dados_csv, keymap)
    print(dados_csv)

    # Combinando os dados
    registros = combinando_dados(dados_csv=dados_csv, dados_json=dados_json)
    print(registros)

    # Tratando as colunas
    dados_tratados = tratamento_colunas(registros)

    # Inserindo os dados
    nome_arquivo = 'data_processed/dados_fusao.csv'
    insere_dados(dados_tratados, nome_arquivo)
