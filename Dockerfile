FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python src/manage.py migrate && \
    python src/manage.py runserver 0.0.0.0:8000