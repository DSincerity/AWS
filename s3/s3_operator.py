import boto3
import os
from tqdm import tqdm
from botocore.exceptions import ClientError

os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "<AWS credential.ini file path>"
profile_name = "dev"


class S3Connector(object):
    """S3 connector for listing, uploading, downloading and deleting files in/to/from S3"""

    def __init__(self, profile_name):

        session = boto3.Session(profile_name=profile_name)
        self.s3_client = session.resource("s3")

    def list_buckets(self):
        """list buckets in s3"""

        return [bucket for bucket in self.s3_client.buckets.all()]

    def list_objects(self, bucket, prefix="", Delimiter="/"):
        """list objects in a speckfic bucket of s3"""

        _bucket = self.s3_client.Bucket(bucket)
        objs = _bucket.objects.filter(Prefix=prefix)

        return [obj for obj in objs]

    def upload_files(self, file_path, bucket, prefix=""):
        """upload single/multiple fils to s3

        Arguments:
        file_path: a file_path in local to upload to s3 bucket.
            This can be a directory path for files or a single file path.
        bucket: a bucket name in s3
        prefix: a key under a bucket. This is like a file path to save in s3
        """

        aws_bucket = self.s3_client.Bucket(name=bucket)

        if os.path.isdir(file_path):
            print("> file path is a directory")
            file_list = [
                os.path.join(file_path, file_name)
                for file_name in os.listdir(file_path)
            ]

        elif os.path.isfile(file_path):
            print("> file path is a file")
            file_list = [file_path]

        # upload files
        try:
            upload_obj_cnt = 0
            for _file in tqdm(file_list):
                s3_file_key = os.path.join(prefix, _file.split("/")[-1])
                aws_bucket.upload_file(_file, s3_file_key)
                upload_obj_cnt += 1
            return upload_obj_cnt

        except ClientError as e:
            print(e)
            return 0

    def download_files(self, save_path, bucket, prefix=""):
        """download objects from s3 to local

        Arguments:
        save_path: a file_path in local to download from s3 bucket.
            This should be a directory path. A file name will be assigned with the files' in s3
        bucket: a bucket name where objects will be downloaded in s3
        prefix: a key (indicating a path in s3) under which objects will be downloaded
        """

        aws_bucket = self.s3_client.Bucket(name=bucket)

        # download files
        try:
            download_obj_cnt = 0
            for obj in tqdm(list(aws_bucket.objects.filter(Prefix=prefix))):
                aws_bucket.download_file(
                    obj.key, os.path.join(save_path, obj.key.split("/")[-1])
                )
                download_obj_cnt += 1

            return download_obj_cnt

        except ClientError as e:
            print(e)
            return 0

    def remove_bucket_object(self, bucket, prefix=""):
        """remove objects in a specific bucket of s3

        Arguments:
        bucket: a bucket name where objects will be deleted in s3
        prefix: a key (indicating a path in s3) under which objects will be deleted
        """

        aws_bucket = self.s3_client.Bucket(name=bucket)
        assert prefix != "", "Please specify the prefix in a bucket"

        # remove files
        try:
            delete_obj_cnt = 0
            for obj in tqdm(list(aws_bucket.objects.filter(Prefix=prefix))):
                aws_bucket.delete_objects(
                    Delete={
                        "Objects": [
                            {
                                "Key": obj.key,
                            }
                        ]
                    }
                )
                delete_obj_cnt += 1

            return delete_obj_cnt

        except ClientError as e:
            print(e)
            return 0

