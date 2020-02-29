SHELL := /bin/bash

# DO NOT CHANGE VERSION NUMBER MANUALLY
VERSION=0.0.1
VERSION_MAJOR:=$(shell echo $(VERSION) | cut -d'.' -f1)
VERSION_MINOR:=$(shell echo $(VERSION) | cut -d'.' -f2)
VERSION_PATCH:=$(shell echo $(VERSION) | cut -d'.' -f3)


# configuration
# -------------

SLUG=hcli
NAME=hCLI


# project setup
# -------------

# setup project for development
setup:
    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt


# code tasks
# ----------

# run all automatic code tasks (formatting, linting)

# format files with black, isort and trim

# lint python code with pycodestyle, pyflakes, mccabe, radon, eradicate and mypy

# run static type analysis with mypy (strict)

# bump project version
# config file: .bumpversion.cfg
# usage:
# $ make bump-version type=major|minor|patch (default is patch)
type?=patch
bump-version:
	bumpversion $(type)


# documentation
# ---------

# docker
# ------

# build docker image
docker-build:
	docker build \
		-t $(SLUG):latest \
		-t $(SLUG):$(VERSION_MAJOR) \
		-t $(SLUG):$(VERSION_MAJOR).$(VERSION_MINOR) \
		-t $(SLUG):$(VERSION) \
		.

# start blockchain with docker
docker-start:
	docker run -d \
		--name $(SLUG) \
		$(SLUG):$(VERSION)

# stop and remove the container that's currently running
docker-stop:
	-docker rm -f $(SLUG)

# stop the container that's currently running
docker-pause:
	docker stop $(SLUG)

# resume the container that's currently paused
docker-resume:
	docker start $(SLUG)


# makefile help and guide
# -----------------------

# print makefile help
define help_text
Makefile for $(NAME) v$(VERSION)

Usage: make [COMMAND] [OPTIONS]
Example: make example-command example-option=value


Commands
========

Project setup
  setup               Setup project for development

Code tasks
  checklist           Run all automatic code tasks (formatting, linting, testing...)
  format              Format files with black, isort and trim
  lint                Lint python code with pycodestyle, pyflakes, mccabe, radon, eradicate and mypy
  bump-version        Bump project version
    - type=major|minor|patch (default: patch)
  test-unit           Run unit tests
  test-integration    Run integration tests
  test                Run all tests
  check-types         Run static type analysis with mypy (strict)

Documentation

Docker
  docker-build        Build docker image
  docker-start        Start blockchain with docker
  docker-stop         Stop and remove the container that's currently running
  docker-pause        Stop the container that's currently running
  docker-resume       Resume the blockchain that's currently paused
  docker-refresh      Build image and start blockchain with docker

Help
  help                Show help with full command list
  guide               Show usage guide
endef
export help_text
# show help with full command list
help:
	@echo "$$help_text"

define guide_text
Makefile for $(NAME) v$(VERSION)


Usage guide
===========

Basic development tasks
-----------------------

- Setup the project when it's freshly cloned:
$ make setup
# activate the virtualenv (or configure it on your IDE)
$ source .venv/bin/activate


Code quality
------------

- Run formatting, linting and testing tasks:
$ make checklist

- Format the project files:
$ make format

- Lint the python code:
$ make lint

- Publish a new version:
$ make bump-version type=major|minor|patch

- Run all tests:
$ make test

- Run unit tests:
$ make test-unit

- Run integration tests:
$ make test-integration

- Analyze types with mypy (strict):
$ make check-types

Documentation
-------------



Execution
---------



Docker
------

- Build the docker image:
$ make docker-build

- Start the blockchain with docker:
$ make docker-start rpc_port=<port> rest_port=<port>

- Stop the blockchain container:
$ make docker-stop

- Rebuild and redeploy the blockchain image with the latest changes:
$ make docker-refresh rpc_port=<port> rest_port=<port>

- Pause and resume the currently running blockchain container:
$ make docker-pause
$ make docker-resume
endef
export guide_text
# show usage guide
guide:
	@echo "$$guide_text"
