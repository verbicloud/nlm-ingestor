docker build -t testtdfconverter .
docker run \
   --env-file .env \
   -v ~/.aws-lambda-rie:/aws-lambda \
   -v ./tmp:/tmp \
   -p 9000:8080 \
   --entrypoint /aws-lambda/aws-lambda-rie \
   testtdfconverter:latest /usr/local/bin/python -m awslambdaric lambda_function.lambda_handler