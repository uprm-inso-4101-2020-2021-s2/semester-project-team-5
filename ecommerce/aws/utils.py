from storages.backends.s3boto3 import S3Boto3Storage

# change location for static and media

StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')
MediaRootS3BotoStorage  = lambda: S3Boto3Storage(location='media')
