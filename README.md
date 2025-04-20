# 📄 **Documentação – Processamento de Arquivos Financeiros (Nubank, Stone, Viacredi, MercadoPago)**

## 🧩 **Descrição Geral**

Este script automatiza o processamento de arquivos financeiros oriundos de diversas instituições (Nubank, Stone, Viacredi e MercadoPago). A partir de critérios definidos em um arquivo `input.xlsx`, ele filtra e organiza os dados contábeis para gerar relatórios finais no formato `.xlsx`.

---

## 📂 **Estrutura de Pastas Esperada**

* `NUBANK/` → arquivos .xlsx com extratos do Nubank
* `STONE/` → arquivos .xlsx com extratos da Stone
* `VIACREDI/` → arquivos .xlsx com extratos da Viacredi
* `MERCADOPAGO/` → arquivos .xlsx com extratos do Mercado Pago
* `input.xlsx` → arquivo com descrições, históricos e códigos contábeis para busca

---

## 📘 **Arquivo de Entrada (`input.xlsx`)**

### Colunas esperadas:

* `DESCRICAO`: texto que será buscado nas colunas de descrição dos extratos
* `HISTORICO`: código de histórico contábil
* `CREDITO`: código da conta de crédito
* `DEBITO`: código da conta de débito

---

## 🔧 **Funções Principais**

---

### 📌 `processarNubank(input_df)`

**Descrição:**

Filtra transações dos extratos do Nubank com base nas descrições do `input.xlsx`, adiciona códigos contábeis e exporta o resultado.

**Parâmetros:**

* `input_df` → DataFrame do `input.xlsx`

**Retorna:**

* DataFrame com os dados encontrados (ou vazio)

**Saída gerada:**

* `resultado_nubank.xlsx`

---

### 📌 `processarStone(input_df)`

**Descrição:**

Lê os extratos da Stone, calcula tarifas a partir do valor bruto e líquido, e realiza o mapeamento com base nas descrições do `input.xlsx`.

**Regras específicas:**

* Se for encontrada uma tarifa (diferença entre valor bruto e líquido), ela é contabilizada separadamente como débito `8534` e crédito `402`.

**Parâmetros:**

* `input_df` → DataFrame do `input.xlsx`

**Retorna:**

* DataFrame com os dados processados (ou vazio)

**Saída gerada:**

* `resultado_stone.xlsx`

---

### 📌 `processarViacredi(input_df)`

**Descrição:**

Filtra os extratos da Viacredi usando os critérios do `input.xlsx` e prepara os dados contábeis.

**Parâmetros:**

* `input_df` → DataFrame do `input.xlsx`

**Retorna:**

* DataFrame com os dados encontrados (ou vazio)

**Saída gerada:**

* `resultado_viacredi.xlsx`

---

### 📌 `processarMercadopago(pasta_mercado)`

**Descrição:**

Calcula o total líquido (NET) dos arquivos da pasta Mercado Pago e exporta um resumo com valor total.

**Parâmetros:**

* `pasta_mercado` → nome da pasta (string)

**Retorna:**

* DataFrame com o total por arquivo

**Saída gerada:**

* `resultado_mercadopago.xlsx`

---

## 🧠 **Lógica Principal do Script**

1. Verifica se existem arquivos `.xlsx` em cada uma das pastas esperadas.
2. Verifica se o arquivo `input.xlsx` é válido.
3. Executa os processamentos específicos por instituição.
4. Exporta os resultados em arquivos separados para cada fonte.

---

## ⚠️ **Tratamento de Erros e Avisos**

* Suprime `UserWarning` do módulo `openpyxl` para evitar ruído.
* Tenta carregar `input.xlsx` com tratamento de exceção.
* Ignora arquivos com colunas inesperadas ou dados inconsistentes.

---

## 📝 **Possíveis Melhorias Futuras**

* Unificar os arquivos finais em um único Excel com abas por instituição.
* Interface gráfica ou web para selecionar as pastas e visualizar os resultados.
* Testes automatizados para garantir integridade dos dados.
* Suporte a CSV além de XLSX.
