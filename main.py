from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import boto3
from botocore.exceptions import ClientError
import os
import configparser
import logging
import io
import zipfile
from typing import Optional

config = configparser.ConfigParser()
config.read("config.ini")

aws_region = config["DEFAULT"]["AWS_REGION"]
target_bucket = config["DEFAULT"]["BUCKET_NAME"]

s3 = boto3.client("s3", region_name=aws_region)

app = FastAPI()

app.mount(
    "/_next/static", StaticFiles(directory="ui/ceres-ui/.next/static"), name="static"
)

templates = Jinja2Templates(directory="ui/ceres-ui/.next/serverless/pages")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/files")
def get_files(start_dt: Optional[str] = None, end_dt: Optional[str] = None):
    """
    List all files.
    """
    pass


@app.get("/api/v1/file/{file_id}")
def get_file(file_id: str):
    """
    Get metadata for a file with file_id.
    """
    pass


@app.get("/api/v1/download")
def download_all():
    """
    Downloads a zip file of all files.
    """
    pass


@app.get("/api/v1/download/{file_id}")
def download_file(file_id: str):
    """
    Download a specific file with file_id.
    """
    pass
