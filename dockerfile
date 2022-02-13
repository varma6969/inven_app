FROM ubuntu

RUN apt-get update
RUN apt install -y python3-pip
RUN pip install virtualenv
RUN virtualenv venv
RUN /bin/bash -c "source venv/bin/activate"
RUN pip install bcrypt
RUN pip install cffi
RUN pip install click
RUN pip install dnspython email-validator Flask
RUN pip install Flask-Admin Flask-Bcrypt Flask-Login Flask-SQLAlchemy Flask-WTF greenlet idna itsdangerous Jinja2 MarkupSafe pycparser setuptools six SQLAlchemy Werkzeug WTForms xlwt
COPY inventory_app /opt/inventory_app

ENTRYPOINT FLASK_APP=/opt/inventory_app/website/run.py flask run --host=0.0.0.0 
