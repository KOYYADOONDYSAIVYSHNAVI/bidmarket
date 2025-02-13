#!/bin/bash

# Generate the gRPC code
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Auction/rpc/service.proto

# Run RabbitMQ
rabbitmq-server start -detached

# Run Celery
celery -A Auction.task_scheduler.tasks worker -f celery.log --loglevel=INFO --detach

# Run service
python -m Auction.rpc.service
