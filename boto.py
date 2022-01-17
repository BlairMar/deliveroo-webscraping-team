#%%

import boto3 
import os

class Upload:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def uploadfile(self, path):
        # self.directory = os.fsencode(f'{address}/images')
        bucketname = 'deliveroobucket'
        
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    self.s3_client.upload_file(os.path.join(root, file), bucketname, file)
                except:
                    print('excepted')
                    pass

    def viewbucket(self):
        self.s3 = boto3.resource('s3')
        self.my_bucket = self.s3.Bucket('deliveroobucket')
        
        for file in self.my_bucket.objects.all():
             print(file.key)

#%%

test1 = Upload()
test1.uploadfile('data/')


# %%
test1.viewbucket()
# %%
