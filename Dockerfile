FROM python:3.7.7-stretch AS BASE

RUN apt-get update \
    && apt-get --assume-yes --no-install-recommends install \
        build-essential \
        curl \
        git \
        jq \
        libgomp1 \
        vim

WORKDIR /app

# upgrade pip version
RUN pip install --no-cache-dir --upgrade pip


RUN pip3 install rasa==2.8.2 && pip3 install --no-cache spacy==3.1.0 && python3 -m spacy download ru_core_news_md  && pip3 install textdistance==4.2.1 && pip3 install nltk && pip3 install Shapely       

ADD config.yml config.yml
ADD domain.yml domain.yml
ADD credentials.yml credentials.yml
ADD endpoints.yml endpoints.yml
ADD custom_rest.py custom_rest.py
ADD custom_telegram.py custom_telegram.py
ADD custom_wati.py custom_wati.py
ADD krg_address.db krg_address.db
ADD users_db.py users_db.py
ADD orders_db.py orders_db.py
ADD yandex_helper.py yandex_helper.py
ADD yandex_stt.py yandex_stt.py
ADD user_audio.ogg user_audio.ogg
ADD wati.py wati.py
ADD telegram_api.py telegram_api.py
ADD callbot_api.py callbot_api.py
ADD rasa_api.py rasa_api.py
ADD telegram_admin_api.py telegram_admin_api.py
ADD AppSingleton.py AppSingleton.py
