import streamlit as st
import pandas as pd
import datetime
import hashlib
import altair as alt

st.set_page_config(page_title="Rozliczenia Spółki", layout="wide")

# Plik danych CSV
data_file = "rozliczenia.csv"

# Uwierzytelnianie
USERS = {
    "jan": "haslojan",
    "kamila": "haslokamila"
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    return username in USERS and USERS[username] == password

with st.sidebar:
    st.title("Logowanie")
    username = st.text_input("Użytkownik")
    password = st.text_input("Hasło", type="password")
    login_btn = st.button("Zaloguj")

if not (username and password and check_login(username, password)):
    st.warning("Wprowadź poprawne dane logowania.")
    st.stop()

# Wczytaj dane z pliku (lub stwórz jeśli nie istnieje)
def load_data():
    try:
        return pd.read_csv(data_file, parse_dates=["data"])
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "data", "przychod", "koszty_stale", "koszty_stale_jan", "koszty_zmienne",
            "do_wyplaty", "jan", "dom", "ila_na_jan", "bluebird",
            "fv_jan", "fv_bluebird"
        ])

def save_data(df):
    df.to_csv(data_file, index=False)

# Funkcja VAT
VAT = 0.23
def brutto(kwota_netto):
    return round(kwota_netto * (1 + VAT), 2)

# Interfejs
st.title("Aplikacja do rozliczeń spółki")

# Wybór miesiąca
data_miesiaca = st.date_input("Wybierz miesiąc", datetime.date.today().replace(day=1))

# Przychód
przychod = st.number_input("Przychód brutto (PLN)", min_value=0.0, step=100.0)

# Koszty stałe
st.subheader("Koszty stałe")
koszty_stale = {}
koszty_specjalne = ["ZUS + księgowość", "Stan", "Paliwo"]
stale_keys = []

with st.expander("Dodaj koszty stałe"):
    for i in range(5):
        kol1, kol2 = st.columns([2, 1])
        key = kol1.text_input(f"Nazwa kosztu {i+1}", key=f"nazwa_{i}")
        val = kol2.number_input(f"Kwota {i+1}", min_value=0.0, key=f"kwota_{i}")
        if key:
            koszty_stale[key] = val
            stale_keys.append(key)

# Koszty zmienne
koszty_zmienne = st.number_input("Koszty zmienne (PLN)", min_value=0.0, step=100.0)

# Podział wypłat
st.subheader("Podział wypłaty (kwoty netto)")
jan_kwota = st.number_input("Jan", min_value=0.0, step=100.0)
dom_kwota = st.number_input("Dom", min_value=0.0, step=100.0)
ila_kwota = st.number_input("Ila na Jan", min_value=0.0, step=100.0)
bluebird_kwota = st.number_input("BlueBird", min_value=0.0, step=100.0)

# Obliczenia
suma_kosztow_stalych = sum(koszty_stale.values())
suma_kosztow_jan = sum([koszty_stale[k] for k in koszty_stale if k in koszty_specjalne])
do_wyplaty = przychod - suma_kosztow_stalych - koszty_zmienne
fv_jan = brutto(jan_kwota + dom_kwota + ila_kwota + suma_kosztow_jan)
fv_bluebird = brutto(bluebird_kwota)

# Pokaz wyniki
st.markdown("### Podsumowanie")
st.write(f"Przychód brutto: {przychod} PLN")
st.write(f"Koszty stałe: {suma_kosztow_stalych} PLN")
st.write(f"Koszty zmienne: {koszty_zmienne} PLN")
st.write(f"Kwota do wypłaty: {do_wyplaty} PLN")
st.write(f"Faktura Jan Kierwiak (brutto): {fv_jan} PLN")
st.write(f"Faktura BlueBird (brutto): {fv_bluebird} PLN")

# Zapisz dane
data = load_data()

if st.button("Zapisz miesiąc"):
    nowy_wiersz = pd.DataFrame([{
        "data": data_miesiaca,
        "przychod": przychod,
        "koszty_stale": suma_kosztow_stalych,
        "koszty_stale_jan": suma_kosztow_jan,
        "koszty_zmienne": koszty_zmienne,
        "do_wyplaty": do_wyplaty,
        "jan": jan_kwota,
        "dom": dom_kwota,
        "ila_na_jan": ila_kwota,
        "bluebird": bluebird_kwota,
        "fv_jan": fv_jan,
        "fv_bluebird": fv_bluebird
    }])
    data = pd.concat([data, nowy_wiersz], ignore_index=True)
    save_data(data)
    st.success("Zapisano dane!")

# Historia
st.markdown("## Historia miesięcy")
data = load_data()
data_sorted = data.sort_values(by="data", ascending=False)
st.dataframe(data_sorted, use_container_width=True)

# Statystyki
st.markdown("## Statystyki sumaryczne")
st.write("Łączne wypłaty:")
st.write("- Jan Kierwiak:", data[["jan", "dom", "ila_na_jan"]].sum().sum(), "PLN")
st.write("- BlueBird:", data["bluebird"].sum(), "PLN")
st.write("- Wszystkie faktury brutto (Jan):", data["fv_jan"].sum(), "PLN")
st.write("- Wszystkie faktury brutto (BlueBird):", data["fv_bluebird"].sum(), "PLN")

# Wykresy
st.markdown("## Wykresy")
if not data.empty:
    chart_data = data[["data", "przychod", "koszty_stale", "koszty_zmienne", "do_wyplaty"]].melt("data")
    chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x="data:T",
        y="value:Q",
        color="variable:N",
        tooltip=["data:T", "variable:N", "value:Q"]
    ).properties(width=800, height=400)
    st.altair_chart(chart, use_container_width=True)
