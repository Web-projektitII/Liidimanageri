Liidimanageri -Flask-sovellus

- session-autentikointi Flask-login myös Reactille
- CORS-Headerit Cross origin resource sharing -menettelylle
- CSRF-token-suojaus (cross site request forgery) lomakkeille
  ja kutsuille

Huom. Tässä flask-bootstrap4 sisältää paikallisen korjauksen tiedostoon flask_bootstrap/templates/bootstrap/__init__.py. Korjauksessa on toimiva CDN bootstrapille ja fontawesomella.

Liidimanagerissa on React-käyttöliittymän rajapinta reactapi-Blueprinttinä. 

Rajapinnassa on sovellettu Flask-login-kirjastoa eli session-autentikointia token-autentikointiratkaisujen sijaan,
jotta Flask-sovelluksen käyttöliittymän toteutukselle olisi useita mahdollisia vaihtoehtoja kuten HTML ja React. 

@login_required-suojauksen kirjautumattoman käyttäjän edelleenohjaus login-sivulle on korvattu json-tyyppisellä response-lausekkeella. Tämä voitaisiin toteuttaa: 

A) Flask-loginin LoginManagerin unauthorized_handlerillä, mutta jotta samaa Flask-sovellusta voidaan käyttää myös html-käyttöliittymien kanssa, 

B) LoginManagerin login_view asetetaan Blueprintille (reactapi) tyhjäksi ja näin syntyvät 401-virhekeskeytykset käsitellään Blueprintin omalla 401-virhekäsittelijällä CORS:in vaatimat Headerit huomioon ottaen.  Huom. Tätä ratkaisua ei näyttäisi löytyvän verkosta ainakaan kovin helposti. Yksi ratkaisu voisi olla 

C) oman @login_required-dekoraattorin laatiminen.

Konfiguraatiossa kaikilta kutsuilta (= oletus, muut kuin GET-metodit) edellytetään joko lomakkeessa csrf_tokenia tai 
X-CSRFToken -Headeriä.

Testattu reactapin signin, logout ja haeProfiili.