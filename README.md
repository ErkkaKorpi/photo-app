# photo-app

Photo application to display pictures from private S3 bucket

prerequisites: Docker and docker-compose installed to host, AWS account, S3 bucket, IAM user

- Create bucket in AWS and IAM user that has read access to the bucket
- Upload photos to bucket
- Run "start_app.sh" script and give it 5 parameters in the following order: bucketname, AWS access key, AWS secred access    key, database username, database user password
- script will build necessary Docker containers and start the application and database
- application will be reachable from http://localhost
