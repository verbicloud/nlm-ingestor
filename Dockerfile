# syntax=docker/dockerfile:experimental

FROM python:3.11-bookworm

# Update and install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libxml2-dev libxslt-dev \
    build-essential libmagic-dev \
    unzip git \
    && apt-get autoremove -y

# Install Java
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update -y && \
    apt-get install -y openjdk-17-jre-headless

# Install Tesseract OCR and dependencies
RUN apt-get install -y tesseract-ocr lsb-release && \
    echo "deb https://notesalexp.org/tesseract-ocr5/$(lsb_release -cs)/ $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/notesalexp.list > /dev/null && \
    apt-get update -oAcquire::AllowInsecureRepositories=true && \
    apt-get install -y notesalexp-keyring --allow-unauthenticated && \
    apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev && \
    wget -P /usr/share/tesseract-ocr/5/tessdata/ \
        https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# Set application directory
ENV APP_HOME=/app
WORKDIR ${APP_HOME}

# Copy project files
COPY pdf_converter/ ${APP_HOME}/

# Install Python dependencies
RUN pip install --upgrade pip setuptools && \
    pip install -r ${APP_HOME}/requirements.txt

# Install additional Python dependencies
RUN python -m nltk.downloader stopwords punkt
RUN python -c "import tiktoken; tiktoken.get_encoding(\"cl100k_base\")"

# Ensure script permissions
RUN chmod +x run.sh

# Environment variables for Apache Tika
ENV TIKA_SERVER_JAR=/app/jars/tika-server.jar
ENV TIKA_PATH=/app/jars/

# Install AWS Lambda Runtime Interface Client
RUN pip install awslambdaric

# Set entrypoint and command for AWS Lambda
CMD ["${APP_HOME}/run.sh"]
CMD ["lambda_function.lambda_handler"]
ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
