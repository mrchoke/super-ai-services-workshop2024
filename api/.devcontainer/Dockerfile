FROM python:3.12-slim

ENV TZ=Asia/Bangkok

ENV MULTIDICT_NO_EXTENSIONS=1
ENV YARL_NO_EXTENSIONS=1
ENV VIRTUAL_ENV /usr/local

COPY .devcontainer/requirements.txt /requirements.txt
RUN pip install --no-cache-dir uv \
  && uv pip install --no-cache -r /requirements.txt

COPY .devcontainer/start.sh /start.sh
RUN chmod +x /start.sh

COPY .devcontainer/hypercorn_conf.py /hypercorn_conf.py

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD ./ /app

WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["/start.sh"]
