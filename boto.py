
import boto3 
import os
from botocore.config import Config
from config import config

class Upload:

    def set_up_boto(self):
        my_config = Config(
            region_name=config['REGION_NAME'],
            aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY']
            )

        self.s3_client = boto3.client('s3', config=my_config)

    def upload_file(self, path):
        # self.directory = os.fsencode(f'{address}/images')
        bucketname = 'deliveroobucket'
        
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    self.s3_client.upload_file(os.path.join(root, file), bucketname, f'{path}/{file}')
                except:
                    print('excepted')
                    pass

    def view_bucket(self):
        self.s3 = boto3.resource('s3')
        self.my_bucket = self.s3.Bucket('deliveroobucket')
        
        for file in self.my_bucket.objects.all():
             print(file.key)

#%%

# test1 = Upload()
# test1.uploadfile('data/')


