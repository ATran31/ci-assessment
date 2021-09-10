from fastapi import FastAPI
import boto3
import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

s3 = boto3.client("s3", region_name=config["DEFAULT"]["AWS_REGION"])

app = FastAPI()


@app.get("/files")
async def get_files():
    """
    List all files.
    """
    pass


@app.get("/file/{file_id}")
async def get_file(file_id: str):
    """
    Get metadata for a file with file_id.
    """
    pass


@app.get("/download")
async def download_all():
    """
    Downloads a zip file of all files.
    """
    pass


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Download a specific file with file_id.
    """
    pass
