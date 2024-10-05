import io
import requests
import traceback
import numpy as np
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile
from obspy import read
from obspy.clients.fdsn import Client
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from utils import generate_seismic_chart

app = FastAPI()

PHASENET_API_URL = "https://ai4eps-eqnet.hf.space"

LAST_TRACING = None


def save_last_tracing(stream, phase_data):
    client = Client("IRIS")
    network = stream[0].stats["network"]
    station = stream[0].stats["station"]

    inventory = client.get_stations(network=network, station=station, level="station")
    latitude = inventory[0][0].latitude
    longitude = inventory[0][0].longitude

    for phase in phase_data:
        phase.pop("station_id")

    global LAST_TRACING
    LAST_TRACING = {
        "network": network,
        "station": station,
        "starttime": stream[0].stats["starttime"].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3],
        "latitude": latitude,
        "longitude": longitude,
        "phase_data": phase_data
    }

@app.post("/plot/")
async def predict(file: UploadFile = File(...)):
    if file.filename.endswith('.mseed'):
        try:
            contents = await file.read()
            file_like_object = io.BytesIO(contents)
            stream = read(file_like_object)
            stream = stream.sort()
            if len(stream) != 3:
                return {"message": "Invalid number of traces in MiniSEED file"}

            data = []
            for trace in stream:
                data.append(trace.data)
            data = np.array(data).T
            data_id = stream[0].get_id()[:-1]
            timestamp = stream[0].stats.starttime.datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

            req = {
                "id": [data_id.split('.')],
                "timestamp": [timestamp],
                "vec": [data.tolist()]
            }
            resp = requests.post(f'{PHASENET_API_URL}/predict', json=req)

            if resp.status_code != 200:
                return {"message": "Error predicting phase", "error": resp.status_code}

            phase_data = resp.json()

            save_last_tracing(stream, phase_data)

            fig = generate_seismic_chart(stream, phase_data)

            # Save the chart to a bytes buffer
            with NamedTemporaryFile("wb+", delete=False) as f:
                fig.savefig(f, format='png')
                f.flush()

                # Close the matplotlib figure to free up memory
                plt.close(fig)

                # Return the chart as a file response
                return FileResponse(f.name, media_type="image/png", filename="seismic_chart.png")
        except Exception as e:
            traceback.print_exc()
            return {"message": "Error reading MiniSEED file", "error": str(e)}
    else:
        return {"message": "Only MiniSEED files are allowed"}
    

@app.get("/data/")
async def data():
    return LAST_TRACING
    