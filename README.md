Liidimanageri -Flask-sovellus
Suoritusympäristöön työntö (git push) vaatii siihen sopivaa gitignore- ja .env-tiedostoa.

Huom. Tässä flask-bootstrap4 sisältää paikallisen korjauksen tiedostoon flask_bootstrap/templates/bootstrap/__init__.py. Korjauksessa on toimiva CDN bootstrapille ja fontawesomella.

Liidimanagerissa on React-käyttöliittymän rajapinta reactapi-Blueprinttinä. 

Rajapinnassa on sovellettu Flask-login-kirjastoa eli session-autentikointia token-autentikointiratkaisujen sijaan,
jotta Flask-sovelluksen käyttöliittymän toteutukselle olisi useita mahdollisia vaihtoehtoja kuten HTML ja React. 

@login_required-suojauksen kirjautumattoman käyttäjän edelleenohjaus login-sivulle on korvattu json-tyyppisellä return-lausekkeella. Tämä voitaisiin toteuttaa A) Flask-loginin LoginManagerin unauthorized_handlerillä, mutta jotta samaa Flask-sovellusta voidaan käyttää myös html-käyttöliittymien kanssa, B) LoginManagerin login_view asetetaan Blueprintille tyhjäksi ja näin syntyvät 401-virhekeskeytykset käsitellään Blueprintin omalla 401-virhekäsittelijällä CORS:in vaatimat Headerit huomioon ottaen.  Huom. Tätä ratkaisua ei näyttäisi löytyvän verkosta ainakaan kovin helposti. Yksi ratkaisu voisi olla C) oman @login_required-dekoraattorin laatiminen.

Tästä ratkaisusta puuttuu vielä lomakkeiden CSRF-suojaus, vrt. quick_form.
