from fastapi import FastAPI, File, UploadFile
import csv

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

