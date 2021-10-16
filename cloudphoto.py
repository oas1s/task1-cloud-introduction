import os
import sys
import uuid

import boto3

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

commands = ['upload', 'download', 'list']


def upload_photos(path, album):
    s3.upload_file(path, 'bucket-cloud-photo', uuid.uuid4().__str__() + "_" + album + ".jpg")


def download_photos(path, album):
    names = []
    for key in s3.list_objects(Bucket='bucket-cloud-photo')['Contents']:
        names.append(key['Key'])
    for name in names:
        x = name.split("_")
        if album in x[1]:
            s3.download_file('bucket-cloud-photo', name, path + name)


def print_albums_photos(album):
    names = []
    for key in s3.list_objects(Bucket='bucket-cloud-photo')['Contents']:
        names.append(key['Key'])
    for name in names:
        x = name.split("_")
        if album in x[1]:
            print(name)


def print_albums():
    names = []
    albums = []
    for key in s3.list_objects(Bucket='bucket-cloud-photo')['Contents']:
        names.append(key['Key'])
    for name in names:
        x = name.split("_")
        albums.append(x[1].split(".")[0])
    unique_alb = set(albums)
    print(unique_alb)


if __name__ == '__main__':
    if sys.argv[1] not in commands:
        print('I dont have this features yet ' + sys.argv[1])
        sys.exit()

    if sys.argv[1] == 'upload':
        for x in os.listdir(sys.argv[3]):
            if x.endswith(".jpg"):
                upload_photos(x, sys.argv[5])

    if sys.argv[1] == 'download':
        download_photos(sys.argv[3], sys.argv[5])

    if sys.argv[1] == 'list':
        if len(sys.argv) > 2:
            print_albums_photos(sys.argv[3])
        else:
            print_albums()
