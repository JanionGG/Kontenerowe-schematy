# Aplikacja do Rozliczeń Spółki

Aplikacja webowa napisana w Streamlit do comiesięcznego rozliczania przychodów i kosztów w spółce. Dane zapisywane są lokalnie w pliku `rozliczenia.csv`.

## Uruchomienie lokalnie

```bash
pip install streamlit pandas altair
streamlit run app.py
```

## Funkcjonalności

- Logowanie dla dwóch użytkowników
- Wprowadzanie przychodów, kosztów i podziałów wypłat
- Automatyczne obliczanie faktur z VAT
- Historia miesięcy i sumaryczne statystyki
- Interaktywne wykresy

