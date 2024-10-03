# FastAPI CSV Uploader

This is a FastAPI application that allows users to upload .mseed files and read their contents.

## Features

- Upload .mseed files via a POST endpoint.
- Read and return the contents of the uploaded .mseed file as JSON.
- Basic error handling for unsupported file types.

## Requirements

- Python 3.9 or higher (if running locally)
- Docker (for running the application in a container)
- obspy (To read .mseed)

### Run the application

- docker-compose up
