import boto3
from botocore.exceptions import ClientError
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class S3Service:
    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
    
    def list_documents(self, prefix: str = "offcourse_doc/") -> List[Dict]:
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' not in response:
                return []
            
            documents = []
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):
                    documents.append({
                        'key': obj['Key'],
                        'filename': obj['Key'].split('/')[-1],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat()
                    })
            
            return documents
        except ClientError as e:
            raise Exception(f"Erreur S3: {str(e)}")
    
    def get_document(self, key: str) -> bytes:
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"Document non trouvé: {str(e)}")
    
    def download_document(self, key: str, local_path: str) -> str:
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            self.s3_client.download_file(self.bucket_name, key, local_path)
            return local_path
        except ClientError as e:
            raise Exception(f"Erreur téléchargement: {str(e)}")


s3_service = S3Service()
