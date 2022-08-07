SHELL := /bin/bash

COMMIT := $(shell git describe --always)
USERNAME := $(shell whoami)

IMAGE ?= $(shell echo $(shell basename $(PWD)) | tr '[A-Z]' '[a-z]')
REGISTRY ?= $(USERNAME)
VERSION ?= $(COMMIT)

CONTAINER := $(USERNAME)-$(IMAGE)-$(COMMIT)
REPOSITORY := $(REGISTRY)/$(IMAGE)


kill:
	@set -euo pipefail; \
	CONTAINER_ID=$$(docker ps -q -a -f "name=$(CONTAINER)"); \
	if [[ -n $$CONTAINER_ID ]]; then \
		docker stop $$CONTAINER_ID; \
		docker rm $$CONTAINER_ID; \
	fi;

clean: kill
	@set -euo pipefail; \
	IMAGE_ID=$$(docker images -q "$(REPOSITORY):$(VERSION)"); \
	if [[ -n $$IMAGE_ID ]]; then \
		docker rmi -f $$IMAGE_ID; \
	fi;

build: kill
	docker build --no-cache -t $(REPOSITORY):$(VERSION) .

run:
	docker run -itd --name $(CONTAINER) $(REPOSITORY):$(VERSION) /bin/bash

exec:
	docker exec -it $(CONTAINER) /bin/bash

dev: build run exec

push:
	@echo "Try to push $(REPOSITORY):$(VERSION) to $(REGISTRY)"
	docker push $(REPOSITORY):$(VERSION)
