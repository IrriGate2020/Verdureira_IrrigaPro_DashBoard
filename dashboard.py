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
external_stylesheets = [
    {'href': 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap', 'rel': 'stylesheet'},
    {'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css', 'rel': 'stylesheet'}
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

def create_card(title, icon, value_id, color):
    return html.Div(
        className="card",
        style={
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
            'transition': '0.3s',
            'textAlign': 'center',
            'width': '18%',
            'borderBottom': f'5px solid {color}'
        },
        children=[
            html.H3([
                html.I(className=f"{icon} mr-2"),
                title
            ], style={'margin': '0', 'color': '#555', 'fontSize': '18px'}),
            html.P(id=value_id, style={'fontSize': '36px', 'fontWeight': 'bold', 'color': color, 'margin': '10px 0 0 0'})
        ]
    )

# --- 3. Layout do Dashboard ---
app.layout = html.Div(
    style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'fontFamily': 'Roboto, sans-serif'},
    children=[
        html.H1(
            "Painel de Controle Verdureira - Tempo de Funcionamento do IrrigaPro",
            style={'textAlign': 'center', 'color': '#343a40', 'marginBottom': '40px', 'fontSize': '36px'}
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
                create_card("Tempo Total", "fas fa-clock", "total-time", "#1a73e8"),
                create_card("Bomba 1", "fas fa-tint", "pump1-time", "#34a853"),
                create_card("Bomba 2", "fas fa-tint", "pump2-time", "#fbbc05"),
                create_card("Bomba 3", "fas fa-tint", "pump3-time", "#ea4335"),
                create_card("Bomba 4", "fas fa-tint", "pump4-time", "#5f6368"),
            ]
        ),

        html.Div(
            className="cards-container",
            style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '40px'},
            children=[
                create_card("Vazão Total", "fas fa-water", "total-flow", "#1a73e8"),
                create_card("Vazão B1", "fas fa-water", "pump1-flow", "#34a853"),
                create_card("Vazão B2", "fas fa-water", "pump2-flow", "#fbbc05"),
                create_card("Vazão B3", "fas fa-water", "pump3-flow", "#ea4335"),
                create_card("Vazão B4", "fas fa-water", "pump4-flow", "#5f6368"),
            ]
        ),

        html.Div(
            style={'textAlign': 'center', 'marginBottom': '20px'},
            children=[
                dcc.Checklist(
                    id='trace-toggle-checklist',
                    options=[
                        {'label': 'EC', 'value': 'EC'},
                        {'label': 'PH', 'value': 'PH'}
                    ],
                    value=['EC', 'PH'],
                    inline=True,
                    labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                )
            ]
        ),

        html.Div(
            id='graph-container',
            style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'},
            children=[
                dcc.Graph(id='ec-graph')
            ]
        )
    ]
)

# --- 4. Callback para atualizar o dashboard ---

def format_time(minutes):
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours}h {mins}m"

@app.callback(
    [Output('ec-graph', 'figure'),
     Output('total-time', 'children'),
     Output('pump1-time', 'children'),
     Output('pump2-time', 'children'),
     Output('pump3-time', 'children'),
     Output('pump4-time', 'children'),
     Output('total-flow', 'children'),
     Output('pump1-flow', 'children'),
     Output('pump2-flow', 'children'),
     Output('pump3-flow', 'children'),
     Output('pump4-flow', 'children')],
    [Input('month-dropdown', 'value'),
     Input('trace-toggle-checklist', 'value')]
)
def update_dashboard(selected_month, checklist_value):
    # Filtrar DataFrame com base no mês selecionado
    if selected_month is not None:
        filtered_df = df[df['Date and Time'].dt.month == selected_month]
    else:
        filtered_df = df

    if filtered_df.empty:
        # Se não houver dados, retorna valores vazios/padrão
        fig = px.line(title="Sem dados para exibir")
        return fig, "0h 0m", "0h 0m", "0h 0m", "0h 0m", "0h 0m", "0.00", "0.00", "0.00", "0.00", "0.00"

    # Corrigir o cálculo para somar apenas o último valor de cada dia
    df_sorted = filtered_df.copy()
    df_sorted.sort_values(by="Date and Time", inplace=True)
    df_sorted['date_only'] = df_sorted['Date and Time'].dt.date

    # Somar o último valor (em minutos) de cada dia para cada bomba
    soma_minutos1 = df_sorted.groupby('date_only')['Hora lig 1'].last().sum()
    soma_minutos2 = df_sorted.groupby('date_only')['Hora lig 2'].last().sum()
    soma_minutos3 = df_sorted.groupby('date_only')['Hora lig 3'].last().sum()
    soma_minutos4 = df_sorted.groupby('date_only')['Hora lig 4'].last().sum()
    soma_total_minutos = soma_minutos1 + soma_minutos2 + soma_minutos3 + soma_minutos4

    # Calcular a vazão em litros
    vazao_bomba1 = soma_minutos1 * 4
    vazao_bomba2 = soma_minutos2 * 4
    vazao_bomba3 = soma_minutos3 * 4
    vazao_bomba4 = soma_minutos4 * 4
    vazao_total = vazao_bomba1 + vazao_bomba2 + vazao_bomba3 + vazao_bomba4

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
        labels={'Date and Time': 'Data e Hora', 'Valor': 'Valor', 'Metrica': 'Métrica'},
        color_discrete_map={'EC da água': '#34a853', 'Média do PH': '#1a73e8'}
    )
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Roboto, sans-serif", size=12, color="#343a40"),
        title_font_size=20,
        xaxis=dict(showgrid=True, gridcolor='#e5e5e5'),
        yaxis=dict(showgrid=True, gridcolor='#e5e5e5'),
        legend_title_text=''
    )

    if 'EC' not in checklist_value:
        fig.data[0].visible = False
    if 'PH' not in checklist_value:
        fig.data[1].visible = False

    # Adicionar anotações de máximo e mínimo
    if not filtered_df.empty:
        if 'EC' in checklist_value:
            max_ec = filtered_df.loc[filtered_df['EC da água'].idxmax()]
            min_ec = filtered_df.loc[filtered_df['EC da água'].idxmin()]
            fig.add_annotation(x=max_ec['Date and Time'], y=max_ec['EC da água'], text="Máx EC", showarrow=True, arrowhead=1)
            fig.add_annotation(x=min_ec['Date and Time'], y=min_ec['EC da água'], text="Mín EC", showarrow=True, arrowhead=1)
        if 'PH' in checklist_value:
            max_ph = filtered_df.loc[filtered_df['Média do PH'].idxmax()]
            min_ph = filtered_df.loc[filtered_df['Média do PH'].idxmin()]
            fig.add_annotation(x=max_ph['Date and Time'], y=max_ph['Média do PH'], text="Máx PH", showarrow=True, arrowhead=1)
            fig.add_annotation(x=min_ph['Date and Time'], y=min_ph['Média do PH'], text="Mín PH", showarrow=True, arrowhead=1)


    return (
        fig, 
        format_time(soma_total_minutos),
        format_time(soma_minutos1),
        format_time(soma_minutos2),
        format_time(soma_minutos3),
        format_time(soma_minutos4),
        f"{vazao_total:.2f}",
        f"{vazao_bomba1:.2f}",
        f"{vazao_bomba2:.2f}",
        f"{vazao_bomba3:.2f}",
        f"{vazao_bomba4:.2f}"
    )

# --- 5. Execução do Servidor ---
if __name__ == '__main__':
    app.run(debug=True)
