IMG ?= controller:latest
dev:
	skaffold dev

.PHONY: fmt
fmt: ## Run go fmt against code.
	go fmt ./...

.PHONY: vet
vet: ## Run go vet against code.
	go vet ./...

.PHONY: docker-build
docker-build:
	docker buildx build --build-arg GOPROXY=direct --load -t  ${IMG} .

.PHONY: docker-push
docker-push:
	docker push ${IMG}

deploy-dev:
	echo "IMAGE_REPO_WITH_TAG=${IMG}" > ./_infra/kustomize/overlays/dev/.env
	kustomize build ./_infra/kustomize/overlays/dev | kubectl apply -f -
