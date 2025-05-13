FROM python:3.13

WORKDIR /app

RUN pip install urllib3==1.26.18 \
    && pip install typing-extensions --upgrade \
    && pip install poetry

RUN cd /usr/local/bin
RUN ln -s /opt/poetry/bin/poetry
RUN poetry config virtualenvs.in-project true