# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:68:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:74:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:103:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:178:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:214:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:222:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:222:0: R0911: Too many return statements (7/6) (too-many-return-statements)
app.py:286:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:318:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:318:0: R0911: Too many return statements (7/6) (too-many-return-statements)
app.py:393:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:413:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:6:0: W0611: Unused g imported from flask (unused-import)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 8.71/10 (previous run: 8.71/10, +0.00)

```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

## Docstring-ilmoitukset

Suuri osa raportin ilmoituksista on seuraavan tyyppisiä ilmoituksia:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Nämä ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole docstring-kommentteja. Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja.

## Liian monta paluuarvoa

Raportissa on seuraavat ilmoitukset liittyen funktion paluuarvojen määrään:

```
app.py:177:0: R0911: Too many return statements (7/6) (too-many-return-statements)
app.py:273:0: R0911: Too many return statements (7/6) (too-many-return-statements)
```

Nämä ilmoitukset koskevat lipun lisäämiseen (`/send`) ja muokkaamiseen (`/update`) liittyviä funktioita, joissa syötteet (artisti, paikka, hinta, päivämäärä, kategoriat) tarkistetaan erikseen ja jokaisesta virheellisestä syötteestä palautetaan oma virheilmoitus. Sovelluksen kehittäjän näkemyksen mukaan on selkeämpää pitää kaikki yhteen lomakkeeseen liittyvä validointi samassa funktiossa kuin pirstoa se erillisiin funktioihin.

## Vakion nimi

Raportissa on seuraava ilmoitus liittyen vakion nimeen:

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Tässä koodin päätasolla määritelty muuttuja tulkitaan vakioksi, jonka nimen tulisi olla kirjoitettu suurilla kirjaimilla. Kuitenkin sovelluksen kehittäjän näkemyksen mukaan tässä tilanteessa näyttää paremmalta, että muuttujan nimi on pienillä kirjaimilla. Muuttujaa käytetään koodissa näin:

```python
app.secret_key = config.secret_key
```

## Vaarallinen oletusarvo

Raportissa on seuraavat ilmoitukset liittyen vaaralliseen oletusarvoon:

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa funktiota:

```python
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

Tässä parametrin oletusarvo `[]` on tyhjä lista. Tässä ongelmaksi voisi tulla, että sama oletusarvona oleva tyhjä listaolio on jaettu kaikkien funktion kutsujen kesken ja jos jossain kutsussa listan sisältöä muutettaisiin, tämä muutos näkyisi myös muihin kutsuihin. Käytännössä tässä tapauksessa tämä ei kuitenkaan haittaa, koska koodi ei muuta listaoliota.
