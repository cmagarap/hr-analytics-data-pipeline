
# HR Recruitment Analytics Pipeline

This project is an HR analytics service designed to extract, transform, and analyze data from multiple sources using Apache Spark. It processes data and generates reports related to job applications, candidates, education, and work experience.

The service uses Docker for containerization, and the code is written in Python with Spark, utilizing MySQL for data storage.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Building the Docker Image](#building-the-docker-image)
- [Running the Services](#running-the-services)
- [Project Structure](#project-structure)
- [Logs](#logs)
- [Error Handling](#error-handling)
- [Stopping the Services](#stopping-the-services)
- [Additional Notes](#additional-notes)

---

## Prerequisites

Before running the services, make sure you have the following installed:

1. **Docker** - To build and run the containers.
   - [Install Docker](https://docs.docker.com/get-docker/)

---

## Building the Docker Image

### 1. Clone the repository

If you haven’t already, clone the repository:

```bash
git clone https://github.com/cmagarap/hr-analytics-data-pipeline.git
cd hr-analytics-data-pipeline
```
You may use SSH is HTTPS clone does not work.
### 2. Build the Docker Image

Once in the project directory, build the Docker image using the following command:

```bash
docker-compose up --build
```

This command will build a Docker image tagged `hr-analytics-data-pipeline-app` from the `Dockerfile` in the repository.

---

## Running the Services

### 1. Run Docker Container

To start the service, you can also use the `docker-compose up` command:

```bash
docker-compose up
```

This will start the container and run both `main.py` and `generate_reports.py` inside the container.

#### Optionally, Run with Detached Mode

To run the container in the background (detached mode):

```bash
docker-compose up -d
```

---

## Project Structure

Here’s a brief overview of the project’s file structure:

```
hr-analytics-data-pipeline/
├── Dockerfile                         # Docker image configuration
├── docker-compose.yml                 # Orchestrates the ETL pipeline and MySQL database services
├── requirements.txt                   # Python dependencies
├── sql                                # DDL scripts for raw data
│   ├── 01_candidates_raw.sql
│   ├── 02_work_experience_raw.sql
│   ├── 03_education_raw.sql
│   └── 04_applications_raw.sql
└── src                                         # Contains the source code
    ├── connector
    │   └── mysql-connector-java-8.0.13.jar
    ├── generate_reports.py                     # Script to generate reports
    ├── jobs                                    # Contains individual transformation modules
    │   ├── applications_data.py
    │   ├── candidates_data.py
    │   ├── education_data.py
    │   └── work_experience_data.py
    ├── main.py                                 # Main ETL script for data transformation and writing to MySQL
    ├── reports                                 # Output directory for generated CSV reports
    │   ├── applications_per_job_role
    │   ├── candidate_success_rate
    │   ├── daily_application_summary
    │   ├── education_levels_by_job_role
    │   └── top_10_candidates_by_experience
    └── utils.py                                # Python utility functions
```

### Key Files:
- **Dockerfile**: Defines the environment for the service, including installing dependencies such as Python, Java, Spark, and MySQL client.
- **docker-compose.yml**: Defines and manages multi-container services for the application, including the ETL service and MySQL database, ensuring seamless interaction between them.
- **main.py**: Runs the ETL process, extracting data from MySQL, transforming it, and writing back to MySQL.
- **generate_reports.py**: Generates reports based on the transformed data and saves them as CSV files.
- **requirements.txt**: Lists the Python dependencies (e.g., `pyspark`, `mysql-connector-python`).
- **jobs/**: Contains individual transformation modules for processing different data aspects like candidates, work experience, etc.
- **utils.py**: Contains utility functions for the entire project.

---

## Logs

Logs from both `main.py` and `generate_reports.py` will be displayed in the Docker container’s output. You can view the logs by running:

```bash
docker logs -f pipeline_app_service
```

This will display real-time logs from the running container.

---

## Error Handling

In case of errors during the ETL process or report generation, error messages will be logged using the Python `logging` module. Any exceptions that occur during data extraction, transformation, or writing will be captured and logged with a stack trace.

---

## Stopping the Services

To stop the running Docker container, press `CTRL + C` in the terminal where the container is running. This will stop the containers that were started in the foreground.

If you started the containers in detached mode using docker-compose up -d, you can stop them by running:

```bash
docker-compose down
```

---

## Additional Notes

- This project is containerized using Docker, meaning all the necessary software dependencies, including Python, MySQL, Java (for PySpark), and any additional libraries are bundled within Docker containers.  As a result, you don't need to install MySQL, Java, or any other dependencies manually on your local machine.
- You can simply build and run the containers using Docker and Docker Compose, which ensures a consistent environment across different systems, making setup and deployment easier and faster.
- The dataset inside the SQL folder only has a few rows. The difference in reports will be seen once data grows.
- The reports generated by `generate_reports.py` will be saved in the `reports/` directory inside the container. If you want to persist them on your local machine, you can mount a local directory to the container's `reports/` directory.

For example:

```bash
docker run -v /path/to/local/reports:/reports --name hr-analytics-data-pipeline-app ...
```

This will ensure that the reports are saved in `/path/to/local/reports` on your local machine.

---
