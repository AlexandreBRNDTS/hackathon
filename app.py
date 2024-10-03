from fastapi import FastAPI, File, UploadFile
import csv
#import obspy
from obspy import read

app = FastAPI()

@app.get('/')
async def root():
    return {"Objevtive hackathon":"API receive a file", "data":0}

@app.post("/uploadAndRead-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        contents = await file.read()
        
        with open(file.filename, 'r') as f:
            csv_reader = csv.DictReader(f)
            data = [row for row in csv_reader]
            return data 


        return{"message": "upload sucess"}
    else:
        return{"message": "Only csv files"}



@app.post("/uploadAndRead-mseed/")
async def upload_mseed(file: UploadFile = File(...)):
    if file.filename.endswith('.mseed'):
        contents = await file.read()
        
        with open(file.filename, 'wb') as f:
            f.write(contents)

        # Read the MiniSEED file
        try:
            st = read(file.filename)
            # Convert to a list of dictionaries for a simple representation
            data = []
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
