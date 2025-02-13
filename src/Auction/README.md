# Deployment
```
docker compose up -d
```
Default port is 50010, you can change it in `docker-compose.yml`

# Local Development
- Install dependencies: `pip install -r requirements.txt`
- Run shell script `Auction/serve.sh` from `bidmarket/src`

# API Reference
See `Auction/rpc/service.proto`

An grpc client example is available in `Auction/grpc/example_client.py`
