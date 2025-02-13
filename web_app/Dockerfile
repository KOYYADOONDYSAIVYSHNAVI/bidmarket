FROM --platform=$BUILDPLATFORM python:3.12-alpine

ARG WEBAPP_PATH=/webapp
COPY ./backend $WEBAPP_PATH

RUN pip install --no-cache-dir -r $WEBAPP_PATH/requirements.txt

WORKDIR /

CMD ["python", "-m", "webapp.app"]
