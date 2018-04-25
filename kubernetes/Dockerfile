# Read from Ubuntu Base Image
FROM python:2.7
RUN mkdir -p /service
# Copy over all the files of interest
ADD app /service/app
ADD app.py /service/app.py
ADD config.py /service/config.py
ADD manage.py /service/manage.py
ADD requirements.txt /service/requirements.txt
ADD author_to_index.json /service/authors_to_index.json
ADD authors_to_books.json /service/authors_to_books.json
ADD book_to_index.json /service/book_to_index.json
ADD books.json /service/books.json
ADD word_to_index.json /service/word_to_index.json
ADD words.json /service/words.json

WORKDIR /service/
RUN pip install -r requirements.txt
CMD python -u app.py $APP_SETTINGS $DATABASE_URL
