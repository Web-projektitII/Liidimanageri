import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
# Tuo terminaaliin db init, db migrate ja db upgrade-komennot
# Kerran flask db init, sitten flask db migrate -m "kuvaus" ja flask db upgrade

# with app.app_context():
    # Tätä ei tarvita, jos tietokanta on päivitetty terminaalissa
    # db.create_all()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    # app.run(app.run(host='0.0.0.0', port=5000, debug=True))
    app.run(debug=True)

# Suoritus VSC:n Run-valikosta miel. virtuaaliympäristössä tai 
# komentorivillä:
#   Python liidimanageri.py
# tai: 
#   set FLASK_APP=liidimanageri.py 
#   python -m flask run
