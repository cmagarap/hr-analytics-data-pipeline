from pyspark.sql import functions as F
from pyspark.sql import Window
from utils import handle_incorrect_format, fill_null_or_empty

def transform_candidates_data(candidates_data, work_exp_data):
    """
    Transforms the candidates data by adding total years of experience, current role, employment status,
    job changes, and average time spent per role.

    Args:
        candidates_data (DataFrame): The input DataFrame containing candidate data with
                                     'candidate_id' and other candidate details.
        work_exp_data (DataFrame): The input DataFrame containing work experience data with
                                   'candidate_id', 'job_title', 'end_date', and 'number_of_years'.

    Returns:
        DataFrame: The transformed candidates data, now including total years of experience,
                   current role, employment status, job changes, and average time spent per role.
    """
    candidates_data = handle_incorrect_format(candidates_data)

    # Aggregate total years of experience per candidate
    total_experience_df = work_exp_data.groupBy("candidate_id").agg(
        F.round(F.sum("number_of_years"), 1).alias("total_years_experience")
    )

    # Join with candidates_data to add the 'total_years_experience' column
    candidates_data = candidates_data.join(total_experience_df, "candidate_id", "left")

    # Get the current role for each candidate (latest job)
    window_spec = Window.partitionBy("candidate_id").orderBy(F.col("end_date").desc())
    latest_job_df = (
        work_exp_data
        .withColumn("latest_end_date", F.max("end_date").over(window_spec))
        .withColumn("current_role", F.first("job_title").over(window_spec))
    )
    latest_job_df = latest_job_df.filter(F.col("end_date") == F.col("latest_end_date"))

    candidates_data = candidates_data.join(
        latest_job_df.select("candidate_id", "current_role", "latest_end_date"),
        "candidate_id",
        "left"
    )

    candidates_data = candidates_data.withColumn(
        "is_currently_employed",
        F.when(F.col("latest_end_date") >= F.current_date(), 1).otherwise(0)
    ).drop("latest_end_date")

    job_change_count_df = work_exp_data.groupBy("candidate_id").agg(F.count("job_title").alias("job_changes"))
    candidates_data = candidates_data.join(job_change_count_df, "candidate_id", "left")
    candidates_data = candidates_data.withColumn(
        "average_time_per_role",
        F.round(F.col("total_years_experience") / F.col("job_changes"), 2)
    )

    return candidates_data
