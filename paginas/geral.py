import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

historico_url = ("/Users/gabrielreis/Git/disciplinas-est/Streamlit/completo_est.csv")
professores_dout_url = ("/Users/gabrielreis/Git/disciplinas-est/Streamlit/professores_dout.csv")
formandos_url = ("/Users/gabrielreis/Git/disciplinas-est/Streamlit/formandos.csv")

profs_ativos = ["Alan Ricardo da Silva", "Ana Maria Nogales Vasconcelos", "André Luiz Fernandes Cançado", "Antônio Eduardo Gomes", "Bernardo Borba de Andrade",
                "Bernardo Nogueira Schlemper", "Cibele Queiroz da Silva", "Cira Etheowalda Guevara Otiniano", "Claudete Ruas", "Démerson André Polli",
                "Donald Matthew Pianto","Eduardo Freitas da Silva", "Eduardo Monteiro de Castro Gomes","Eduardo Yoshio Nakano","George Freitas Von Borries",
                "Geraldo da Silva e Souza", "Gladston Luiz da Silva", "Guilherme Souza Rodrigues", "Gustavo Leonel Gilardoni Avalle", "Helton Saulo Bezerra dos Santos",
                "Israel de Freitas Madureira", "Jhames Matos Sampaio", "Joanlise Marco de Leon Andrade", "José Angelo Belloni", "José Augusto Fiorucci", 
                "Juliana Betini Fachini Gomes", "Leandro Tavares Correia", "Lucas Moreira", "Luís Gustavo do Amaral Vinha", "Maria Teresa Leão Costa", 
                "Peter Zornig", "Raul Yukihiro Matsushita", "Roberto Vila Gabriel", "Thais Carvalho Valadares Rodrigues"]

@st.cache(persist=True)
def load_data(url = historico_url):
    data = pd.read_csv(url)
    #data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

historico = load_data(historico_url)
professores_dout = load_data(professores_dout_url)
formandos = load_data(formandos_url)

#profs_dout = [prof for prof in profs_ativos if prof in list(professores_dout.Professores)]
disciplinas_pie = historico.drop_duplicates(subset=['disciplina']).groupby('tipo')['disciplina'].count().reset_index()
#disciplinas_pie = historico.head()
profs_pie = pd.DataFrame({'professor': profs_ativos, 'doutor': ['Doutor' if prof in list(professores_dout.Professores) else 'Mestre' for prof in profs_ativos]}).groupby('doutor').count().reset_index()

def app():
    st.title("Informações Gerais")
    st.write("Informações Gerais do Departamento de Estatística")
    
    #st.write(profs)
    #st.write(professores_dout)
    #st.write(disciplinas_pie)

    col1, col2 = st.beta_columns([3,1])

    fig_pie_profs = px.pie(profs_pie, names='doutor', values='professor', title='Formação dos Professores', color_discrete_sequence=["#133E79", "#D0F5FF"], width=500, hole=.6)
    fig_pie_disc = px.pie(disciplinas_pie, names='tipo', values='disciplina', title='Tipo de Disciplina', color_discrete_sequence=["#008940","#C5F1E9"], width=500, hole=.6)
    fig_line = px.line(formandos, x='Semestre', y='Quantitativo', color_discrete_sequence=["#133E79"], title="Quantidade de Formandos", width=1000, height=600,
                       labels={'Semestre':'Período', 'Quantitativo':'Quantidade'})
    
    col1.plotly_chart(fig_pie_profs)
    col2.plotly_chart(fig_pie_disc)
    st.plotly_chart(fig_line)
