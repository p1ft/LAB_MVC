# Kolekcja ulubionych przepisow do koktajli

## Spis tresci

- [Opis projektu](#opis-projektu)
- [Opis funkcjonalnosci](#opis-funkcjonalnosci)
- [Instrukcja uruchomienia](#instrukcja-uruchomienia)
- [Struktura projektu](#struktura-projektu)

## Opis projektu

Aplikacja pozwala dodawac, przegladac, edytowac i usuwac przepisy na koktajle. Kazdy przepis zawiera nazwe, skladniki oraz instrukcje przygotowania. Projekt korzysta z bazy danych SQLite oraz przykladowych danych zapisanych w pliku `initial_data.json`.

Najwazniejsze elementy projektu:

- `models.py` - zawiera definicje modeli bazy danych
- `views.py` - odpowiada za obsluge zapytan HTTP i przekazywanie danych do szablonow
- `urls.py` - definiuje adresy URL dla listy, szczegolow, dodawania, edycji i usuwania przepisow
- `forms.py` - zawiera formularz `ModelForm` wykorzystywany przy tworzeniu i edycji danych
- `templates/` - przechowuje widoki HTML wyswietlane w przegladarce
- `static/` - zawiera plik CSS odpowiedzialny za podstawowy wyglad aplikacji

Glownym modelem jest `CocktailRecipe`, ktory przechowuje dane przepisu. Dodatkowo projekt zawiera modele `Category` oraz `Ingredient`, dzieki czemu mozna porzadkowac przepisy wedlug kategorii i przypisywac do nich wiele skladnikow.

## Opis funkcjonalnosci

- Wyswietlanie listy przepisow na koktajle - na stronie glownej aplikacja pokazuje wszystkie zapisane przepisy w formie tabeli. Uzytkownik widzi najwazniejsze informacje, takie jak nazwa, kategoria, poziom intensywnosci i data dodania
- Wyswietlanie szczegolow pojedynczego przepisu - po wybraniu przepisu otwiera sie osobny widok, w ktorym prezentowane sa wszystkie dane dotyczace koktajlu: nazwa, skladniki, instrukcja przygotowania oraz dodatkowe informacje
- Dodawanie nowego przepisu za pomoca formularza - nowy przepis dodawany jest przez formularz oparty o `ModelForm`, co upraszcza wprowadzanie danych i laczy formularz bezposrednio z modelem bazy danych
- Edycja istniejacego przepisu - aplikacja pozwala otworzyc formularz z juz zapisanymi danymi i wprowadzic zmiany bez koniecznosci usuwania calego rekordu
- Usuwanie przepisu z potwierdzeniem - przed usunieciem przepisu wyswietlany jest ekran potwierdzenia, co zmniejsza ryzyko przypadkowego skasowania danych
- Przypisywanie kategorii do przepisu - przepisy moga byc przypisywane do kategorii, co pomaga uporzadkowac kolekcje i ulatwia filtrowanie danych
- Dodawanie skladnikow do przepisu przy pomocy relacji wiele-do-wielu - skladniki sa przechowywane jako osobny model, a jeden przepis moze byc polaczony z wieloma skladnikami. To rozwiazanie jest bardziej czytelne niz wpisywanie wszystkiego w jedno pole tekstowe
- Filtrowanie i wyszukiwanie przepisow po nazwie, kategorii oraz poziomie intensywnosci - w widoku listy dostepny jest formularz filtrowania, ktory pozwala szybko znalezc konkretny przepis albo ograniczyc widok tylko do wybranej grupy koktajli
- Walidacja formularza podczas dodawania i edycji danych - formularz sprawdza, czy dane spelniaja podstawowe warunki, na przyklad czy nazwa nie jest za krotka i czy nie powtarza sie juz w bazie danych
- Prosty panel administracyjny Django do zarzadzania danymi - projekt wykorzystuje wbudowany panel `Django admin`, dzieki czemu mozna dodawac i edytowac przepisy, skladniki oraz kategorie rowniez z poziomu panelu administratora
- Dolaczony plik z przykladowymi danymi do szybkiego uruchomienia projektu - w folderze `fixtures` znajduje sie plik `initial_data.json`, ktory pozwala szybko zaladowac testowe rekordy i od razu sprawdzic dzialanie aplikacji

## Instrukcja uruchomienia

### 1. Klonowanie repozytorium

```bash
git clone <adres_repozytorium>
cd LAB_MVC/Project
```

### 2. Instalacja zaleznosci

```bash
pip install -r requirements.txt
```

### 3. Przejscie do katalogu projektu Django

```bash
cd cocktail_project
```

### 4. Wykonanie migracji bazy danych

```bash
python manage.py migrate
```

### 5. Zaladowanie przykladowych danych

```bash
python manage.py loaddata initial_data.json
```

### 6. Uruchomienie serwera developerskiego

```bash
python manage.py runserver
```

Po uruchomieniu aplikacja bedzie dostepna pod adresem:

```text
http://127.0.0.1:8000/cocktails/
```

## Struktura projektu

```text
LAB_MVC/
|-- Project/
    |-- README.md
    |-- requirements.txt
    `-- cocktail_project/
        |-- manage.py
        |-- db.sqlite3
        |-- cocktail_project/
        |   |-- settings.py
        |   |-- urls.py
        |   |-- asgi.py
        |   `-- wsgi.py
        `-- cocktails/
            |-- models.py
            |-- views.py
            |-- forms.py
            |-- urls.py
            |-- admin.py
            |-- tests.py
            |-- migrations/
            |-- templates/
                `-- cocktails/
            |-- static/
            `-- fixtures/
                `-- initial_data.json

```

### Krotki opis katalogow

- `Project/cocktail_project/` - glowny katalog projektu Django.
- `cocktail_project/` - konfiguracja projektu, plik ustawien i routing glowny.
- `cocktails/` - aplikacja odpowiedzialna za obsluge przepisow na koktajle.
- `templates/` - szablony HTML wyswietlane uzytkownikowi.
- `static/` - pliki statyczne, na przyklad arkusz stylow CSS.
- `migrations/` - pliki migracji bazy danych.
- `fixtures/initial_data.json` - przykladowe dane do zaladowania do aplikacji.
