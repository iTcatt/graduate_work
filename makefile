build:
	docker build -t vizbuilder .

run:
	docker run -p 8000:8000 vizbuilder
