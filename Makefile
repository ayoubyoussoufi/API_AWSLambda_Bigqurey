# Define variables
IMAGE_NAME := test_data
CONTAINER_NAME := test_data_container
SCRIPT_NAME := api_test.py

# Default target
.PHONY: all
all: build run

# Target to build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Target to run the Python script inside a Docker container
.PHONY: run
run:
	docker run --rm $(IMAGE_NAME)

# Target to clean up temporary files and containers
.PHONY: clean
clean:
	# Remove the Docker container
	-docker rm -f $(CONTAINER_NAME)
	# Remove the Docker image
	-docker rmi -f $(IMAGE_NAME)

# Help target to display available targets and their descriptions
.PHONY: help
help:
	@echo "Available targets:"
	@echo "make build   : Build the Docker image"
	@echo "make run     : Run the Python script inside a Docker container"
	@echo "make clean   : Clean up temporary files and containers"
	@echo "make help    : Display this help message"
