docker build --tag nlmingestor -f Dockerfile .
docker run --read-only -v ./tmp:/tmp nlmingestor
