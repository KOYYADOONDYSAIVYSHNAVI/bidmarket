from __future__ import absolute_import
from celery import Celery
from Auction.consts.consts import RABBITMQ_URI

app = Celery('auction_celery',
             broker=RABBITMQ_URI,
             backend='rpc://',
             include=['Auction.task_scheduler.tasks'])