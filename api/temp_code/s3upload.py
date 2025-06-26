import boto3

# Set up S3 client
# See Notepad

# Local file and target bucket/key
local_file = 'Math_Concepts_Practice_Exam_1.pdf'
bucket_name = 'study-buddy-app'
s3_key = 'uploads/Math_Concepts_Practice_Exam_1.pdf'  # folder/key path in bucket

# Upload the file
try:
  # s3.upload_file(local_file, bucket_name, s3_key)
  print(f'Successfully uploaded {local_file} to s3://{bucket_name}/{s3_key}')
except Exception as e:
  print('Upload failed:', e)