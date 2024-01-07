import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Modeli yükle
rf_model = joblib.load("model.pkl")

def main():
    st.sidebar.title('Streamlit ile ML Uygulaması')
    selected_page = st.sidebar.selectbox('Sayfa Seçiniz..', ["-", "Tahmin Yap"])

    if selected_page == "-":
        welcome_page()
    elif selected_page == "Tahmin Yap":
        predict()

def welcome_page():
    st.title('Streamlit Uygulamasına Hoşgeldiniz 👋')
    st.image('resim.png', use_column_width=True)

def predict():
    st.title('Merhaba, *Streamlit!* 👨‍💻')

    def predict_models(res):
        prediction = rf_model.predict(res)
        return prediction

    def create_prediction_value(ekran_boyutu, ekran_kartı, ram, ssd_kapasitesi, çözünürlük, işlemci_tipi, işletim_sistemi, marka):
        res = pd.DataFrame(data={
            'Ekran_Boyutu': [ekran_boyutu],
            'Ekran_Kartı': [ekran_kartı],
            'Ram': [ram],
            'SSD_Kapasitesi': [ssd_kapasitesi],
            'Çözünürlük': [çözünürlük],
            'İşlemci_Tipi': [işlemci_tipi],
            'İşletim_Sistemi': [işletim_sistemi],
            'Marka': [marka],
        })
        return res

    def load_data():
        m = pd.read_csv("Marka.csv")
        marka = pd.DataFrame(m)

        e = pd.read_csv("Ekran Kartı.csv")
        ekran = pd.DataFrame(e)

        i_s = pd.read_csv("İşletim Sistemi.csv")
        i_sis = pd.DataFrame(i_s)

        i_t = pd.read_csv("İşlemci Tipi.csv")
        i_tip = pd.DataFrame(i_t)

        c = pd.read_csv("Çözünürlük.csv")
        cöz = pd.DataFrame(c)

        return marka, ekran, i_sis, i_tip, cöz

    # Verileri yükle
    marka, ekran, i_sis, i_tip, cöz = load_data()

    # Tahmin değerlerini kullanıcı girişiyle al
    selected_ekran_boyutu = st.number_input('Ekran Boyutu', min_value=10, max_value=18)
    st.write("Ekran Boyutu: " + str(selected_ekran_boyutu) + " inç")

    selected_ekran_kartı = ekran_index(ekran, st.selectbox('Ekran Kartı Seçiniz..', ekran))

    selected_ram = st.slider("Ram", min_value=1, max_value=128)
    st.write("Ram: " + str(selected_ram) + " GB")

    selected_ssd_kapasitesi = st.slider("SSD Kapasitesi", min_value=32, max_value=8192)
    st.write("SSD Kapasitesi: " + str(selected_ssd_kapasitesi) + " GB")

    selected_çözünürlük = çözünürlük_index(cöz, st.selectbox('Çözünürlük Seçiniz..', cöz))

    selected_işlemci_tipi = işlemci_index(i_tip, st.selectbox('İşlemci tipi seçniz..', i_tip))

    selected_işletim_sistemi = işletim_index(i_sis, st.selectbox('İşletim Sistemi Seçiniz..', i_sis))

    selected_marka = marka_index(marka, st.selectbox('Marka Seçiniz..', marka))

    if st.button("Tahmin Yap"):
        prediction_value = create_prediction_value(selected_ekran_boyutu, selected_ekran_kartı, selected_ram,
                                                   selected_ssd_kapasitesi, selected_çözünürlük, selected_işlemci_tipi,
                                                   selected_işletim_sistemi, selected_marka)
        result = predict_models(prediction_value)
        if result is not None:
            st.success('Tahmin Başarılı')
            st.balloons()
            st.write("Tahmin Edilen Fiyat: " + str(float(result)) + " TL")
        else:
            st.error('Tahmin yaparken hata meydana geldi..!')

def marka_index(marka, aranan_marka):
    index = marka[marka["Marka"] == aranan_marka].index
    return index[0] + 2

def ekran_index(ekran, aranan_ekran):
    index = ekran[ekran["Ekran Kartı"] == aranan_ekran].index
    return index[0] + 2

def işletim_index(i_sis, aranan_işletim):
    index = i_sis[i_sis["İşletim Sistemi"] == aranan_işletim].index
    return index[0] + 2

def işlemci_index(i_tip, aranan_işlemci):
    index = i_tip[i_tip["İşlemci Tipi"] == aranan_işlemci].index
    return index[0] + 2

def çözünürlük_index(cöz, aranan_çözünürlük):
    index = cöz[cöz["Çözünürlük"] == aranan_çözünürlük].index
    return index[0] + 2









if __name__ == "__main__":
    main()
