.PHONY: build up

IMAGE_NAME = djangoeasydata
TAG = latest

build:
	docker build . -t $(IMAGE_NAME):$(TAG)

up:
	docker compose up -d
	docker compose logs -f