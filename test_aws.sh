docker build -t testtdfconverter -f dockerfile12 .
docker run \
   --env-file .env \
   -v ~/.aws-lambda-rie:/aws-lambda \
   -v ./tmp:/tmp \
   -p 9000:8080 \
   --entrypoint /aws-lambda/aws-lambda-rie \
   testtdfconverter /usr/local/bin/python -m awslambdaric lambda_function.lambda_handler