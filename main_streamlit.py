import streamlit as st
import SessionState
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Medicamentos y alergias",layout='wide')
session_state = SessionState.get(a=0)
selection_col, display_col = st.beta_columns([1, 3])
siteFooter = st.beta_container()

with selection_col:
    input = st.text_input('Escribe aqui el medicamento')

    modos_disponibles=['Gluten']
    modo_selected=st.selectbox('Alergia a buscar',
                                           options=modos_disponibles, index=0)

    if modo_selected=='Gluten':
        keywords=['gluten', 'trigo','cebada','avena','cebada','triticale', 'centeno',
                  'celíac', 'celiac','celiaq', 'carboximetilalmid']
    meds=False
    med_dict = {}
    if st.button('Buscar'):
        url=f"https://www.aemps.gob.es/?s={input}"
        sopa=BeautifulSoup(requests.get(url,timeout=20).content, 'html.parser')
        meds=sopa.find_all('article',{'class': "post type-post status-publish format-standard has-post-thumbnail hentry entry"})

        for med in meds:
            medicina=med.find('a')
            nombre=medicina.text
            link=medicina['href']
            code=link[-5:]
            img=med.find('img')['src']
            status=[]
            FT_link=f"https://cima.aemps.es/cima/dochtml/ft/{code}/FT_{code}.html"
            sopa_FT=BeautifulSoup(requests.get(FT_link,timeout=20).content, 'html.parser')
            for key in keywords:
                status.append(int(key in str(sopa_FT).lower()))
            med_dict[nombre]={'link':FT_link, 'img':img,'status':status}

    with display_col:
        if type(meds)!=bool:
            if len(meds)==0:
                st.write(f'No hemos encontrado medicamentos con {input}')
        for k in med_dict.keys():
            st.image(f'{med_dict[k]["img"]}')
            st.write(k)
            st.markdown(f'Ficha técnica: {med_dict[k]["link"]}', unsafe_allow_html=True)
            sum=0
            for i in range(len(keywords)):
                if status[i]>0:
                    st.write(f'ALERTA: {keywords[i]} encontrado. Por favor, revisa la ficha técnica', unsafe_allow_html=True)
                    sum+=status[i]
            if sum==0:
                st.markdown('Todo OK :)')

with siteFooter:
    style="""<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    }
    </style>"""
    footer = """
    <div    class ="footer">
    <p><small>
    Esta web ha sido desarrollada con Python y Streamlit.
    La información aquí publicada ha sido extraída de información pública de la Asociación Española de Medicamentos y Productos Sanitarios (AEMPS) <a href="www.aemps.gob.es" target="_blank">link</a>.</small></p>
    </div>
    """
    st.markdown(style, unsafe_allow_html=True)
    st.markdown(footer, unsafe_allow_html=True)
    #
    #