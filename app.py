import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(page_title="🩺 AI Ön Tanı Asistanı", page_icon="🩺", layout="centered")
load_dotenv()

st.title("🩺 AI Destekli İlk Tanı Asistanı")
st.markdown("**ÖNEMLİ UYARI:** Bu uygulama sadece ön bilgilendirme amaçlıdır. Kesin teşhis için mutlaka doktora başvurun.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

yas = st.number_input("Yaşınız", min_value=1, max_value=120, value=35)
cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın", "Belirtmek istemiyorum"])
semptom_text = st.text_area("Semptomlarınızı detaylı yazın", placeholder="Örnek: 3 gündür ateş, öksürük, yorgunluk...", height=150)
ek_bilgi = st.text_area("Ek bilgiler (alerji, ilaç vs.)", height=80)

if st.button("🔍 Ön Tanıyı Hesapla", type="primary"):
    if not semptom_text:
        st.error("Lütfen semptom yazın.")
    else:
        with st.spinner("AI analiz ediyor..."):
            prompt = f"""Sen deneyimli bir doktor asistanısın. Hasta bilgileri:
Yaş: {yas}
Cinsiyet: {cinsiyet}
Semptomlar: {semptom_text}
Ek: {ek_bilgi if ek_bilgi else 'Yok'}

Olası ön tanıları Türkçe olarak sırala. Her zaman en altta 'Bu sadece AI tahmini, doktora danışın' uyarısını koy."""

            response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.7)
            st.markdown(response.choices[0].message.content)
