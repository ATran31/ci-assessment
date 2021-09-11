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


def _get_metadata():
    file = s3.get_object(Bucket=target_bucket, Key="metadata.txt")
    contents = file["Body"].iter_lines()
    metadata = dict()
    attributes = next(contents).decode("utf-8").split("\t")
    for remaining in contents:
        vals = remaining.decode("utf-8").split("\t")
        key = vals[0]
        metadata[key] = dict()
        for idx, val in enumerate(attributes):
            if idx == 0:
                metadata[key]["imageName"] = vals[0]
            else:
                metadata[key][val] = vals[idx]
    return metadata


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/files")
def get_files(start_dt: Optional[str] = None, end_dt: Optional[str] = None):
    """
    List all files.
    """
    try:
        resp = [v for v in _get_metadata().values()]
        if start_dt and end_dt:
            return list(
                map(
                    lambda x: x["imageName"],
                    filter(
                        lambda x: x["dateTime"] <= end_dt and x["dateTime"] >= start_dt,
                        resp,
                    ),
                )
            )
        elif start_dt:
            return list(
                map(
                    lambda x: x["imageName"],
                    filter(lambda x: x["dateTime"] >= start_dt, resp),
                )
            )
        elif end_dt:
            return list(
                map(
                    lambda x: x["imageName"],
                    filter(lambda x: x["dateTime"] <= end_dt, resp),
                )
            )
        else:
            return [file["imageName"] for file in resp]
    except ClientError as ce:
        logging.error(ce)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": f"{ce.response['Error']['Code']}",
                "message": f"{ce.response['Error']['Message']}",
            },
        )


@app.get("/api/v1/file/{file_id}")
def get_file(file_id: str):
    """
    Get metadata for a file with file_id.
    """
    try:
        resp = _get_metadata()
        return resp[file_id]
    except ClientError as ce:
        logging.error(ce)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": f"{ce.response['Error']['Code']}",
                "message": f"{ce.response['Error']['Message']}",
            },
        )


@app.get("/api/v1/download")
def download_all():
    """
    Downloads a zip file of all files.
    """
    try:
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zipper:
            all_files = s3.list_objects_v2(Bucket=target_bucket)
            for s3Key in list(map(lambda x: x["Key"], all_files["Contents"])):
                infile_object = s3.get_object(Bucket=target_bucket, Key=s3Key)
                infile_content = infile_object["Body"].read()
                zipper.writestr(s3Key, infile_content)

        return Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment;filename=All-Files.zip"},
        )
    except ClientError as ce:
        logging.error(ce)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": f"{ce.response['Error']['Code']}",
                "message": f"{ce.response['Error']['Message']}",
            },
        )


@app.get("/api/v1/download/{file_id}")
def download_file(file_id: str):
    """
    Download a specific file with file_id.
    """
    try:
        file = s3.get_object(Bucket=target_bucket, Key=file_id)
        return Response(
            content=file["Body"].read(),
            media_type=file["ContentType"],
            headers={"Content-Disposition": f"attachment;filename={file_id}"},
        )
    except ClientError as ce:
        logging.error(ce)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": f"{ce.response['Error']['Code']}",
                "message": f"{ce.response['Error']['Message']}",
            },
        )
