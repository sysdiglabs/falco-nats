DOCKER_ORG := sysdiglabs
IMAGE := $(if $(HUB),$(HUB)/)$(DOCKER_ORG)/falco-nats


all: linux image

linux:
	# Compile statically linked binary for linux.
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s" -o nats-pub nats-pub.go

image:
	docker build -t "$(IMAGE):latest" .

push:
	docker push "$(IMAGE):latest"
	