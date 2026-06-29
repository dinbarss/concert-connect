# Concert Connect
Concert Connect on verkkosovellus, jossa käyttäjät voivat myydä ja ostaa konserttilippuja.

## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan konserttilippuilmoituksia
* Käyttäjä näkee sovellukseen lisätyt liput (omat ja muiden käyttäjien)
* Käyttäjä pystyy etsimään lippuja hakusanalla (artisti, paikka, kuvaus, kategoria)
* Käyttäjä pystyy valitsemaan lipulle yhden tai useamman kategorian
* Käyttäjä pystyy näkemään muiden käyttäjien profiilisivut ja heidän ilmoituksensa
* Käyttäjä pystyy kommentoimaan lippuilmoituksia ja esittämään kysymyksiä

## Asennus ja käyttöönotto

### 1. Kloonaa repositorio
```
git clone https://github.com/dinbarss/concert-connect.git
cd concert-connect
```

### 2. Luo ja aktivoi virtuaaliympäristö
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Asenna Flask
```
pip install flask
```

### 4. Alusta tietokanta
```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

### 5. Käynnistä sovellus
```
flask run
```

Sovellus käynnistyy osoitteeseen: http://127.0.0.1:5000

## Testaaminen
1. **Rekisteröidy**: Luo uusi tunnus "Rekisteröidy"-linkistä
2. **Kirjaudu sisään**: Kirjaudu luomallasi tunnuksella
3. **Lisää lippu**: Lisää uusi konserttilipun ilmoitus kategorialla/kategorioilla
4. **Etsi**: Käytä hakutoimintoa etsiäksesi lippuja
5. **Lipun sivu**: Klikkaa lippua nähdäksesi tarkemmat tiedot ja kommentit
6. **Kommentoi**: Jätä kommentti toisen käyttäjän lippuilmoitukseen
7. **Käyttäjäprofiili**: Klikkaa myyjän nimeä nähdäksesi hänen profiilisivunsa
8. **Muokkaa/poista**: Kokeile omien lippujesi muokkaamista ja poistamista
9. **Kirjaudu ulos**: Kirjaudu ulos järjestelmästä
