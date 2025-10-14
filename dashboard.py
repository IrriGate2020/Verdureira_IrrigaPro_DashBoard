import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# --- 1. Carregamento e Limpeza dos Dados ---
try:
    # Leitura dos arquivos CSV
    df_ec = pd.read_csv("Tabela EC-1760452721432.csv", delimiter=';', low_memory=False)
    df_ph = pd.read_csv("Tabela PH-1760455118242.csv", delimiter=';', low_memory=False)

    # --- Processamento DF EC ---
    colunas_horas_ec = ["Hora lig 1", "Hora lig 2", "Hora lig 3"]
    for col in colunas_horas_ec:
        df_ec[col] = pd.to_numeric(df_ec[col].astype(str).str.replace(',', '.'), errors='coerce')
    df_ec["Date and Time"] = pd.to_datetime(df_ec["Date and Time"], errors='coerce')
    df_ec["EC da água"] = pd.to_numeric(df_ec["EC da água"].astype(str).str.replace(',', '.'), errors='coerce')
    df_ec.dropna(subset=["Date and Time", "EC da água"], inplace=True)

    # --- Processamento DF PH ---
    df_ph["Hora lig 4"] = pd.to_numeric(df_ph["Hora lig 4"].astype(str).str.replace(',', '.'), errors='coerce')
    df_ph["Média do PH"] = pd.to_numeric(df_ph["Média do PH"].astype(str).str.replace(',', '.'), errors='coerce')
    df_ph["Date and Time"] = pd.to_datetime(df_ph["Date and Time"], errors='coerce')

    # --- Merge dos DataFrames ---
    # Manter apenas colunas relevantes do df_ph antes de juntar
    df_ph_relevante = df_ph[["Date and Time", "Hora lig 4", "Média do PH"]]
    # Usar merge externo para manter todos os registros de tempo de ambos os arquivos
    df = pd.merge(df_ec, df_ph_relevante, on="Date and Time", how="outer")

    # Preencher valores NaN (resultantes do merge) com 0 para as colunas de tempo
    time_cols = ["Hora lig 1", "Hora lig 2", "Hora lig 3", "Hora lig 4"]
    for col in time_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            
    # Para o gráfico, preencher valores ausentes para garantir linhas contínuas
    df['EC da água'] = df['EC da água'].ffill().bfill()
    df['Média do PH'] = df['Média do PH'].ffill().bfill()
    df.sort_values(by="Date and Time", inplace=True)


except (FileNotFoundError, KeyError) as e:
    print(f"Erro ao carregar ou processar os arquivos de dados: {e}")
    # Se houver erro, cria um DataFrame vazio para evitar que o dashboard quebre
    df = pd.DataFrame({
        "Date and Time": [], "EC da água": [], "Média do PH": [],
        "Hora lig 1": [], "Hora lig 2": [], "Hora lig 3": [], "Hora lig 4": []
    })

# Extrair meses únicos para o dropdown
if not df.empty:
    meses_disponiveis = sorted(df['Date and Time'].dt.month.unique())
else:
    meses_disponiveis = []


# --- 2. Inicialização do Dashboard ---
app = dash.Dash(__name__)
server = app.server

# --- 3. Layout do Dashboard ---
app.layout = html.Div(
    style={'backgroundColor': '#f0f2f5', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H1(
            "Painel de Controle Verdureira - Tempo de Funcionamento do IrrigaPro",
            style={'textAlign': 'center', 'color': '#333', 'marginBottom': '30px'}
        ),

        # Dropdown para filtro de mês
        html.Div([
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': f'Mês {month}', 'value': month} for month in meses_disponiveis],
                placeholder="Selecione um mês"
            ),
        ], style={'width': '20%', 'margin': '20px auto'}),

        html.Div(
            className="cards-container",
            style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '40px'},
            children=[
                # Card Tempo Total
                html.Div(
                    style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'width': '18%'},
                    children=[
                        html.H3("Tempo Total (Horas)", style={'margin': '0', 'color': '#555'}),
                        html.P(id='total-time', style={'fontSize': '36px', 'fontWeight': 'bold', 'color': '#1a73e8', 'margin': '10px 0 0 0'})
                    ]
                ),
                # Card Bomba 1
                html.Div(
                    style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'width': '18%'},
                    children=[
                        html.H3("Bomba 1 (Horas)", style={'margin': '0', 'color': '#555'}),
                        html.P(id='pump1-time', style={'fontSize': '30px', 'fontWeight': 'bold', 'color': '#34a853', 'margin': '10px 0 0 0'})
                    ]
                ),
                # Card Bomba 2
                html.Div(
                    style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'width': '18%'},
                    children=[
                        html.H3("Bomba 2 (Horas)", style={'margin': '0', 'color': '#555'}),
                        html.P(id='pump2-time', style={'fontSize': '30px', 'fontWeight': 'bold', 'color': '#fbbc05', 'margin': '10px 0 0 0'})
                    ]
                ),
                # Card Bomba 3
                html.Div(
                    style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'width': '18%'},
                    children=[
                        html.H3("Bomba 3 (Horas)", style={'margin': '0', 'color': '#555'}),
                        html.P(id='pump3-time', style={'fontSize': '30px', 'fontWeight': 'bold', 'color': '#ea4335', 'margin': '10px 0 0 0'})
                    ]
                ),
                # Card Bomba 4
                html.Div(
                    style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'width': '18%'},
                    children=[
                        html.H3("Bomba 4 (Horas)", style={'margin': '0', 'color': '#555'}),
                        html.P(id='pump4-time', style={'fontSize': '30px', 'fontWeight': 'bold', 'color': '#5f6368', 'margin': '10px 0 0 0'})
                    ]
                ),
            ]
        ),

        html.Div(
            style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'},
            children=[
                dcc.Graph(id='ec-graph')
            ]
        )
    ]
)

# --- 4. Callback para atualizar o dashboard ---
@app.callback(
    [Output('ec-graph', 'figure'),
     Output('total-time', 'children'),
     Output('pump1-time', 'children'),
     Output('pump2-time', 'children'),
     Output('pump3-time', 'children'),
     Output('pump4-time', 'children')],
    [Input('month-dropdown', 'value')]
)
def update_dashboard(selected_month):
    # Filtrar DataFrame com base no mês selecionado
    if selected_month is not None:
        filtered_df = df[df['Date and Time'].dt.month == selected_month]
    else:
        filtered_df = df

    if filtered_df.empty:
        # Se não houver dados, retorna valores vazios/padrão
        fig = px.line(title="Sem dados para exibir")
        return fig, "0.00", "0.00", "0.00", "0.00", "0.00"

    # Corrigir o cálculo para somar apenas o último valor de cada dia
    df_sorted = filtered_df.copy()
    df_sorted.sort_values(by="Date and Time", inplace=True)
    df_sorted['date_only'] = df_sorted['Date and Time'].dt.date

    # Somar o último valor (em minutos) de cada dia para cada bomba
    soma_minutos1 = df_sorted.groupby('date_only')['Hora lig 1'].last().sum()
    soma_minutos2 = df_sorted.groupby('date_only')['Hora lig 2'].last().sum()
    soma_minutos3 = df_sorted.groupby('date_only')['Hora lig 3'].last().sum()
    soma_minutos4 = df_sorted.groupby('date_only')['Hora lig 4'].last().sum()

    # Converter o total de minutos para horas
    soma_hora1 = soma_minutos1 / 60
    soma_hora2 = soma_minutos2 / 60
    soma_hora3 = soma_minutos3 / 60
    soma_hora4 = soma_minutos4 / 60
    soma_total = soma_hora1 + soma_hora2 + soma_hora3 + soma_hora4

    # --- Lógica do Gráfico ---
    # Transformar o DataFrame de formato largo para longo para o gráfico
    df_long = filtered_df.melt(id_vars=['Date and Time'], 
                               value_vars=['EC da água', 'Média do PH'],
                               var_name='Metrica', 
                               value_name='Valor')

    # Atualizar figura do gráfico
    fig = px.line(
        df_long, 
        x="Date and Time", 
        y="Valor", 
        color='Metrica', # Usar a coluna 'Metrica' para criar linhas diferentes
        title="Variação do EC e PH ao Longo do Tempo",
        labels={'Date and Time': 'Data e Hora', 'Valor': 'Valor', 'Metrica': 'Métrica'}
    )
    fig.update_layout(
        paper_bgcolor="#f9f9f9",
        plot_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color="#333"),
        title_font_size=20,
        xaxis=dict(showgrid=True, gridcolor='#e5e5e5'),
        yaxis=dict(showgrid=True, gridcolor='#e5e5e5')
    )

    return fig, f"{soma_total:.2f}", f"{soma_hora1:.2f}", f"{soma_hora2:.2f}", f"{soma_hora3:.2f}", f"{soma_hora4:.2f}"

# --- 5. Execução do Servidor ---
if __name__ == '__main__':
    app.run(debug=True)
