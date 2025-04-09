# Análise de Rede de Emails

## Visão Geral
Ferramenta para construção e análise de grafos baseados em comunicações por email, transformando dados de remetentes e destinatários em uma rede direcionada e ponderada.

## Funcionalidades

### Geração de Grafo
- Construção de grafo direcionado e ponderado a partir de dados de emails
- Armazenamento em formato de texto para análise posterior

### Métricas e Análises
- **Métricas Básicas**: Ordem (nº de vértices), tamanho (nº de arestas) e vértices isolados
- **Centralidade**: Identificação dos 20 indivíduos com maior grau de entrada e saída
- **Visualização**: Exibição organizada das métricas e resultados

## Estrutura do Projeto
```
/
├── controller/       # Lógica de controle da aplicação
├── models/           # Estruturas de dados e persistência
├── utils/            # Utilitários e ferramentas auxiliares
├── data/             # Dados brutos e processados
├── views/            # Interface com usuário (opcional)
└── main.py           # Ponto de entrada da aplicação
```

## Tecnologias
- Python
- Estruturas de dados em grafos
- Análise de rede social

## Como Usar

1. Execute o programa:
```
python main.py
```

2. Selecione uma opção:
   - **Gerar novo**: Cria um novo grafo a partir dos dados
   - **Extrair informações**: Mostra métricas e análises do grafo
   
## Autores
Desenvolvido como projeto acadêmico para análise de redes.