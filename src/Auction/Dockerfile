FROM python:3.12-slim

ARG AUCTION_FOLDER=/Auction

# Copy files to the container
COPY . $AUCTION_FOLDER

# Install dependencies
RUN apt update && \
  apt install -y --no-install-recommends gcc python3-dev libssl-dev rabbitmq-server dos2unix && \
  apt remove -y gcc python3-dev libssl-dev && \
  apt autoremove -y

# Install Python dependencies
RUN pip install --no-cache-dir -r $AUCTION_FOLDER/requirements.txt

# Convert serve.sh to Unix line endings and ensure executable
RUN dos2unix $AUCTION_FOLDER/serve.sh
RUN chmod +x $AUCTION_FOLDER/serve.sh

# Debug: Verify file exists
RUN ls -l $AUCTION_FOLDER
RUN cat $AUCTION_FOLDER/serve.sh

WORKDIR /

ENTRYPOINT ["/Auction/serve.sh"]
