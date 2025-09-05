"""
S3 Bucket Service for interacting with S3-compatible storage.

This module provides a service class for performing operations like creating buckets,
uploading, and listing objects in an S3-compatible storage.
"""
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from .config import Settings


class S3BucketService:
    """
    A service for interacting with an S3-compatible storage bucket.
    """
    def __init__(
        self,
        bucket_name: str,
        endpoint: str,
        access_key: str,
        secret_key: str,
    ) -> None:
        """
        Initializes the S3BucketService.

        Args:
            bucket_name (str): The name of the S3 bucket.
            endpoint (str): The S3 endpoint URL.
            access_key (str): The access key for the S3 bucket.
            secret_key (str): The secret key for the S3 bucket.
        """
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    def create_s3_client(self) -> boto3.client:
        """
        Creates and returns a boto3 S3 client.

        Returns:
            boto3.client: An S3 client instance.
        """
        client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version="s3v4"),
        )
        return client

    def create_bucket(self):
        """
        Creates the S3 bucket if it doesn't exist.

        Returns:
            Exception: An exception if the bucket creation fails, otherwise None.
        """
        try:
            client = self.create_s3_client()
            client.create_bucket(Bucket=self.bucket_name)
        except Exception as e:
            return e

    def get_object_by_key(self, file_key):
        """
        Retrieves an object from the S3 bucket by its key.

        Args:
            file_key (str): The key of the object to retrieve.

        Returns:
            dict: The S3 object, or a ClientError if the object is not found.
        """
        client = self.create_s3_client()

        try:
            return client.get_object(Bucket=self.bucket_name, Key=file_key)
        except ClientError as e:
            return e

    def list_objects(self, ) -> list[str]:
        """
        Lists all object keys in the S3 bucket.

        Returns:
            list[str]: A list of object keys.
        """
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

    def upload_object(self, source_file_name: str, content: bytes) -> None:
        """
        Uploads an object to the S3 bucket.

        Args:
            source_file_name (str): The key to use for the object in the bucket.
            content (bytes): The content of the object to upload.

        Raises:
            ClientError: If the upload fails.

        Returns:
            dict: The response from the S3 put_object call.
        """
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


def s3_bucket_service_factory(settings: Settings) -> S3BucketService:
    """
    Factory function to create an S3BucketService instance from settings.

    Args:
        settings (Settings): The application settings.

    Returns:
        S3BucketService: An instance of S3BucketService.
    """
    return S3BucketService(settings.BUCKET_NAME, settings.ENDPOINT, settings.ACCESS_KEY, settings.SECRET_KEY)
