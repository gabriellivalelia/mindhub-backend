"""
Dados geográficos (estados e cidades) do Brasil.

⚠️ DEPRECATED: Este arquivo não é mais utilizado.
Os dados geográficos agora são obtidos automaticamente da API do IBGE.

Veja: src/infra/services/ibge_service.py
"""

# Mantido apenas para referência histórica
STATES_AND_CITIES = [
    {
        "name": "Minas Gerais",
        "abbreviation": "MG",
        "cities": [
            "Belo Horizonte",
            "Uberlândia",
            "Contagem",
            "Juiz de Fora",
            "Betim",
            "Montes Claros",
            "Ribeirão das Neves",
            "Uberaba",
            "Governador Valadares",
            "Ipatinga",
            "Sete Lagoas",
            "Divinópolis",
            "Santa Luzia",
        ],
    },
    {
        "name": "São Paulo",
        "abbreviation": "SP",
        "cities": [
            "São Paulo",
            "Guarulhos",
            "Campinas",
            "São Bernardo do Campo",
            "Santo André",
            "Osasco",
            "São José dos Campos",
            "Ribeirão Preto",
            "Sorocaba",
            "Santos",
        ],
    },
    {
        "name": "Rio de Janeiro",
        "abbreviation": "RJ",
        "cities": [
            "Rio de Janeiro",
            "São Gonçalo",
            "Duque de Caxias",
            "Nova Iguaçu",
            "Niterói",
            "Belford Roxo",
            "Campos dos Goytacazes",
            "São João de Meriti",
            "Petrópolis",
            "Volta Redonda",
        ],
    },
    {
        "name": "Bahia",
        "abbreviation": "BA",
        "cities": [
            "Salvador",
            "Feira de Santana",
            "Vitória da Conquista",
            "Camaçari",
            "Juazeiro",
            "Ilhéus",
            "Itabuna",
            "Lauro de Freitas",
            "Jequié",
            "Alagoinhas",
        ],
    },
    {
        "name": "Paraná",
        "abbreviation": "PR",
        "cities": [
            "Curitiba",
            "Londrina",
            "Maringá",
            "Ponta Grossa",
            "Cascavel",
            "São José dos Pinhais",
            "Foz do Iguaçu",
            "Colombo",
            "Guarapuava",
            "Paranaguá",
        ],
    },
    {
        "name": "Rio Grande do Sul",
        "abbreviation": "RS",
        "cities": [
            "Porto Alegre",
            "Caxias do Sul",
            "Pelotas",
            "Canoas",
            "Santa Maria",
            "Gravataí",
            "Viamão",
            "Novo Hamburgo",
            "São Leopoldo",
            "Rio Grande",
        ],
    },
    {
        "name": "Pernambuco",
        "abbreviation": "PE",
        "cities": [
            "Recife",
            "Jaboatão dos Guararapes",
            "Olinda",
            "Caruaru",
            "Petrolina",
            "Paulista",
            "Cabo de Santo Agostinho",
            "Camaragibe",
            "Garanhuns",
            "Vitória de Santo Antão",
        ],
    },
    {
        "name": "Ceará",
        "abbreviation": "CE",
        "cities": [
            "Fortaleza",
            "Caucaia",
            "Juazeiro do Norte",
            "Maracanaú",
            "Sobral",
            "Crato",
            "Itapipoca",
            "Maranguape",
            "Iguatu",
            "Quixadá",
        ],
    },
]
