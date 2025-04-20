import pandas as pd
import os
import re
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Pastas
arquivos_nubank = 'NUBANK'
arquivos_stone = 'STONE'
arquivos_viacredi = 'VIACREDI'
arquivos_mercadopago = 'MERCADOPAGO'
input_file = 'input.xlsx'

def processarNubank(input_df):
    arquivos_xlsx = [f for f in os.listdir(arquivos_nubank) if f.endswith('.xlsx')]
    resultados = []

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(arquivos_nubank, arquivo)
        df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        df.columns = df.columns.str.replace(' ', '_').str.upper()

        if not {'DATA', 'VALOR', 'DESCRIÇÃO'}.issubset(df.columns):
            continue

        for _, row in input_df.iterrows():
            descricao_input = row['DESCRICAO'].strip()
            historico = row['HISTORICO']
            credito = row['CREDITO']
            debito = row['DEBITO']

            filtro = df['DESCRIÇÃO'].str.contains(descricao_input, case=False, na=False, regex=False)
            if filtro.any():
                df_filtrado = df[filtro]
                df_filtrado = df_filtrado.assign(
                    DEBITO=debito,
                    CREDITO=credito,
                    DESCRICAO=descricao_input,
                    HISTORICO=historico
                )
                if 'DATA' in df_filtrado.columns:
                    df_filtrado['DATA'] = pd.to_datetime(df_filtrado['DATA'], errors='coerce').dt.strftime('%d/%m/%Y')
                df_final = df_filtrado[['DATA', 'DEBITO', 'CREDITO', 'DESCRICAO', 'HISTORICO', 'VALOR']]
                resultados.append(df_final)

    if resultados:
        resultado_final = pd.concat(resultados, ignore_index=True)
        resultado_final.to_excel('resultado_nubank.xlsx', index=False, header=False)
        return resultado_final
    else:
        return pd.DataFrame()

def processarStone(input_df):
    arquivos_xlsx = [f for f in os.listdir(arquivos_stone) if f.endswith('.xlsx')]
    resultados = []

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(arquivos_stone, arquivo)
        try:
            df = pd.read_excel(caminho_arquivo, skiprows=2, header=None, engine='openpyxl')
            colunas_esperadas = ['DATA_PAGAMENTO', 'VALOR_LIQUIDO', 'DETALHES', 'COMENTARIO']
            if len(df.columns) >= len(colunas_esperadas):
                df.columns = colunas_esperadas
            else:
                continue

            def calcular_tarifa(row):
                detalhes = str(row.get('DETALHES', ''))
                valor_liquido = float(row.get('VALOR_LIQUIDO', 0))
                valor_transacao_match = re.search(r'R\$ ([\d.,]+)', detalhes)
                if valor_transacao_match:
                    valor_transacao = float(valor_transacao_match.group(1).replace('.', '').replace(',', '.'))
                    tarifa = valor_transacao - valor_liquido
                    return round(tarifa, 2) if tarifa > 0 else None
                return None

            df['TARIFA'] = df.apply(calcular_tarifa, axis=1)

            for _, row in input_df.iterrows():
                descricao_input = str(row['DESCRICAO']).strip()
                historico = str(row['HISTORICO']).strip() if pd.notna(row['HISTORICO']) else None
                credito = str(row['CREDITO']).strip() if pd.notna(row['CREDITO']) else ""
                debito = str(row['DEBITO']).strip() if pd.notna(row['DEBITO']) else ""

                filtro_regular = df['COMENTARIO'].str.contains(descricao_input, case=False, na=False, regex=False)
                if filtro_regular.any():
                    df_filtrado = df[filtro_regular].copy()

                    df_filtrado['DEBITO'] = debito
                    df_filtrado['CREDITO'] = credito
                    df_filtrado['DESCRICAO'] = descricao_input
                    df_filtrado['HISTORICO'] = historico
                    df_filtrado['VALOR'] = df_filtrado['VALOR_LIQUIDO']

                    df_filtrado = df_filtrado[df_filtrado['HISTORICO'].notna()]

                    if "Transferência entre contas PJ" not in descricao_input:
                        filtro_tarifa = df_filtrado['TARIFA'].notnull()
                        if filtro_tarifa.any():
                            df_tarifa = df_filtrado[filtro_tarifa].copy()
                            df_tarifa['DEBITO'] = '8534'
                            df_tarifa['CREDITO'] = '402'
                            df_tarifa['HISTORICO'] = '0'
                            df_tarifa['VALOR'] = df_tarifa['TARIFA']
                            df_tarifa = df_tarifa[['DATA_PAGAMENTO', 'DEBITO', 'CREDITO', 'DESCRICAO', 'HISTORICO', 'VALOR']]
                            resultados.append(df_tarifa)

                    df_filtrado = df_filtrado[['DATA_PAGAMENTO', 'DEBITO', 'CREDITO', 'DESCRICAO', 'HISTORICO', 'VALOR']]
                    resultados.append(df_filtrado)
        except Exception as e:
            pass

    if resultados:
        resultado_final = pd.concat(resultados, ignore_index=True)
        resultado_final['DATA_PAGAMENTO'] = pd.to_datetime(resultado_final['DATA_PAGAMENTO'], errors='coerce').dt.strftime('%d/%m/%Y')
        resultado_final.to_excel('resultado_stone.xlsx', index=False, header=False)
        return resultado_final
    else:
        return pd.DataFrame()

def processarViacredi(input_df):
    arquivos_xlsx = [f for f in os.listdir(arquivos_viacredi) if f.endswith('.xlsx')]
    resultados = []

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(arquivos_viacredi, arquivo)
        df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        df.columns = df.columns.str.replace(' ', '_').str.upper()

        if not {'DATA', 'VALOR', 'DESCRIÇÃO'}.issubset(df.columns):
            continue

        for _, row in input_df.iterrows():
            descricao_input = row['DESCRICAO'].strip()
            historico = row['HISTORICO']
            credito = row['CREDITO']
            debito = row['DEBITO']

            filtro = df['DESCRIÇÃO'].str.contains(descricao_input, case=False, na=False, regex=False)
            if filtro.any():
                df_filtrado = df[filtro]
                df_filtrado = df_filtrado.assign(
                    DEBITO=debito,
                    CREDITO=credito,
                    DESCRICAO=descricao_input,
                    HISTORICO=historico
                )
                if 'DATA' in df_filtrado.columns:
                    df_filtrado['DATA'] = pd.to_datetime(df_filtrado['DATA'], errors='coerce').dt.strftime('%d/%m/%Y')
                df_final = df_filtrado[['DATA', 'DEBITO', 'CREDITO', 'DESCRICAO', 'HISTORICO', 'VALOR']]
                resultados.append(df_final)

    if resultados:
        resultado_final = pd.concat(resultados, ignore_index=True)
        resultado_final.to_excel('resultado_viacredi.xlsx', index=False, header=False)
        return resultado_final
    else:
        return pd.DataFrame()

def processarMercadopago(pasta_mercado):
    arquivos_xlsx = [f for f in os.listdir(pasta_mercado) if f.endswith('.xlsx')]
    resultados = []

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(pasta_mercado, arquivo)
        df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        df.columns = df.columns.str.upper().str.strip()

        if 'NET' in df.columns:
            
            df['NET'] = pd.to_numeric(
                df['NET'].astype(str).str.replace(',', '.'), 
                errors='coerce'
            )

            soma_net = df['NET'].sum()
            resultado = pd.DataFrame({'DESCRICAO': ['TOTAL MERCADO PAGO'], 'VALOR': [soma_net]})
            resultados.append(resultado)


    if resultados:
        resultado_final = pd.concat(resultados, ignore_index=True)
        resultado_final.to_excel('resultado_mercadopago.xlsx', index=False)
        return resultado_final
    else:
        return pd.DataFrame()

# ----------- Execução principal -----------

tem_nubank = os.path.isdir(arquivos_nubank) and any(f.endswith('.xlsx') for f in os.listdir(arquivos_nubank))
tem_stone = os.path.isdir(arquivos_stone) and any(f.endswith('.xlsx') for f in os.listdir(arquivos_stone))
tem_viacredi = os.path.isdir(arquivos_viacredi) and any(f.endswith('.xlsx') for f in os.listdir(arquivos_viacredi))
tem_mercadopago = os.path.isdir(arquivos_mercadopago) and any(f.endswith('.xlsx') for f in os.listdir(arquivos_mercadopago))

input_df = None
if (tem_nubank or tem_stone or tem_viacredi) and os.path.isfile(input_file):
    try:
        input_df = pd.read_excel(input_file, engine='openpyxl')
    except Exception as e:
        print(f"Erro ao carregar input.xlsx: {e}")
        input_df = None

if (tem_nubank or tem_stone or tem_viacredi) and input_df is None:
    print("Input.xlsx necessário, mas ausente ou inválido. Pulando Nubank, Stone e Viacredi.")
    tem_nubank = tem_stone = tem_viacredi = False

if tem_nubank:
    processarNubank(input_df)

if tem_stone:
    processarStone(input_df)

if tem_viacredi:
    processarViacredi(input_df)

if tem_mercadopago:
    processarMercadopago(arquivos_mercadopago)

if not any([tem_nubank, tem_stone, tem_viacredi, tem_mercadopago]):
    print("Nenhum arquivo encontrado em nenhuma pasta. Nada para processar.")
