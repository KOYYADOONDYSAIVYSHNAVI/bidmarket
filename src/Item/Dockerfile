FROM --platform=$BUILDPLATFORM python:3.12-alpine

ARG ITEM_FOLDER=/Item
COPY . $ITEM_FOLDER

RUN pip install --no-cache-dir -r /Item/requirements.txt

WORKDIR /

CMD ["python", "-m", "Item.app"]
