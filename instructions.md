### for setting up virtual environment:
- install virtualenv
- virtualenv venv
- source venv/bin/activate

### for setting up db:
- open python shell
- from app import db, app
- app.app_context().push()
- db.create_all()

### install jinja2 snippet kit

### install gunicorn for deployment (helps in running flask app on server)

### pip freeze > requirements.txt