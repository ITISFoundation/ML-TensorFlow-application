SHELL = /bin/sh
.DEFAULT_GOAL := help

export IMAGE_TRAIN=ml-tf-train
export IMAGE_PREDICT=ml-tf-predict
export IMAGE_EVALUATE=ml-tf-evaluate

export TAG_TRAIN=1.0.0
export TAG_PREDICT=1.0.0
export TAG_EVALUATE=1.0.0

#export COMPOSE_INPUT_DIR_TRAIN  := ml_tf_train/input
#export COMPOSE_INPUT_DIR_PREDICT := ml_tf_predict/input
#export COMPOSE_INPUT_DIR_EVALUATE := ml_tf_evaluate/input

define _bumpversion
	# upgrades as $(subst $(1),,$@) version, commits and tags
	@docker run -it --rm -v $(PWD):/ml-lab \
		-u $(shell id -u):$(shell id -g) \
		itisfoundation/ci-service-integration-library:v1.0.1-dev-32 \
		sh -c "cd /ml-lab && bump2version --verbose --list --config-file $(1) $(subst $(2),,$@)"
endef

.PHONY: version-train-patch version-train-minor version-train-major
version-train-patch version-train-minor version-train-major: .bumpversion-train.cfg ## increases ml-tf-train service's version
	@make compose-spec
	@$(call _bumpversion,$<,version-train-)
	@make compose-spec

.PHONY: version-predict-patch version-predict-minor version-predict-major
version-predict-patch version-predict-minor version-predict-major: .bumpversion-predict.cfg ## increases ml-tf-predict service's version
	@make compose-spec
	@$(call _bumpversion,$<,version-predict-)
	@make compose-spec

.PHONY: version-evaluate-patch version-evaluate-minor version-evaluate-major
version-evaluate-patch version-evaluate-minor version-evaluate-major: .bumpversion-evaluate.cfg ## increases ml-tf-evaluate service's version
	@make compose-spec
	@$(call _bumpversion,$<,version-evaluate-)
	@make compose-spec

.PHONY: compose-spec
compose-spec: ## runs ooil to assemble the docker-compose.yml file
	@docker run -it --rm -v $(PWD):/ml-lab \
		-u $(shell id -u):$(shell id -g) \
		itisfoundation/ci-service-integration-library:v1.0.1-dev-32 \
		sh -c "cd /ml-lab && ooil compose"

.PHONY: devenv
devenv: ## creates python virtualenv
	python3 -m venv .$@
	# upgrading package managers
	.$@/bin/pip3 install --upgrade \
		pip \
		wheel \
		setuptools
	# tooling
	.$@/bin/pip3 install \
		pip-tools

.PHONY: build
build: compose-spec ## build docker images
	docker-compose build

.PHONY: run-train-local
run-train-local: ## runs train image with local configuration
	IMAGE_TO_RUN=${IMAGE_TRAIN} \
	TAG_TO_RUN=${TAG_TRAIN} \
	docker-compose --file docker-compose-local.yml up

.PHONY: run-predict-local
run-predict-local: ## runs predict image with local configuration
	IMAGE_TO_RUN=${IMAGE_PREDICT} \
	TAG_TO_RUN=${TAG_PREDICT} \
	docker-compose --file docker-compose-local.yml up

.PHONY: run-evaluate-local
run-evaluate-local: ## runs evaluate image with local configuration
	IMAGE_TO_RUN=${IMAGE_EVALUATE} \
	TAG_TO_RUN=${TAG_EVALUATE} \
	docker-compose --file docker-compose-local.yml up


.PHONY: shell-train # Doesn't work for now
shell-train:  ## Starts a shell for train service instead of running the container. Useful for development.
	# starting service and go in...
	$(call _docker_compose_cli,run --service-ports $(IMAGE_TRAIN) /bin/sh)


publish-local:  ## push to local throw away registry to test integration
	@docker tag simcore/services/comp/${IMAGE_TRAIN}:${TAG_TRAIN} registry:5000/simcore/services/comp/${IMAGE_TRAIN}:${TAG_TRAIN}
	@docker tag simcore/services/comp/${IMAGE_PREDICT}:${TAG_PREDICT} registry:5000/simcore/services/comp/${IMAGE_PREDICT}:${TAG_PREDICT}
	@docker tag simcore/services/comp/${IMAGE_EVALUATE}:${TAG_EVALUATE} registry:5000/simcore/services/comp/${IMAGE_EVALUATE}:${TAG_EVALUATE}
	@docker push registry:5000/simcore/services/comp/${IMAGE_TRAIN}:${TAG_TRAIN}
	@docker push registry:5000/simcore/services/comp/${IMAGE_PREDICT}:${TAG_PREDICT}
	@docker push registry:5000/simcore/services/comp/${IMAGE_EVALUATE}:${TAG_EVALUATE}

.PHONY: help
help: ## this colorful help
	@echo "Recipes for '$(notdir $(CURDIR))':"
	@echo ""
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
