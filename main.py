import pandas as pd
import os
import re

arquivos_nubank = 'NUBANK'
arquivos_stone = 'STONE'
arquivos_viacredi = 'VIACREDI'

def processarNubank(input_file):
    arquivos_xlsx = [f for f in os.listdir(arquivos_nubank) if f.endswith('.xlsx')]
    input_df = pd.read_excel(input_file)
    resultados = []

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(arquivos_nubank, arquivo)
        df = pd.read_excel(caminho_arquivo)
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

def processarStone(input_file):
    arquivos_xlsx = [f for f in os.listdir(arquivos_stone) if f.endswith('.xlsx')]

    try:
        input_df = pd.read_excel(input_file, usecols=['DESCRICAO', 'HISTORICO', 'CREDITO', 'DEBITO'], dtype=str)
    except Exception as e:
        return pd.DataFrame()

    resultados = []

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(arquivos_stone, arquivo)
        try:
            df = pd.read_excel(caminho_arquivo, skiprows=2, header=None)
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

        if 'DATA_PAGAMENTO' in resultado_final.columns:
            resultado_final['DATA_PAGAMENTO'] = pd.to_datetime(
                resultado_final['DATA_PAGAMENTO'], errors='coerce'
            ).dt.strftime('%d/%m/%Y')

        resultado_final.to_excel('resultado_stone.xlsx', index=False, header=False)
        return resultado_final
    else:
        return pd.DataFrame()

def processarViacredi(input_file):
    arquivos_xlsx = [f for f in os.listdir(arquivos_viacredi) if f.endswith('.xlsx')]
    input_df = pd.read_excel(input_file)
    resultados = []

    for arquivo in arquivos_xlsx:
        caminho_arquivo = os.path.join(arquivos_viacredi, arquivo)
        df = pd.read_excel(caminho_arquivo)
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

input_file = 'input.xlsx'
processarNubank(input_file)
processarStone(input_file)
processarViacredi(input_file)
