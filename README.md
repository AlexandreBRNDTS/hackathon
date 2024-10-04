# FastAPI MSEED Uploader

This FastAPI-based web application processes seismic data from MiniSEED files and generates seismic waveform charts

## Features

- Seismic Data Processing: Upload MiniSEED files to visualize seismic waveforms for three channels (Z, N, E).
- Phase Detection: Detect P and S seismic phases using the PhaseNet API.
- Plot Generation: Generate PNG images of seismic waveforms with phase information.

## Requirements

- Python 3.9 or higher (if running locally)
- Docker (for running the application in a container)
- obspy (To read .mseed)

## Installation

- Python (if running locally)
- Docker (for running the application in a container)
- obspy (To read .mseed)

### Run the application

- docker-compose up

## Input

- MiniSEED file (example.mseed)

## Output

- PNG image containing a seismic waveform chart with detected phases.
