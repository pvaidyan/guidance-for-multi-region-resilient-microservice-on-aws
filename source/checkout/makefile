IMG ?= checkout:latest

.PHONY: docker-build
docker-build:
	docker buildx build --platform linux/amd64 --load -t  ${IMG} .

.PHONY: docker-push
docker-push:
	docker push ${IMG}


deploy-dev:
	 echo "IMAGE_REPO_WITH_TAG=${IMG}" > ./_infra/kustomize/overlays/dev/.env
	 kustomize build ./_infra/kustomize/overlays/dev


deploy-param:
	 echo "IMAGE_REPO_WITH_TAG=${IMG}" > ./_infra/kustomize/overlays/dev/.env
	 kustomize build ./_infra/kustomize/overlays/param
