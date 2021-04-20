import datetime
AWS_GROUP_NAME = "team5_ecommerce"
AWS_USERNAME = "team5-ecommerce-user"
# username and group for reference
AWS_ACCESS_KEY_ID = "AKIAZQPOEFKFKCHTDSFN"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'ecommerce.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'ecommerce.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'team5ecommerce'
S3DIRECT_REGION = 'us-east-2'
AWS_S3_REGION_NAME = 'us-east-2' #change to your region


S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}


