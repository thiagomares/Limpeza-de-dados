class Dados:
    def __init__(self, path, tipo_arquivo):
        self.path = path
        self.tipo_arquivo = tipo_arquivo
        self.dados = self.leitura_dados()
        self.columns = self.get_columns()
        self.qtd_linhas = self.size_data

    def leitura_dados(self):
        if self.tipo_arquivo == 'json':
            import json
            with open(self.path, 'r') as f:
                dados = json.load(f)
            return dados
        elif self.tipo_arquivo == 'csv':
            import csv
            with open(self.path, 'r') as arquivo:
                spamreader = csv.DictReader(arquivo, delimiter=',')
                dados = []
                for linha in spamreader:
                    dados.append(linha)
            return dados
        elif self.tipo_arquivo == 'list':
            dados = self.path
            self.path = 'Lista em memoria'
            return dados
        else:
            print('Tipo de arquivo não suportado')
            return None

    def get_columns(self):
        return list(self.dados[0].keys())
    
    def rename_colums(self, keymap):
        new_dados = []

        for linha in self.dados:
            new_linha = {}
            for key, value in linha.items():
                new_linha[keymap[key]] = value
            new_dados.append(new_linha)
        
        self.dados = new_dados
        self.columns = self.get_columns()
        
    
    def size_data(self):
        return len(self.dados)
    
    
    def join(lista_dados, lista_dados2):
        registros = []
        registros.extend(lista_dados)
        registros.extend(lista_dados2)
        return Dados(registros, 'list')
    
    def tratamento_colunas(self):
        dados_combinados = [self.columns]
        
        for row in self.dados:
            linha = []
            for coluna in self.columns:
                linha.append(row.get(coluna, 'indisponível'))
            dados_combinados.append(linha)
        return dados_combinados
    
    def insere_dados(self, nome_arquivo):
        import csv
        
        dados_combinados = self.tratamento_colunas()
        
        with open(nome_arquivo, 'w') as arquivo:
            spamwriter = csv.writer(arquivo, delimiter=',')
            spamwriter.writerows(dados_combinados)
        
    

dados_empresaA = Dados('data_raw/dados_empresaA.json', 'json')
dados_empresaB = Dados('data_raw/dados_empresaB.csv', 'csv')

keymap = {  # nota mental: a chave é a lista que queremos mudar, a chave é o valor que entrará no lugar
        'Nome do Item': 'Nome do Produto',
        'Classificação do Produto': 'Categoria do Produto',
        'Valor em Reais (R$)': 'Preço do Produto (R$)',
        'Quantidade em Estoque': 'Quantidade em Estoque',
        'Nome da Loja': 'Filial',
        'Data da Venda': 'Data da Venda'}

dados_empresaB.rename_colums(keymap=keymap)

print(dados_empresaA.size_data())
print(dados_empresaB.size_data())

dados_fusao = Dados.join(dados_empresaB.dados, dados_empresaA.dados)
print(dados_fusao.size_data())

print(dados_empresaB.get_columns())
print(dados_empresaA.get_columns())
dados_fusao.insere_dados('data_processed/dados_fusao.csv')
