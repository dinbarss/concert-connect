# Concert Connect
Concert Connect on verkkosovellus, jossa käyttäjät voivat myydä ja ostaa konserttilippuja.

## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan konserttilippuilmoituksia
* Käyttäjä näkee sovellukseen lisätyt liput (omat ja muiden käyttäjien)
* Käyttäjä pystyy etsimään lippuja hakusanalla (artisti, paikka, kuvaus)
* Käyttäjä pystyy selaamaan lippuja kategorioittain
* Käyttäjä pystyy näkemään muiden käyttäjien profiilisivut ja heidän ilmoituksensa
* Käyttäjä pystyy kommentoimaan lippuilmoituksia ja esittämään kysymyksiä

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

## Testaaminen
1. **Rekisteröidy**: Luo uusi tunnus "Rekisteröidy"-linkistä
2. **Kirjaudu sisään**: Kirjaudu luomallasi tunnuksella
3. **Lisää lippu**: Lisää uusi konserttilipun ilmoitus kategorialla
4. **Etsi**: Käytä hakutoimintoa etsiäksesi lippuja
5. **Lipun sivu**: Klikkaa lippua nähdäksesi tarkemmat tiedot ja kommentit
6. **Kommentoi**: Jätä kommentti toisen käyttäjän lippuilmoitukseen
7. **Käyttäjäprofiili**: Klikkaa myyjän nimeä nähdäksesi hänen profiilisivunsa
8. **Muokkaa/poista**: Kokeile omien lippujesi muokkaamista ja poistamista
9. **Kirjaudu ulos**: Kirjaudu ulos järjestelmästä

Sovellus käynnistyy osoitteeseen: http://127.0.0.1:5000

## Testaus suurella tietomäärällä
 
Sovellus on testattu `seed.py`-skriptillä seuraavilla määrillä:
 
| Entiteetti | Määrä |
|---|---|
| Käyttäjät | 1 000 |
| Liput | 1 000 000 |
| Kommentit | 10 000 000 |
 
Etusivun latausaika on noin 1.4-2 sekuntia. Hidas suoritusaika johtuu siitä, että kysely yhdistää neljä taulua ja käyttää `GROUP_CONCAT`-funktiota kategorioiden kokoamiseen. Tietokantaan lisättiin indeksit, jotka nopeuttivat sivulatauksia noin 2 sekunnista 1.4 sekuntiin.


