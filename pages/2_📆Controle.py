import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Plataforma Santiago Engenharia",
    page_icon= "https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
    layout="wide"
)
st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

# Atualização da página a cada 5 minutos. Não permitir a hibernação.
keep_alive_script = """
<script>
    function keepAlive() {
        setInterval(function() {
            console.log("Sending keep-alive ping...");
            fetch("/").then(response => {
                console.log("Ping response: ", response);
            });
        }, 300000); // A cada 5 minutos
    }
    document.addEventListener('DOMContentLoaded', keepAlive);
</script>
"""

st.components.v1.html(keep_alive_script, height=0)


# Função JavaScript para manipular o localStorage
local_storage_script = """
<script>
    function getLoginState() {
        return localStorage.getItem("logged_in") === "true";
    }

    function clearLoginState() {
        localStorage.removeItem("logged_in");
    }

    document.addEventListener('DOMContentLoaded', (event) => {
        const loggedIn = getLoginState();
        if (!loggedIn) {
            window.parent.postMessage("logged_out", "*");
        }
    });
</script>
"""

# Incluir o JavaScript no Streamlit
st.components.v1.html(local_storage_script, height=0)

# Função para verificar se o usuário está logado
def is_logged_in():
    return st.session_state.get('logged_in', False)

# Função para limpar o login no localStorage
def logout():
    st.session_state['logged_in'] = False
    st.components.v1.html('<script>clearLoginState();</script>', height=0)

# Verificação de login
if not is_logged_in():
    st.subheader("Você precisa fazer login para acessar este menu")
    st.subheader("Volte para a página inicial")
    st.stop()  # Interrompe o código se não estiver logado

else:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.subheader("Logoff")
    with col2:
        if st.button("Sair"):
            logout()
            st.write("Você foi desconectado")


    path = Path(__file__).parent.parent


    # TÍTULO DA PÁGINA
    st.title("CONTROLE DE DOCUMENTOS")
    st.header("Empresa: Gennesis Engenharia e Consultoria LTDA")
    st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

# CARREGAR OS DADOS DA PLANILHA

    if "data" in st.session_state:
        df_data = st.session_state["data"]
        df_data = df_data.dropna(subset=["Cidade",
                                        "Licença",
                                        "Documento",
                                        "Licença-Data de emissão",
                                        "Licença-Data de validade",
                                        "Status da licença",
                                        "Dias restantes",                                  
                                        ])
        df_data = df_data[(df_data["Cidade"] != "") &
                        (df_data["Licença"] != "") &
                        (df_data["Documento"] != "") &
                        (df_data["Licença-Data de emissão"] != "") &
                        (df_data["Licença-Data de validade"] != "") &
                        (df_data["Status da licença"] != "") &
                        (df_data["Dias restantes"] != "") ]
        df_data = df_data[["Cidade",
                        "Licença",
                        "Documento",
                        "Licença-Data de emissão",
                        "Licença-Data de validade",
                        "Status da licença",
                        "Dias restantes"]]
    
    # DESCRITIVO INICIAL
        st.subheader("Número de Documentos: 1")
        st.subheader("Código do Documento 1: PGRSCC")
        #st.subheader("Código da licença 2: L-5678")

    # INSERIR OPÇÃO PARA ESCOLHA DA LICENÇA
        licenca = df_data["Documento"].unique()
        licenca_selecionada = st.sidebar.selectbox("Licenças", licenca)

        df_filtrado = df_data[df_data["Documento"] == licenca_selecionada]

        contagem_por_data = df_filtrado.groupby("Licença-Data de validade")["Documento"].count().reset_index()

        st.divider()

        st.header(f"Documento {licenca_selecionada}")

        if not df_filtrado.empty:
            col1, col2, col3 = st.columns([0.25 , 0.25 , 0.5])
            col1.metric(label="Data de emissão do documento:", value=df_filtrado["Licença-Data de emissão"].iloc[0].strftime("%d/%m/%Y"))
            #col2.metric(label="Data da validade do documento:", value=df_filtrado["Licença-Data de validade"].iloc[0].strftime("%d/%m/%Y"))
        
            #col1, col2 = st.columns(2)

            #col1.metric(label="Dias para vencimento:", value=int(df_filtrado["Dias restantes"].iloc[0]))
            col2.metric(label="Status:", value=df_filtrado["Status da licença"].iloc[0])
        else:
            st.warning("Não há licença para a condição selecionada.")

        #st.divider()

    # VENCIMENTO

        #st.subheader("Vencimento")

    # CRIANDO CORES DAS BARRAS DO GRÁFICO

        df_filtrado["Cor"] = df_filtrado["Status da licença"].map({
            "Dentro do prazo": "green",
            "Válido": "green",
            "Vencida": "red",
            "Renovar": "yellow"
    })

    # 1º GRÁFICO

        #contagem_por_data = contagem_por_data.merge(df_filtrado[["Licença-Data de validade", "Cor"]].drop_duplicates(), on="Licença-Data de validade", how="left") 



        #fig = px.bar(
    #         contagem_por_data,
    #         x="Licença-Data de validade",
    #         y="Código Licença",
    #         color="Cor",
    #         labels={"Licença-Data de validade": "Data de Validade", "Quantidade de licenças": "Número de Licenças"},
    #         template="plotly_dark",
    #         color_discrete_map={"green":"green","red":"red","yellow":"yellow"}
    # )

    #CONFIGURANDO O TAMANHO DO GRÁFICO
    #     fig.update_layout(
    #         width=600,
    #         height=400
    # )

        #col1, col2, col3 = st.columns([1, 2, 1])

        #with col2:
        # col3.plotly_chart(fig)

        st.divider()

        st.subheader("Download do PGRSCC")
        pgrscc_path = path / "dataset" / "Arquivo" / "PGRSCC.pdf"

        with open(pgrscc_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        st.download_button(
            label="Download PGRSCC",
            data=pdf_data,
            file_name="PGRSCC.pdf",
            mime="application/pdf"
        )
        
        st.subheader("Download do ART")
        art_path = path / "dataset" / "Arquivo" / "ART.pdf"

        with open(art_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        st.download_button(
            label="Download ART",
            data=pdf_data,
            file_name="ART.pdf",
            mime="application/pdf"
        )



    else:
        st.write("Dados não correlacionados")

    # FUNÇÃO QUE DEFINE A PARA A LOGO

    st.sidebar.image("Santiago.png", caption="Plataforma de Controle")
    st.sidebar.markdown("Desenvolvido por Santiago Engenharia (https://santiagoengenharia.com)")


 
 