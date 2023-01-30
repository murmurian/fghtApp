# fghtApp
Tämä on Helsingin yliopiston tietojenkäsittelytieteen kandiohjelman itsenäisesti toteutettu tietokantasovellusten harjoitustyö. Sovellus toimii vapaaottelutietokantana, josta löytyy tietoa vapaaottelijoista, otteluista ja tapahtumista. Lisäksi rekisteröityneet käyttäjät voivat kommentoida otteluita ja pisteyttää ottelut jotka ovat ratkenneet tuomariäänin. Sovelluksessa on kolme käyttäjäroolia: vierailija, (rekisteröitynyt) käyttäjä ja ylläpitäjä. Sovelluksen ominaisuuksia:

Vierailija voi:
* selata ottelijoita, otteluita ja tapahtumia
* hakea ottelijoita, etu- ja sukunimellä, molemmilla tai lempinimellä
* hakea otteluita valitsemiltaan päivämääriltä
* hakea tapahtumia tapahtuman nimellä tai promootion nimellä
* rekisteröityä käyttäjäksi

Edellisten ominaisuuksien lisäksi rekisteröitynyt käyttäjä voi:
* kommentoida otteluita
* pisteyttää tuomariäänillä ratkenneita otteluita
* muokata ja poistaa omia kommenttejaan ja pisteytyksiään

Ylläpitäjä voi lisäksi:
* lisätä, muokata ja poistaa ottelijoita, erätuomareita, otteluita ja tapahtumia
* muokata ja poistaa käyttäjien kommentteja ja pisteytyksiä

## Sovelluksen kokeilu
Sovellusta voi kokeilla tuotannossa osoitteessa [https://divine-violet-8048.fly.dev/](https://divine-violet-8048.fly.dev/). Sovelluksessa on jo valmiiksi lisätty joitakin ottelijoita, otteluita ja tapahtumia. Esim. tapahtuman 'UFC 100' ottelijat ja ottelut on lisätty kokonaisuudessaan. Sovelluksen toiminnot löytyvät yläpalkista ja hakutoiminnot kunkin sivun alusta. Useimmissa listoissa klikkailemalla esim. ottelijan tai tapahtuman nimeä pääsee yksityiskohtaisille sivuille. Sisään- ja uloskirjautuminen, rekisteröityminen ja ylläpitäjän toiminnot löytyvät oikeasta yläkulmasta alasvetovalikoista.

* ylläpitäjän tunnukset ovat: käyttäjätunnus: `admin`, salasana: `AYBABTU1337`

## Vapaaottelun säännöistä
Vapaaottelua otellaan monenlaisilla säännöillä. Tämä sovellus perustuu nykyään yleisimmin ammattilaisvapaaottelussa käyttäviin 'Unified Rules of Mixed Martial Arts' sääntöihin. Tavallisissa otteluissa on kolme viiden minuutin erää, mestaruusotteluissa ja tapahtumien pääotteluissa viisi viiden minuutin erää. Ottelut pisteytään ns. 10 pisteen järjestelmällä, jossa erän voittaja saa 10 pistettä ja häviäjä käytännössä 9 tai vähemmän. 10-10 erät ovat äärimmäisen harvinaisia. Tarkempaa tietoa säännöistä: [https://www.abcboxing.com/wp-content/uploads/2020/02/unified-rules-mma-2019.pdf](https://www.abcboxing.com/wp-content/uploads/2020/02/unified-rules-mma-2019.pdf) ja vapaaottelusta yleensä: [https://en.wikipedia.org/wiki/Mixed_martial_arts](https://en.wikipedia.org/wiki/Mixed_martial_arts).

## Kommentteja sovelluksen toteutuksesta
Alkuperäisenä suunnitelmana sovelluksessa oli tarkoitus, että käyttäjät olisivat voineet pisteyttää otteluissa jokaisen erän erikseen. Ajanpuutteen ja kompeleksisuuden vuoksi, päädyin lopulta rajoittamaan pisteytyksen ottelukohtaiseksi. Suunnitelmissa oli myös lisätä virallisten tuomarien ottelupisteille oma taulunsa, mutta tämä ei päätynyt toteutukseen asti. Sovelluksen haut voisivat olla monipuolisemmat ja muutama tekninen ratkaisu tuntuu jälkikäteen kömpelöltä. Aiemmissa opinnoissa olen käyttänyt enimmäkseen Javaa joten projektissa tuli opittua paljon hieman isomman sovelluksen kirjoittamisesta Pythonilla. Sovellus on toteutettu todella ripeällä aikataululla, mikä epäilemättä näkyy koodin viimeistelemättömyydessä. Opintojen etenemisen kannalta aika ei kuitenkaan riitä sovelluksen tarkempaan hiomiseen.

## Sovelluksen ajaminen paikallisesti
Sovelluksen voi toki ajaa myös paikallisesti kurssin ohjeiden mukaisesti: [https://hy-tsoha.github.io/materiaali/aikataulu/](kts. Esimerkki käynnistysohjeista)