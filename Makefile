# Makefile
SHELL := /bin/bash

DOCKER_IMAGE ?= iei-builder
IN_DOCKER    ?= $(wildcard /.dockerenv)

.PHONY: all clean build-image check-docker

ifeq ($(strip $(IN_DOCKER)),)

define check_docker
	@if ! command -v docker >/dev/null 2>&1; then \
		echo ""; \
		echo "=================================================================="; \
		echo "Error: Docker is not installed on this system."; \
		echo "To build course slides and materials, please install Docker:"; \
		echo "  - macOS / Windows: https://docs.docker.com/desktop/"; \
		echo "  - Linux: https://docs.docker.com/engine/install/"; \
		echo "=================================================================="; \
		echo ""; \
		exit 1; \
	fi
	@if ! docker info >/dev/null 2>&1; then \
		echo ""; \
		echo "=================================================================="; \
		echo "Error: Docker daemon is not running."; \
		echo "Please start Docker Desktop (or the docker service) and try again."; \
		echo "=================================================================="; \
		echo ""; \
		exit 1; \
	fi
endef

define ensure_image
	@if ! docker image inspect $(DOCKER_IMAGE) >/dev/null 2>&1; then \
		echo "==> Builder image '$(DOCKER_IMAGE)' not found. Building from Dockerfile..."; \
		docker build -t $(DOCKER_IMAGE) -f Dockerfile . || exit 1; \
	fi
endef

define run_docker
	$(call check_docker)
	$(call ensure_image)
	@docker run --rm \
		-u "$$(id -u):$$(id -g)" \
		-e HOME=/tmp \
		-e IN_DOCKER=1 \
		-v "$$(PWD):/data" \
		-w /data \
		$(DOCKER_IMAGE) make $(1)
endef

all clean:
	$(call run_docker,$@)

class_%:
	$(call run_docker,$@)

project%:
	$(call run_docker,$@)

build-image:
	$(call check_docker)
	@echo "==> Building Docker builder image ($(DOCKER_IMAGE))..."
	@docker build -t $(DOCKER_IMAGE) -f Dockerfile .

check-docker:
	$(call check_docker)
	@echo "Docker is installed and running."

else

# -------------------------------------------------------------------------
# Recipes executed inside the Docker container
# -------------------------------------------------------------------------

all clean:
	@total=$$(find . -name ".venv" -prune -o -mindepth 2 -name "Makefile" -print | wc -l); \
	current=0; \
	width=40; \
	echo "Build started at $$(date)" > build.log; \
	tput civis 2>/dev/null || true; \
	find . -name ".venv" -prune -o -mindepth 2 -name "Makefile" -print0 | while IFS= read -r -d '' mkfile; do \
		[ -z "$$mkfile" ] && continue; \
		dir=$$(dirname "$$mkfile"); \
		current=$$((current + 1)); \
		percent=$$((current * 100 / total)); \
		filled=$$((percent * width / 100)); \
		empty=$$((width - filled)); \
		bar_filled=$$(printf "%$${filled}s" | tr " " "#"); \
		bar_empty=$$(printf "%$${empty}s" | tr " " " "); \
		printf "\r%3d%%|%s%s| %d/%d [%s]\033[K" "$$percent" "$$bar_filled" "$$bar_empty" "$$current" "$$total" "$$dir"; \
		if ! $(MAKE) -s -C "$$dir" $@; then \
			printf "\nError processing %s. See build.log\n" "$$dir"; \
		fi; \
	done; \
	echo ""; \
	tput cnorm 2>/dev/null || true; \
	echo "Done."

# Individual class builds (e.g.: make class_00, make class_01)
class_%:
	@if [ ! -d "classes/$@" ]; then \
		echo "Error: classes/$@ does not exist."; \
		exit 1; \
	fi
	@find classes/$@ -name "Makefile" -print0 | while IFS= read -r -d '' mkfile; do \
		dir=$$(dirname "$$mkfile"); \
		echo "==> Building $$dir..."; \
		$(MAKE) -C "$$dir" all; \
	done

# Individual project builds (e.g.: make project01 or make project_01)
project%:
	@name="$@"; \
	clean_name=$$(echo "$$name" | tr -d '_'); \
	pdir="evaluation/$$clean_name"; \
	if [ ! -d "$$pdir" ]; then \
		echo "Error: $$pdir does not exist."; \
		exit 1; \
	fi; \
	find "$$pdir" -name "Makefile" -print0 | while IFS= read -r -d '' mkfile; do \
		dir=$$(dirname "$$mkfile"); \
		echo "==> Building $$dir..."; \
		$(MAKE) -C "$$dir" all; \
	done

endif