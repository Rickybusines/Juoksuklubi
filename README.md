# Juoksuklubi

- Sivulla käyttäjät voivat etsiä juoksuseuraa tekemällä ilmoituksia ajan ja paikan perusteella
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ilmoituksia.
- Käyttäjä näkee sovellukseen lisätyt ilmoitukset.
- Käyttäjä pystyy etsimään ilmoituksia ajan, paikan, juoksutahdin ja lenkin pituuden perusteella.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän tekemät ilmoitukset ja kuinka monelle juoksulle käyttäjä on ilmoittautunut.
- Käyttäjä pystyy valitsemaan ilmoitukselle missä tahdissa haluaa juosta, esim hidas, keskinopea tai nopeaa lenkki.
- Käyttäjä pystyy ilmoittautumaan mukaan lenkille
- Käyttäjä pystyy perumaan ilmoittautumisen


Sovelluksen testaus:

- Asenna flask-kirjasto terminaalissa:

$ pip install flask

- Luo itsellesi kansio
- Mene kansioon terminaalin kautta
- Lataa sovellus Githubista: $ git clone https://github.com/Rickybusines/Juoksuklubi.git
- Luo virtuaaliympäristö: $ python3 -m venv venv
- Aktivoi virtuaaliympäristö: $ source venv/bin/activate

Luo tietokantaan taulut:

  - $ sqlite3 database.db < schema.sql
  - $ sqlite3 database.db < init.sql

Käynnistä sovellus:
$ flask run
