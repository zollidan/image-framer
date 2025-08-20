import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings # Импортируем настройки Django

class S3BucketService:
    def __init__(
        self,
        bucket_name: str,
        endpoint: str,
        access_key: str,
        secret_key: str,
    ) -> None:
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    def create_s3_client(self) -> boto3.client:
        client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version="s3v4"),
        )
        return client

    def upload_object(self, source_file_name: str, content: bytes) -> None:
        client = self.create_s3_client()
        try:
            response = client.put_object(
                Bucket=self.bucket_name,
                Key=source_file_name,
                Body=content,
            )
            return response
        except ClientError as e:
            raise e

    def create_bucket(self):
        try:
            client = self.create_s3_client()
            client.create_bucket(Bucket=self.bucket_name)
        except Exception as e:
            return e

    def get_object_by_key(self, file_key):
        client = self.create_s3_client()

        try:
            return client.get_object(Bucket=self.bucket_name, Key=file_key)
        except ClientError as e:
            return e

    def list_objects(self, ) -> list[str]:
        client = self.create_s3_client()

        response = client.list_objects_v2(
            Bucket=self.bucket_name)
        storage_content: list[str] = []

        try:
            contents = response["Contents"]
        except KeyError:
            return storage_content

        for item in contents:
            storage_content.append(item["Key"])

        return storage_content



def get_s3_service() -> S3BucketService:
    """Фабрика для создания экземпляра сервиса S3 из настроек Django."""
    return S3BucketService(
        settings.BUCKET_NAME,
        settings.ENDPOINT_URL,
        settings.ACCESS_KEY,
        settings.SECRET_KEY
    )

s3_service = get_s3_service()