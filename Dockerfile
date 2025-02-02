FROM python:3.11.8-bullseye

# Install Java (required for PySpark)
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=${JAVA_HOME}/bin:${PATH}

# Install MySQL
RUN apt-get install -y default-mysql-client

WORKDIR /src

COPY . /src/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python main.py && wait && python generate_reports.py"]

