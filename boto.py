#%%

import boto3 
import os

class Upload:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def uploadfile(self, address):
        self.directory = os.fsencode(f'{address}/images')
    
        for image in os.listdir(self.directory):
            try:
                self.imagename = os.fsdecode(image) 
                # print(os.path.join(directory, filename))
                for self.im in self.imagename:
                    self.response = self.s3_client.upload_file(f'{self.im}', 'deliveroobucket', f'{self.im}')
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
test1.uploadfile('data/SW1A 0AA')


# %%
test1.viewbucket()
# %%
