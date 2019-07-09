FROM python:3.7.4-slim-stretch

RUN apt-get update \
    && apt-get install -y --no-install-recommends libatlas-base-dev gfortran cmake build-essential git tk \
    && echo "deb http://httpredir.debian.org/debian jessie main contrib" > /etc/apt/sources.list \
    && echo "deb http://security.debian.org/ jessie/updates main contrib" >> /etc/apt/sources.list \
    && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
    && apt-get update \
    && apt-get install -y --no-install-recommends ttf-mscorefonts-installer \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Europe/Paris
ENV SET_CONTAINER_TIMEZONE=true

RUN mkdir /keywords
WORKDIR /keywords
COPY ./requirements.txt ./requirements.txt

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY ./CHANGELOG.md ./
COPY ./keyword_app ./keyword_app
ENV PORT_API=54321
ENV BIND_INTERFACE=0.0.0.0
ENV API_VERSION=1.0.0

EXPOSE 54321

RUN python3 -m spacy download fr_core_news_sm
RUN python3 -m spacy download es_core_news_sm
RUN python3 -m spacy download en_core_web_sm

RUN pip install textacy
RUN pip install ftfy
RUN python3 -m nltk.downloader punkt && python3 -m nltk.downloader stopwords

CMD python3 -m keyword_app.keywords_extraction
