from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Função para gerar gráficos de pizza
def gerar_grafico_pizza(df, coluna, titulo, config):
    
    df[coluna] = df[coluna].str.strip() 
    
    # Contar as ocorrências
    contagem = df[coluna].value_counts().reset_index()
    contagem.columns = [coluna, "Quantidade"]
    
    # Criando o gráfico de pizza
    fig = px.pie(
        contagem,
        names=coluna,
        values="Quantidade",
        title=titulo,
        hover_data=["Quantidade"],  
        labels={coluna: "Categoria", "Quantidade": "Qtd"}  
    )
    
    # Exibindo apenas os números dentro do gráfico
    fig.update_traces(textinfo='value', textposition='inside')  
    
    return fig.to_html(full_html=False, config=config)


def gerar_grafico_barras(df, config):
    
    df["Conhece_Mecânico"] = df["Conhece_Mecânico"].str.strip()
    df["Indicação_Parente"] = df["Indicação_Parente"].str.strip()
    
    
    df_filtrado = df[~((df['Conhece_Mecânico'] == 'Não') & (df['Indicação_Parente'] == 'Sim'))]
    
    
    grouped = df_filtrado.groupby(["Conhece_Mecânico", "Indicação_Parente"]).size().reset_index(name='count')
    
    
    fig = px.bar(
        grouped,
        x="Conhece_Mecânico",
        y="count",
        color="Indicação_Parente",
        barmode="group",
        title="Conhece mecânico × Indicação de parente"
    )
    
    return fig.to_html(full_html=False, config=config)

@app.route('/')
def index():
    # Carregar os dados CSV com encoding UTF-8
    df = pd.read_csv("dados.csv", sep=";", encoding="utf-8", on_bad_lines="skip")
    
    
    df.columns = [
        "Idade", "Gênero", "CNH", "Conhecimento_Mecânica", "Conhece_Mecânico",
        "Indicação_Parente", "Confiança_Mecânica", "Visitas_Mecânico"
    ]
    
    # Limpeza dos dados para garantir que não haja valores inesperados
    df["Conhecimento_Mecânica"] = df["Conhecimento_Mecânica"].str.strip()  
    
    
    graficos_html = []

    # Configuração para remover o logo do Plotly
    config_plotly = {'displaylogo': False} 

    
    for coluna, titulo in [
        ("Idade", "Distribuição por Idade"),
        ("Gênero", "Distribuição por Gênero"),
        ("CNH", "Você possui CNH?"),
        ("Conhecimento_Mecânica", "Conhecimento em mecânica automotiva?"),
        ("Confiança_Mecânica", "Confiança para mexer na mecânica")
    ]:
        # Gerando o gráfico de pizza para cada coluna
        fig = gerar_grafico_pizza(df, coluna, titulo, config_plotly)
        graficos_html.append(fig)

    # Gerando o gráfico de barras
    fig_bar = gerar_grafico_barras(df, config_plotly)
    graficos_html.append(fig_bar)

    return render_template("index.html", graficos=graficos_html)

if __name__ == '__main__':
    app.run(debug=True)
