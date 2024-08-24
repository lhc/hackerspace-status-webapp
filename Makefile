# Nome da imagem Docker
IMAGE_NAME = hackersapce-status-webapp
CONTAINER_NAME = hackersapce-status-webapp

# Porta em que a aplicação irá rodar
PORT = 5000

# Construir a imagem Docker
build:
	docker build -t $(IMAGE_NAME) .

# Rodar o contêiner Docker
run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Parar o contêiner Docker
stop:
	docker stop $(CONTAINER_NAME)

# Remover o contêiner Docker
clean: stop
	docker rm $(CONTAINER_NAME)

# Ver logs do contêiner Docker
logs:
	docker logs -f $(CONTAINER_NAME)

# Publicar a imagem Docker no Docker Hub
publish:
	docker login
	docker tag $(IMAGE_NAME) your_dockerhub_username/$(IMAGE_NAME)
	docker push your_dockerhub_username/$(IMAGE_NAME)

.PHONY: build run stop clean logs publish
