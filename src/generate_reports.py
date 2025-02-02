import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window
from utils import extract_data_from_mysql, write_to_mysql

logging.basicConfig(level=logging.INFO)


def generate_daily_application_summary(applications_data):
    """
    Generates a daily summary of applications, including counts of accepted, pending, rejected,
    and interview applications.

    Args:
        applications_data (DataFrame): The input DataFrame containing application data with
                                       columns like 'application_date' and 'status'.

    Returns:
        DataFrame: A DataFrame containing the daily summary, grouped by 'application_date'
                   with counts of different application statuses.
    """
    daily_summary = applications_data.groupBy("application_date") \
        .agg(
        F.count("application_id").alias("total_applications"),
        F.sum((F.col("status") == "Accepted").cast("int")).alias("accepted_applications"),
        F.sum((F.col("status") == "Pending").cast("int")).alias("pending_applications"),
        F.sum((F.col("status") == "Rejected").cast("int")).alias("rejected_applications"),
        F.sum((F.col("status") == "Interview").cast("int")).alias("interview_applications")
    ).orderBy("application_date")

    return daily_summary


def generate_candidate_success_rate(applications_data, candidates_data):
    """
    Calculates the success rate for each candidate based on the number of accepted applications.

    Args:
        applications_data (DataFrame): The input DataFrame containing application data
                                       with columns like 'candidate_id' and 'status'.
        candidates_data (DataFrame): The input DataFrame containing candidate data with
                                     'candidate_id' and 'full_name'.

    Returns:
        DataFrame: A DataFrame containing candidate success rates, including
        the candidate's name, total applications, and accepted applications.
    """
    candidate_total_applications = applications_data.groupBy("candidate_id") \
        .agg(
        F.count("application_id").alias("total_applications"),
        F.sum((F.col("status") == "Accepted").cast("int")).alias("accepted_applications")
    )

    # Calculate the success rate for each candidate
    candidate_success_rate = candidate_total_applications.withColumn(
        "success_rate",
        F.when(F.col("total_applications") == 0, 0).otherwise(
            F.col("accepted_applications") / F.col("total_applications"))
    )

    candidate_success_rate_with_name = candidate_success_rate.join(
        candidates_data,
        on="candidate_id",
        how="left"
    ).select(
        "candidate_id", "full_name", "total_applications", "accepted_applications", "success_rate"
    )

    return candidate_success_rate_with_name


def generate_top_10_candidates_by_experience(experience_data):
    """
    Generates the top 10 candidates with the most years of experience.

    Args:
        experience_data (DataFrame): The input DataFrame containing candidate experience data
                                     with 'candidate_id' and 'number_of_years' columns.

    Returns:
        DataFrame: A DataFrame containing the top 10 candidates sorted by
                   their total years of experience in descending order.
    """
    candidate_experience = experience_data.groupBy("candidate_id") \
        .agg(
        F.sum("number_of_years").alias("total_experience_years")
    ).orderBy(F.col("total_experience_years").desc())

    top_10_candidates = candidate_experience.limit(10)

    return top_10_candidates


def generate_applications_per_job_role(applications_data):
    """
    Generates a summary of total applications per job role, sorted by the number of applications.

    Args:
        applications_data (DataFrame): The input DataFrame containing application data with a 'job_role' column.

    Returns:
        DataFrame: A DataFrame containing the total number of applications per job role, sorted in descending order of applications.
    """
    job_role_applications = applications_data.groupBy("job_role") \
        .agg(F.count("application_id").alias("total_applications")) \
        .orderBy(F.col("total_applications").desc())

    return job_role_applications


def generate_education_levels_by_job_role(applications_data, candidates_data, education_data):
    """
    Generates a summary of total applications per job role, sorted by the number of applications.

    Args:
        applications_data (DataFrame): The input DataFrame containing application data with a 'job_role' column.

    Returns:
        DataFrame: A DataFrame containing the total number of applications per job role,
                   sorted in descending order of applications.
    """
    applications_with_candidates = applications_data.join(
        candidates_data, "candidate_id", "left"
    )

    applications_with_education = applications_with_candidates.join(
        education_data, "candidate_id", "left"
    )

    # Categorize education levels
    education_categorized = applications_with_education.withColumn(
        "education_level",
        F.when(F.col("degree").startswith("BSc"), "Bachelor")
        .when(F.col("degree").startswith("MSc"), "Master")
        .when(F.col("degree").startswith("MBA"), "Master")
        .when(F.col("degree").startswith("PhD"), "Doctorate")
        .otherwise("Other")
    )

    education_summary = education_categorized.groupBy("job_role", "education_level") \
        .agg(F.countDistinct("candidate_id").alias("num_candidates")) \
        .orderBy("job_role", "education_level")

    return education_summary


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
        tables = ['candidates_final', 'work_experience_final', 'education_final', 'applications_final']
        data = extract_data_from_mysql(spark, tables)
        logging.info("Data extraction completed.")

        candidates_data = data["candidates_final"]
        applications_data = data["applications_final"]
        work_exp_data = data["work_experience_final"]
        education_data = data["education_final"]

        daily_summary = generate_daily_application_summary(applications_data)
        candidate_success_rate = generate_candidate_success_rate(applications_data, candidates_data)
        top_10_candidates = generate_top_10_candidates_by_experience(work_exp_data)
        app_per_job_role = generate_applications_per_job_role(applications_data)
        educ_lvl_by_job_role = generate_education_levels_by_job_role(applications_data, candidates_data, education_data)

        try:
            logging.info(f"Writing records to daily_application_summary.csv...")
            daily_summary.write.csv("reports/daily_application_summary", header=True, mode="overwrite")
            logging.info("Successfully written daily_application_summary data.")

            logging.info(f"Writing records to candidate_success_rate.csv...")
            candidate_success_rate.write.csv("reports/candidate_success_rate", header=True, mode="overwrite")
            logging.info("Successfully written candidate_success_rate data.")

            logging.info(f"Writing records to top_10_candidates_by_experience.csv...")
            top_10_candidates.write.csv("reports/top_10_candidates_by_experience", header=True, mode="overwrite")
            logging.info("Successfully written top_10_candidates_by_experience data.")

            logging.info(f"Writing records to applications_per_job_role.csv...")
            app_per_job_role.write.csv("reports/applications_per_job_role", header=True, mode="overwrite")
            logging.info("Successfully written applications_per_job_role data.")

            logging.info(f"Writing records to education_levels_by_job_role.csv...")
            educ_lvl_by_job_role.write.csv("reports/education_levels_by_job_role", header=True, mode="overwrite")
            logging.info("Successfully written education_levels_by_job_role data.")
        except Exception as e:
            logging.error(f"Error encountered while writing to CSV: {e}")


    except Exception as e:
        logging.error(f"Error during processing: {e}")


if __name__ == '__main__':
    main()