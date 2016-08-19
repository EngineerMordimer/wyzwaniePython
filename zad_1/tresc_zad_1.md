## [\#wyzwaniepython](http://www.wykop.pl/tag/wyzwaniepython/) Zadanie 03

### Łatwa
Propozycja:
"Konsolowy eksplorator plików (poruszanie się folderach,
wyświetlanie informacji o plikach, może jakieś kopiowanie, usuwanie,
tworzenie folderów)."

* przydatna biblioteka **shutil** [Python 2](https://docs.python.org/2.7/library/shutil.html) 
[Python 3](https://docs.python.org/3/library/shutil.html)

Stworzymy po prostu pseudokonsolę, czyli program, który w pętli będzie wczytywał polecenia
na plikach oraz odpowiednio na nie reagował.

#### Polecenia do obsłużenia:
 - `pwd` - wraca napis zawierający pełną ścieżkę bezwzględną do aktualnego katalogu
 - `cd <nazwa_katalogu>` - przechodzi do katalogu `<nazwa_katalogu>` (zmienia aktualny katalog,
czyli ten wskazywany przez `pwd`)
 - `cp <sciezka1> <sciezka2>` - kopiuje **plik** lub **katalog** ze `<sciezka1>` do `<sciezka2>`
 - `mv <sciezka1> <sciezka2>` - przenosi **plik** lub **katalog** ze `<sciezka1>` do `<sciezka2>`
 - `info <sciezka1>` - zwraca informacje o **pliku** lub **katalogu** z `<sciezka1>` (format niżej)
 - `ls` - wyświetla zawartość aktualnego (czyli zwracanego przez polecenie `pwd`) **katalogu**
 - `rm <sciezka>` - usuwa **plik** lub **katalog** spod `<sciezka>`
 - `touch <sciezka>` - tworzy **pusty** plik pod `<sciezka>`

#### Format polecenia `info`
Polecenie `info` powinno wyświetlać następujące informacje:
* typ - plik/katalog/inny
* ścieżkę bezwzględną podanego **pliku** lub **katalogu**
* pełny (tzn. w przypadku katalogu sumaryczny rozmiar całej jego zawartości) rozmiar w bajtach **pliku** lub **katalogu**
* **[w przypadku katalogów]** liczbę plików (czyli bez katalogów) znajdujących się wewnątrz
* czas zwracany przez **os.path.getctime()**
* czas zwracany przez **os.path.getmtime()**


Przykład dla **katalogu** `dir1`:
```
typ: katalog
sciezka: /home/raw/docs/dir1
rozmiar: 5813B
liczba_plikow: 31
ctime: 2016-05-28
mtime: 2015-11-03
```

#### Wymagania
 * rozwiązanie **musi** zawierać funkcję `parse(cmd, *args, **kwargs)`, która będzie interpretowała polecenie podane jako `cmd`
   z argumentami występującymi po nim oraz w przypadku poleceń wypisujących informacje (`pwd`, `ls`, `info`) zwróci napis je
   je zawierający; w przypadku pozostałych poleceń wykona związane z nimi akcje i zwróci **None** - pozwoli to wygodnie
   testować podsyłane rozwiązania i je ujednolici

### Trudna
Graficzny eksplorator plików (biblioteka do wyboru: pyQt/tkinter/pyGTK/ncurses), pozwalający wykonać takie akcje jak
eksplorator z wersji łatwej.

___

___

___


## [\#wyzwaniepython](http://www.wykop.pl/tag/wyzwaniepython/) Zadanie 02

### Łatwa
Rekurencyjne wyszukiwanie plików w danym katalogu i zrobienie histogramu w
osobnym pliku tekstowym z częstotliwością (tzn. informacją jaką część
wszystkich plików są pliki z danym rozszerzeniem) występowania plików z danym
rozszerzeniem oraz sumą ich rozmiarów.

#### Wymagania:
 - odpowiednie formatowanie: kolumny wyrównanie do prawej strony, pierwsza
   o szerokości 5 znaków, druga 15, trzecia 60 (w trzeciej 10 spacji przed
   pierwszym znakiem `#`)
 - katalog jak i nazwa pliku wyjściowego muszą być przyjmowane jako
   argumenty programu (ułatwi to testowanie):
       `./prog nazwa_katalogu nazwa_pliku_wyjsciowego`
 - rozmiar podajemy w bajtach, po rozszerzeniu
 - histogram ma składać się ze znaków `#` i ma mieć szerokość 50 znaków,
   czyli jeśli w katalogu występują wyłącznie pliki z rozszerzeniem .txt,
   obok tego rozszerzenie, po sumie rozmiarów tych plików, ma się znaleźć
   50 znaków '#'.

#### Przykład
Załóżmy, że w podanym katalogu znajduje się 12 plików:
```
6 z rozszerzeniem  .txt o rozmiarze    5932B
3 z rozszerzeniem .jpeg o rozmiarze   10000B
2 z rozszerzeniem  .mp3 o rozmiarze  203151B
1 z rozszerzeniem  .zip o rozmiarze   43131B
```

Rozwiązanie powinno zapisać do podanego pliku następujące dane (bez pierwszej
linii, służy ona jedynie przedstawieniu szerokości kolumn, 5-15-60):

```
#####***************%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  txt          5932B                                   #########################
 jpeg         10000B                                                ############
  mp3        203151B                                                    ########
  zip         43131B                                                        ####
```

#### Wyjaśnienie
Plików z rozszerzeniem `.txt` jest **6**, co stanowi **50%** wszystkich, więc przy `txt`
powinno być **25** znaków `#` (**50%** z **50**). Plików z rozszerzeniem `.mp3` jest **2**, co
stanowi **16,(6)%** wszystkich plików, zatem przy tym rozszerzeniu powinno być **8**
znaków `#` (**16,(6)%** z 50 to **8,(3)** - zaokrąglamy to więc w dół). Analogicznie dla
pozostałych rozszerzeń.

Metoda wspomnianego wyżej zaokrąglania musi być kompatybilna z wbudowaną funkcją round.

### Trudna
~~Zapisanie danych o plikach z danego katalogu do bazy danych (takie dane jak
ścieżka, rozmiar, rozszerzenie, data modyfikacji). Moglibyśmy to rozbudować o
sprawdzanie, czy pliki i podkatalogi danego katalogu zmieniły się od ostatniego
zapisu do bazy - nawet poza #wyzwaniepython ;-). Do ustalenia schemat bazy.~~

  `./prog nazwa_katalogu nazwa_bazy`

Zapisanie danych o obiektach z katalogu podanego jako pierwszy argument do bazy
danych **SQLite** o nazwie podanej jako drugi argument z następującymi tabelami:

#### objects - tabela z wszystkimi obiektami znajdującymi się w podanym katalogu oraz on sam
```
|         objects         |
---------------------------
| id | path | type | size |
```
* **id** - unikalne id
* **path** - ścieżka rozpoczynająca się od katalogu podanego jako argument dla programu
* **type** - `f` plik, `d` katalog, `o` inny (symlink itp.)
* **size** - rozmiar obiektu, w przypadku katalogów suma rozmiarów jego elementów

#### cardinality - tabela zawierająca liczbę elementów danego katalogu
```
|      cardinality     |
------------------------
| id | nbr_of_elements |
```
* **id** - **id** katalogu z tabeli **objects**
* **nbr_of_elements** - liczba elementów w danym katalogu (rekurencyjnie wszystkich plików i katalogów)

#### checksums - tabela zawierająca sumę kontrolną MD5 danego pliku
```
|       checksums      |
------------------------
| id |     checksum    |
```
* **id** - **id** pliku z tabeli **objects**
* **checksum** - suma kontrolna MD5

===

### Przydatne linki:
* [SQLite](https://www.sqlite.org/)
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [String methods](https://docs.python.org/3/library/stdtypes.html#string-methods)

### Czas na wykonanie
**1 tydzień, do 27.07.2016**

___

___

___



Zadanie 1
========================

Otrzymujesz katalog zawierający 1000 plików o losowych nazwach które są wypełnione 3 losowymi znakami. Twoim zadaniem jest:
Wersja łatwa

- Odczytać rok i miesiąc modyfikacji pliku
- skopiowac wszystkie pliki z danego roku do do jednego katalogu a poźniej to samo dla miesięcy

___

Wersja trudna

- To co łatwa
- Znaleźć wszystkie duplikaty.

___

Przydatne biblioteki:

* Time - https://docs.python.org/2/library/time.html
* os.path - https://docs.python.org/2/library/os.path.html

Czas na wykonanie to 2 tygodnie tj. do 17.07.2016 wtedy też opublikujemy wpis gdzie będziecie mogli wstawić linka do swojego programu. Nie publikujcie proszę wczesniej rozwiązań bo zepsujecie zabawę.

Linki:

* Pliki testowe - https://github.com/qofnaught/wykop_wyzwaniepython/blob/master/edycja1/test.zip
* Github - https://github.com/qofnaught/wykop_wyzwaniepython/tree/master/edycja1
* Spam lista - http://mirkolisty.pvu.pl/list/qIRpnpHg3WM8YOv5
