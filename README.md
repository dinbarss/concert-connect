# Concert-connect

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan konserttilippuilmoituksia.
* Käyttäjä näkee sovellukseen lisätyt liput (omat ja muiden käyttäjien).
* Käyttäjä pystyy etsimään lippuja hakusanalla (esim. artistin, paikan tai päivämäärän perusteella).
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät liput.
* Käyttäjä pystyy valitsemaan lipuille yhden tai useamman luokittelun (esim. K-pop, J-pop).
* Käyttäjä pystyy lisäämään kommentteja ja kysymyksiä lippuilmoituksiin.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
