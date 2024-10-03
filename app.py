from fastapi import FastAPI, File, UploadFile
from obspy import read

app = FastAPI()

data = []

@app.get('/')
async def root():
    return {"Objevtive hackathon":"API receive a file", "data":0}


@app.post("/uploadAndStore-mseed/")
async def upload_and_store_mseed(file: UploadFile = File(...)):
    if file.filename.endswith('.mseed'):
        contents = await file.read()
        
        with open(file.filename, 'wb') as f:
            f.write(contents)

        try:
            st = read(file.filename)

            for tr in st:
                data.append({
                    "network": tr.stats.network,
                    "station": tr.stats.station,
                    "location": tr.stats.location,
                    "channel": tr.stats.channel,
                    "starttime": tr.stats.starttime.isoformat(),
                    "endtime": tr.stats.endtime.isoformat(),
                    "sampling_rate": tr.stats.sampling_rate,
                    "data": tr.data.tolist()
                })

            return {"message": "Upload successful"}
        except Exception as e:
            return {"message": "Error reading MiniSEED file", "error": str(e)}
    else:
        return {"message": "Only MiniSEED files are allowed"}


@app.get("/showData/")
async def show_data():
    if data:
        return {"message": "Data retrieved successfully", "data": data}
    else:
        return {"message": "No data available"}


@app.post("/uploadAndRead-mseed/")
async def upload_mseed(file: UploadFile = File(...)):
    if file.filename.endswith('.mseed'):
        contents = await file.read()
        
        with open(file.filename, 'wb') as f:
            f.write(contents)

        try:
            st = read(file.filename)

            for tr in st:
                data.append({
                    "network": tr.stats.network,
                    "station": tr.stats.station,
                    "location": tr.stats.location,
                    "channel": tr.stats.channel,
                    "starttime": tr.stats.starttime.isoformat(),
                    "endtime": tr.stats.endtime.isoformat(),
                    "sampling_rate": tr.stats.sampling_rate,
                    "data": tr.data.tolist()
                })

            return {"message": "Upload successful", "data": data}
        except Exception as e:
            return {"message": "Error reading MiniSEED file", "error": str(e)}
    else:
        return {"message": "Only MiniSEED files are allowed"}
