import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

historico_url = ("/Users/gabrielreis/Git/disciplinas-est/Streamlit/completo_est_cripto.csv")

#profs_ativos = ["Alan Ricardo da Silva", "Ana Maria Nogales Vasconcelos", "André Luiz Fernandes Cançado", "Antônio Eduardo Gomes", "Bernardo Borba de Andrade",
#                "Bernardo Nogueira Schlemper", "Cibele Queiroz da Silva", "Cira Etheowalda Guevara Otiniano", "Claudete Ruas", "Démerson André Polli",
#                "Donald Matthew Pianto","Eduardo Freitas da Silva", "Eduardo Monteiro de Castro Gomes","Eduardo Yoshio Nakano","George Freitas Von Borries",
#                "Geraldo da Silva e Souza", "Gladston Luiz da Silva", "Guilherme Souza Rodrigues", "Gustavo Leonel Gilardoni Avalle", "Helton Saulo Bezerra dos Santos",
#                "Israel de Freitas Madureira", "Jhames Matos Sampaio", "Joanlise Marco de Leon Andrade", "José Angelo Belloni", "José Augusto Fiorucci", 
#                "Juliana Betini Fachini Gomes", "Leandro Tavares Correia", "Lucas Moreira", "Luís Gustavo do Amaral Vinha", "Maria Teresa Leão Costa", 
#                "Peter Zornig", "Raul Yukihiro Matsushita", "Roberto Vila Gabriel", "Thais Carvalho Valadares Rodrigues"]

profs_ativos = ["GrgtfXoigxjufJgfYorBg", "GtgfSgxogfTumgrkyf1gyiutikruy", "GtjxkfRAoFfLkxtgtjkyfIgtigju",
        "GtzutoufKjAgxjufMusky", "HkxtgxjufHuxhgfJkfGtjxgjk", "HkxtgxjufTumAkoxgfYinrksvkx",
        "IohkrkfWAkoxuFfJgfYorBg", "IoxgfKznkuCgrjgfMAkBgxgfUzotogtu", "IrgAjkzkfXAgy",
        "JkskxyutfGtjxkfVurro", "JutgrjfSgzznkCfVogtzu", "KjAgxjufLxkozgyfJgfYorBg",
        "KjAgxjufSutzkoxufJkfIgyzxufMusky", "KjAgxjuf4uynoufTgqgtu", "MkuxmkfLxkozgyf1utfHuxxoky",
        "MkxgrjufJgfYorBgfKfYuAFg", "MrgjyzutfRAoFfJgfYorBg", "MAornkxskfYuAFgfXujxomAky",
        "MAyzgBufRkutkrfMorgxjutofGBgrrk", "NkrzutfYgArufHkFkxxgfJuyfYgtzuy", "OyxgkrfJkfLxkozgyfSgjAxkoxg",
        "PngskyfSgzuyfYgsvgou", "PugtroykfSgxiufJkfRkutfGtjxgjk", "PuykfGtmkrufHkrruto",       
        "PuykfGAmAyzufLouxAiio", "PArogtgfHkzotofLginotofMusky", "RkgtjxufZgBgxkyfIuxxkog",
        "RAigyfSuxkoxg", "RAoyfMAyzgBufJufGsgxgrf1otng", "SgxogfZkxkygfRkgufIuyzg",
        "Vkzkxf5uxtom", "XgArf4AqonoxufSgzyAynozg", "Xuhkxzuf1orgfMghxokr",
        "ZngoyfIgxBgrnuf1grgjgxkyfXujxomAky"]

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(historico_url)
    #data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

historico = load_data()

df_professores = historico[~historico.mencao.isin(["CC", "DP"])]
df_professores['mencao'].replace({"TJ":"TR"}, inplace=True)

def app():
    st.title("Professores")
    st.write("Informações dos Professores do Departamento de Estatística")

    #st.write(df_bacharelado.mencao.value_counts())

    disciplinas_ordenadas = sorted(df_professores.disciplina.unique())
    
    check_profs_ativos = st.checkbox("Professores Ativos", True)

    if check_profs_ativos:
        professores_ordenados = sorted(profs_ativos)
    else:
        professores_ordenados = sorted(df_professores.professor.unique())

    disc_selecionadas = st.sidebar.multiselect('Disciplina(s)', disciplinas_ordenadas, None, key=0)
    
    prof_selecionados = st.sidebar.multiselect('Professor(es)', professores_ordenados, None, key=1)

    period_selecionados = st.sidebar.slider("Período(s)", 1994, 2021, (1994, 2021), key=0)
    
    if len(disc_selecionadas) > 0:
        disciplinas = df_professores[df_professores.disciplina.isin(disc_selecionadas)]
    else:
        disciplinas = df_professores

    if len(prof_selecionados) > 0:
        selecao = disciplinas[disciplinas.professor.isin(prof_selecionados)]
    else:
        selecao = disciplinas
    
    if check_profs_ativos:
        professores_selecao = selecao[selecao.professor.isin(profs_ativos)]
    else:
        professores_selecao = selecao

    if st.sidebar.checkbox("Incluir SR", True):
        if st.sidebar.checkbox("Incluir Trancamentos", True):
            disciplinas_mencoes = professores_selecao
        else:
            disciplinas_mencoes = selecao[selecao.mencao != "TR"]
    else:
        if st.sidebar.checkbox("Incluir Trancamentos", True):
            disciplinas_mencoes = selecao[selecao.mencao != "SR"]
        else:
            disciplinas_mencoes = selecao[~selecao.mencao.isin(["SR", "TR"])]       

    absoluto = st.sidebar.checkbox("Valores Absolutos", False)
    
    if absoluto:
        mencoes_professores = disciplinas_mencoes.groupby('professor')['mencao'].value_counts(normalize=False).\
            rename_axis(['professor', 'mencoes']).reset_index().sort_values(by=['mencao'], ascending=False)
    else:
        mencoes_professores = disciplinas_mencoes.groupby('professor')['mencao'].value_counts(normalize=True).\
            rename_axis(['professor', 'mencoes']).reset_index().sort_values(by=['mencao'], ascending=False)        

    mencoes_periodos = disciplinas_mencoes.groupby('periodo')['mencao'].value_counts(normalize=True).rename_axis(['periodo', 'mencoes']).reset_index()
    
    alunos_professor = df_professores.groupby(['periodo', 'professor']).nome.count().reset_index().groupby('periodo').nome.mean().reset_index()

    if absoluto:
        fig_barras = px.bar(mencoes_professores, x = 'mencao', y='professor', color='mencoes', labels={'professor': 'Professor', 'mencao': 'Quantidade de Alunos', 'mencoes': 'Menção'},
                    orientation='h', height=1000, width=1000, category_orders={"mencoes": ["SR", "II", "MI", "TR", "MM", "MS", "SS"],
                                                                   "professor": list(mencoes_professores[mencoes_professores.mencoes.isin(["SR", "II", "MI", "TR"])].groupby('professor').mencao.sum().sort_values(ascending=True).index)}, 
                    color_discrete_sequence=["#b2172b", "#ef8a62", "#fddbc7", "#b3b3b3", "#d1e5f0", "#66a9cf", "#2266ac"])
    else:
        fig_barras = px.bar(mencoes_professores, x = 'mencao', y='professor', color='mencoes', labels={'professor': 'Professor', 'mencao': 'Proporção de Alunos', 'mencoes': 'Menção'},
                    orientation='h', height=1000, width=1000, category_orders={"mencoes": ["SR", "II", "MI", "TR", "MM", "MS", "SS"],
                                                                   "professor": list(mencoes_professores[mencoes_professores.mencoes.isin(["SS", "MS", "MM"])].groupby('professor').mencao.sum().sort_values(ascending=False).index)}, 
                    color_discrete_sequence=["#b2172b", "#ef8a62", "#fddbc7", "#b3b3b3", "#d1e5f0", "#66a9cf", "#2266ac"])

    fig_linhas = px.line(alunos_professor, x = 'periodo', y='nome', color_discrete_sequence = ["#2266ac"], labels={'nome': 'Alunos por Professor', 'periodo': 'Período'},
                category_orders={"periodo": ["1994/1","1994/2","1995/1","1995/2","1996/1","1996/2","1997/1","1997/2","1998/0", "1998/1","1998/2","1999/1","1999/2",
                                             "2000/0","2000/1","2000/2","2001/0","2001/1","2001/2","2002/1","2002/2","2003/1","2003/2","2004/1","2004/2","2005/1","2005/2","2006/1","2006/2","2007/0","2007/1","2007/2","2008/0","2008/1","2008/2","2009/0","2009/1","2009/2",
                                             "2010/0","2010/1","2010/2","2011/1","2011/2","2012/0","2012/1","2012/2","2013/1","2013/2","2014/0","2014/1","2014/2","2015/0","2015/1","2015/2","2016/0","2016/1","2016/2","2017/0","2017/1","2017/2","2018/0","2018/1","2018/2","2019/0","2019/1","2019/2",
                                             "2020/0"]}, 
                width=1000)    
    #fig.update_layout(yaxis= {'categoryorder':'total descending'})

    #st.write(disciplinas_mencoes)
    #st.write(mencoes_periodos)
    #st.write(mencoes_disciplinas)
    #st.write(alunos_professor)
    
    st.plotly_chart(fig_barras)

    st.plotly_chart(fig_linhas)