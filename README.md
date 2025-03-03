# Processamento de Dados Financeiros - Nubank, Stone, Viacredi

Este repositório contém um script em Python para processar arquivos de dados financeiros de três instituições bancárias: **Nubank**, **Stone** e **Viacredi**. O script é projetado para comparar e filtrar informações contidas nos arquivos das instituições financeiras com base em um arquivo de entrada fornecido pelo usuário, além de realizar cálculos como tarifas de transações.

## Funcionalidade

O código executa o seguinte processamento:

- **Nubank**: Filtra e organiza transações bancárias baseadas na descrição do arquivo de entrada e adiciona informações de débito e crédito.
- **Stone**: Realiza o mesmo processamento, com a adição do cálculo de tarifas associadas às transações, e filtra os dados conforme a descrição.
- **Viacredi**: Processa os dados de forma semelhante às outras instituições, com filtragem por descrição e adição de dados financeiros como débito e crédito.

Para cada instituição, o script gera um arquivo `.xlsx` com os resultados, que contém as seguintes colunas: `DATA`, `DEBITO`, `CREDITO`, `DESCRICAO`, `HISTORICO` e `VALOR`.

## Pré-requisitos

- Python 3.x
- Bibliotecas necessárias:
  - pandas
  - re
  - os

Você pode instalar as dependências necessárias utilizando o seguinte comando:

```bash
pip install pandas
