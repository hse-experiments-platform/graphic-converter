from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import matplotlib.pyplot as plt
from minio import Minio
from minio.error import S3Error
import csv
from io import BytesIO, StringIO
import uuid
import os

from getPoints import getGraphicPoints

class Scale(BaseModel):
    minX: float
    minY: float
    maxX: float
    maxY: float

class Request(BaseModel):
    imageUrl: str
    scale: Scale

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

minio_client = Minio(
    os.getenv('MINIO_URL'),
    access_key=os.getenv('ACCESS_KEY'),
    secret_key=os.getenv('SECRET_KEY'),
    secure=False
)

def upload_file_to_minio(file_bytes, file_name):
    try:
        minio_url = os.getenv('MINIO_URL')
        bucket_name = os.getenv('BUCKET_NAME')
        file_bytes.seek(0)
        minio_client.put_object(bucket_name, file_name, file_bytes, length=file_bytes.getbuffer().nbytes)
        return f"http://{minio_url}/{bucket_name}/{file_name}"
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-image/")
async def process_image(request: Request):
    scale = request.scale
    result = getGraphicPoints(request.imageUrl, scale.minX, scale.minY, scale.maxX, scale.maxY)

    csv_file = StringIO()
    csv_file_writer = csv.writer(csv_file)
    csv_file_writer.writerow(['x', 'y'])
    for pair in result:
        csv_file_writer.writerow([str(pair[0]), str(pair[1])])
    csv_file.seek(0)
    csv_buffer = BytesIO(csv_file.getvalue().encode())
    csv_file_name = f"output-{uuid.uuid4()}.csv"
    csv_url = upload_file_to_minio(csv_buffer, csv_file_name)


    fig, ax = plt.subplots()
    x, y = list(zip(*result))
    ax.plot(x, y)
    plt.grid(True)
    plt.xlabel('2О, degrees')
    plt.ylabel('Intensity (impl/sec)')
    if scale:
        ax.set_xlim([scale.minX, scale.maxX])
        ax.set_ylim([scale.minY, scale.maxY])
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_file_name = f"plot-{uuid.uuid4()}.png"
    img_url = upload_file_to_minio(img_buf, img_file_name)

    return {"csvUrl": csv_url, "graphicUrl": img_url}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5003)