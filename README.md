# IUM Discount prediction service

Autorzy:

Czobot Stanisław

Kucharki Michał

Projekt z przedmiot Inżynieria Uczenia Maszynowego.
Projekt składa się z dwóch zasadniczych części:
  - obróbka danych wejściowych, tworzenie i trenowanie modeli (wykonane w notatnikach jupyter)
  - aplikakacja webowa wykorzystująca wcześniej przygotowane modele do predykcji wartości zniżek, po wybraniu odpowiedniego klienta i produktu (aplikacja napisana w języku Python z wykorzystaniem frameworka Flask)

## Instalacja
W celu zainstalowania potrzebnych pakietów należ wykonać komendę:

```
pip install -r requirements.txt
```

lub pip3

## Uruchomienie
Serwer aplikacji uruchomić można komendą:

```
python -m app .
```

lub python3

Tak uruchomiony serwer można włączyć w dowolnej przeglądarce pod adresem:

```
http://127.0.0.1:5000/
```
