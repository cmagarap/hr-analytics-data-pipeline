import logging
from pyspark.sql import SparkSession
from jobs.candidates_data import transform_candidates_data
from jobs.work_experience_data import transform_work_experience_data
from jobs.applications_data import transform_applications_data
from jobs.education_data import transform_education_data
from utils import extract_data_from_mysql, write_to_mysql

logging.basicConfig(level=logging.INFO)


def transform_data(data):
    """
    Transforms the extracted data by filling missing values and correcting formats.

    Args:
        data: A dictionary containing the dataframes for each table.

    Returns:
        dict: A dictionary containing the transformed dataframes.
    """
    candidates_data = data["candidates"]
    work_exp_data = data["work_experience"]
    education_data = data["education"]
    applications_data = data["applications"]

    work_exp_data = transform_work_experience_data(work_exp_data)
    candidates_data = transform_candidates_data(candidates_data, work_exp_data)
    applications_data = transform_applications_data(applications_data)
    education_data = transform_education_data(education_data, work_exp_data)

    return {
        "candidates": candidates_data,
        "work_experience": work_exp_data,
        "applications": applications_data,
        "education": education_data
    }


def main():
    try:
        logging.info("Initializing Spark session...")
        spark = SparkSession.builder \
            .master("local") \
            .appName("HRAnalytics") \
            .config("spark.executor.memory", "5g") \
            .config("spark.cores.max", "6") \
            .config("spark.jars", "connector/mysql-connector-java-8.0.13.jar") \
            .config("spark.driver.extraClassPath", "connector/mysql-connector-java-8.0.13.jar") \
            .getOrCreate()
        logging.info("Spark session initialized.")

        logging.info("Extracting data from MySQL...")
        data = extract_data_from_mysql(spark)
        logging.info("Data extraction completed.")

        # Perform data transformations
        transformed_data = transform_data(data)

        logging.info("Doing transformations...")
        candidates_data = transformed_data["candidates"]
        work_exp_data = transformed_data["work_experience"]
        applications_data = transformed_data["applications"]
        education_data = transformed_data["education"]

        try:
            logging.info(f"Writing records to candidates_final...")
            write_to_mysql(spark, candidates_data, "candidates_final")
            logging.info("Successfully written candidates_final data.")

            logging.info(f"Writing records to work_experience_final...")
            write_to_mysql(spark, work_exp_data, "work_experience_final")
            logging.info("Successfully written work_experience_final data.")

            logging.info(f"Writing records to applications_final...")
            write_to_mysql(spark, applications_data, "applications_final")
            logging.info("Successfully written applications_final data.")

            logging.info(f"Writing records to education_final...")
            write_to_mysql(spark, education_data, "education_final")
            logging.info("Successfully written education_final data.")
        except Exception as e:
            logging.error(f"Error encountered while writing to MySQL: {e}")

    except Exception as e:
        logging.error(f"Error during processing: {e}")


if __name__ == '__main__':
    main()
