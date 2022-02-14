import boto3 
import os
from botocore.config import Config
from config import config
from logger import log

class Upload:

    def __init__(self):
        my_config = Config(
            region_name=config['REGION_NAME']
        )

        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                                      aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'],
                                      config=my_config)
        

    def upload_file(self, filename, directory=None, bucketname='deliveroobucket'):
        """Upload a file to an S3 bucket
        
        :param filename: File to upload
        :param bucketname: Bucket to upload to.
        :param directory: Directory for file to uploaded inside. If not specified, then is saved in the bucket.
        :return: s3 path/key of file.
        """
        if directory is None:
            objectname = os.path.basename(filename)
        else:
            objectname = f'{directory}/{os.path.basename(filename)}'
        
        try:
            self.s3_client.upload_file(filename, bucketname, objectname)
        except Exception as e:
            log('error', f'Unable to upload file: {e}')
        return objectname


    def view_bucket(self):
        self.s3 = boto3.resource('s3')
        self.my_bucket = self.s3.Bucket('deliveroobucket')
        
        for file in self.my_bucket.objects.all():
             print(file.key)