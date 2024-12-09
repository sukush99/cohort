run-dev:
	uv run run.py

lint:
	ruff check --fix

format:
	ruff format .

build:
	docker build -f Dockerfile -t trades .

run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		trades