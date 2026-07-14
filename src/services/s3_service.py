import os
from typing import List, Tuple

import boto3
from botocore.exceptions import ClientError


class S3Service:
    def __init__(self):
        self.bucket = os.getenv("BUCKET_NAME")
        aws_region = os.getenv("AWS_REGION")
        
        if not self.bucket:
            raise ValueError("BUCKET_NAME n'est pas défini dans les variables d'environnement")
        
        if not aws_region:
            raise ValueError("AWS_REGION n'est pas défini dans les variables d'environnement")
        
        self.client = boto3.client("s3", region_name=aws_region)

    def list_documents(self, prefix: str = "offcourse_doc/", extensions: Tuple[str, ...] = (".pdf", ".docx")) -> List[str]:
        keys: List[str] = []
        paginator = self.client.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if key.lower().endswith(extensions):
                    keys.append(key)

        return keys

    def download(self, key: str, local_dir: str = "./assets") -> str:
        os.makedirs(local_dir, exist_ok=True)
        filename = os.path.basename(key)
        local_path = os.path.join(local_dir, filename)

        try:
            self.client.download_file(self.bucket, key, local_path)
        except ClientError as e:
            raise RuntimeError(f"Erreur téléchargement {key} : {e}") from e

        return local_path
