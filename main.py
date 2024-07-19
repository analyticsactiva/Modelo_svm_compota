import pandas as pd
import numpy as np
import time
import pickle
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
from openpyxl import load_workbook
import yaml
from yaml.loader import SafeLoader

# ----------------------------- Definición de variables -------------------------------------

def def_sexo(sexo):
    sexo_1 = 0
    sexo_2 = 0
    if(sexo == Sexo_txt[0]):
        sexo_1 = 1
    else:
        sexo_2 = 1
    return sexo_1,sexo_2

def rango_edad(edad):
    edad_1 = 0
    edad_2 = 0
    edad_3 = 0
    edad_4 = 0
    if(edad == Edad_txt[0]):
        edad_1 = 1
    elif(edad == Edad_txt[1]):
        edad_2 = 1
    elif(edad == Edad_txt[2]):
        edad_3 = 1
    else:
        edad_4 = 1
    return edad_1,edad_2,edad_3,edad_4

def asig_gse(gse):
    gse_1 = 0
    gse_2 = 0
    gse_3 = 0
    gse_4 = 0
    if(gse == GSE_txt[0]):
        gse_1 = 1
    elif(gse == GSE_txt[1]):
        gse_2 = 1
    elif(gse == GSE_txt[2]):
        gse_3 = 1
    else:
        gse_4 = 1
    return gse_1,gse_2,gse_3,gse_4

def CompHogar_mult(lista):
    f11_1 = 0
    f11_2 = 0
    f11_3 = 0
    f11_4 = 0
    f11_5 = 0
    f11_6 = 0
    for comp_hogar in lista:
        if(comp_hogar == CompHogar_txt[0]):
            f11_1 = 1
        if(comp_hogar == CompHogar_txt[1]):
            f11_2 = 1
        if(comp_hogar == CompHogar_txt[2]):
            f11_3 = 1
        if(comp_hogar == CompHogar_txt[3]):
            f11_4 = 1
        if(comp_hogar == CompHogar_txt[4]):
            f11_5 = 1
        if(comp_hogar == CompHogar_txt[5]):
            f11_6 = 1
    return f11_1,f11_2,f11_3,f11_4,f11_5,f11_6

def res_p13(p13):
    p13_1 = 0
    p13_2 = 0
    if(p13 == p13_txt[0]):
        p13_1 = 1
    else:
        p13_2 = 1
    return p13_1,p13_2

def res_p34(p34):
    p34_1 = 0
    p34_2 = 0
    p34_3 = 0
    if(p34 == p34_txt[0]):
        p34_1 = 1
    elif(p34 == p34_txt[1]):
        p34_2 = 1
    else:
        p34_3 = 1
    return p34_1,p34_2,p34_3

def res_p36_mult(lista):
    p36_1 = 0
    p36_2 = 0
    p36_3 = 0
    p36_4 = 0
    for p36 in lista:
        if(p36 == p36_txt[0]):
            p36_1 = 1
        if(p36 == p36_txt[1]):
            p36_2 = 1
        if(p36 == p36_txt[2]):
            p36_3 = 1
        if(p36 == p36_txt[3]):
            p36_4 = 1
    return p36_1,p36_2,p36_3,p36_4

def res_p35(p35):
    p35_1 = 0
    p35_2 = 0
    if(p35 == p35_txt[0]):
        p35_1 = 1
    else:
        p35_2 = 1
    return p35_1,p35_2

x_columns = ['SEXO_1','SEXO_2','RANGOEDAD_1','RANGOEDAD_2','RANGOEDAD_3','RANGOEDAD_4',
             'V_GSE_1_1','V_GSE_1_2','V_GSE_1_3','V_GSE_1_4','F11_A_1',
             'F11_A_2', 'F11_A_3', 'F11_A_4', 'F11_A_5', 'F11_A_6', 'P13_1',
             'P13_2', 'P34_0_1', 'P34_0_2', 'P34_0_3', 'P36_A_1', 'P36_A_2',
             'P36_A_3', 'P36_A_4', 'P35_0_1', 'P35_0_2']

def crear_reg(sexo,edad,gse,comp_hogar,p13,p34,p36,p35):

    sexo_1,sexo_2 = def_sexo(sexo)
    edad_1,edad_2,edad_3,edad_4 = rango_edad(edad)
    gse_1,gse_2,gse_3,gse_4 = asig_gse(gse)
    f11_1,f11_2,f11_3,f11_4,f11_5,f11_6 = CompHogar_mult(comp_hogar)
    p13_1,p13_2 = res_p13(p13)
    p34_1,p34_2,p34_3 = res_p34(p34)
    p36_1,p36_2,p36_3,p36_4 = res_p36_mult(p36)
    p35_1,p35_2 = res_p35(p35)

    reg_array = [sexo_1,sexo_2,edad_1,edad_2,edad_3,edad_4,gse_1,gse_2,gse_3,gse_4,f11_1,f11_2,f11_3,f11_4,f11_5,f11_6,
                 p13_1,p13_2,p34_1,p34_2,p34_3,p36_1,p36_2,p36_3,p36_4,p35_1,p35_2]
    registro = pd.DataFrame([reg_array], columns=x_columns)

    return registro

def cluster_label(cluster):
    dic_cluster = {
        1: 'Práctico y Consciente',
        2: 'Versátil y Ahorrador',
        3: 'Vigilante de la salud',
        4: 'Multitasking protector',
        5: 'Tradicional Saludable'
    }
    return dic_cluster[cluster]

# ---------------------------- Cargar Modelo ----------------------------------

with open('scaler.pkl','rb') as f:
    scaler = pickle.load(f)

# load the model from disk
filename = 'finalized_model.sav'
modelo_svm2 = pickle.load(open(filename, 'rb'))

# modelo SVM lineal

def get_cluster(new_x):
    x_pred = scaler.transform(new_x)

    pred = modelo_svm2.predict(x_pred)

    return int(pred[0])

def get_clusters(new_x):
    x_pred = scaler.transform(new_x)

    pred = modelo_svm2.predict(x_pred)

    return pred


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

hashed_passwords = Hasher(['Baf60255', 'activa1']).generate()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('main', fields = {'Form name': 'Activa Research'})



if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    #st.write(f'Bienvenido *{st.session_state["name"]}*')
    #st.title('Some content')

    st.image('logo-activa.svg',width=500)
    # --------------------- Display Barra Lateral -----------------------------------

    
    Sexo_txt = ('Hombre','Mujer')

    sexo = st.sidebar.selectbox('Sexo',Sexo_txt)

    Edad_txt = ('15 a 17 años','18 a 35 años','36 a 55 años','56 a 80 años')

    edad = st.sidebar.selectbox('Rango Edad',Edad_txt)

    GSE_txt = ('ABC1','C2','C3','D')

    gse = st.sidebar.selectbox('Grupo socioeconómico',GSE_txt)

    CompHogar_txt = ('Vive Solo', 'No vive solo','Vive con cónyuge','No vive con cónyuge','Vive con hijos','No vive con hijos')

    #comp_hogar = st.sidebar.selectbox('¿Con quién vive?',CompHogar_txt)

    comp_hogar = st.sidebar.multiselect('¿Con quién vive?',CompHogar_txt)

    p13_txt = ('Reemplazo por snack procesados dulces','No reemplazo por snack procesados dulces')

    p13 = st.sidebar.selectbox('¿Reemplaza snack?',p13_txt)

    p34_txt = ('Hogar de hábitos Saludables','Hogar de hábitos Regular','Hogar de hábitos No saludables')

    p34 = st.sidebar.selectbox('Hábitos del Hogar',p34_txt)

    p36_txt = ('Controlar calorías','No controlar calorías','Un Consumo rápido y fácil','No consumo rápido y fácil')

    #p36 = st.sidebar.selectbox('Objetivo de consumo',p36_txt)
    p36 = st.sidebar.multiselect('Objetivo de consumo',p36_txt)

    p35_txt = ('Totalmente dispuesto (5) a probar innovaciones saludables','1 a 4')

    p35 = st.sidebar.selectbox('Disposición a probar innovaciones saludables',p35_txt)

    new_x = crear_reg(sexo,edad,gse,comp_hogar,p13,p34,p36,p35)

    new_cluster = get_cluster(new_x)

    # ---------------------------------------- Display Resultado ---------------------------------------------

    progress_text = "Cargando. Por favor espere."
    my_bar = st.progress(0, text=progress_text)


    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()


    #st.markdown('Cluster: ')
    st.title(f'Cluster Compota: {cluster_label(new_cluster)}')

    #st.subheader(cluster_label(new_cluster))

    st.sidebar.button("Ejecutar")

    on = st.toggle("Información del modelo")

    if on:
        st.write("Modelo: Maquina de Soporte Vectorial")
        st.write('Confiabilidad del modelo en el conjunto de entrenamiento: 84%')

    # ------------------------ Cargar archivo ---------------------------------

    uploaded_file = st.file_uploader("Elegir Archivo", type = 'xlsx')
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        #st.dataframe(df1)

        book = load_workbook(uploaded_file)

        pred_clusters = pd.DataFrame(get_clusters(df[x_columns]))
        pred_clusters.rename(columns={0:'Cluster'},inplace=True)
        pred_clusters['Etiqueta_Cluster'] = pred_clusters.Cluster.apply(cluster_label)

        #pred_clusters.reset_index(inplace = True)

        #pred_clusters.set_index(df.index)

        df_new = pd.concat([df,pred_clusters],axis=1)

        #st.write(uploaded_file)

        #with pd.ExcelWriter(buffer, engine = 'openpyxl') as writer:
                #writer.book = book
                #writer.sheets = dict((ws.title, ws) for ws in book.worksheets)    

        #        df_new.to_excel(writer, sheet_name='Cluster_Pred', engine = 'openpyxl',index = False)
        #        writer.close()
                #book.save(uploaded_file)
                #book.close()
        output_file = df_new.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar", output_file,'Cluster.csv') #uploaded_file.name)

elif st.session_state["authentication_status"] == False:
    st.error('Usuario/Contraseña incorrecta')
elif st.session_state["authentication_status"] == None:
    st.warning('Por favor ingrese su usuario y contraseña')

