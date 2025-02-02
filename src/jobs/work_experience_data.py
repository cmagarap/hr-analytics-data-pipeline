from pyspark.sql import functions as F
from pyspark.sql import Window
from utils import fill_null_or_empty

def transform_work_experience_data(work_exp_data):
    """
    Transforms the work experience data by handling missing values, calculating job duration,
    and computing employment gaps between jobs.

    Args:
        work_exp_data (DataFrame): The input DataFrame containing work experience data with columns like
                                   'candidate_id', 'job_title', 'company_name', 'start_date', and 'end_date'.

    Returns:
        DataFrame: The transformed work experience data with missing values filled,
                   calculated job duration, and gap days between jobs.
    """
    work_exp_data = fill_null_or_empty(work_exp_data, ['job_title', 'company_name', 'description'])

    work_exp_data = work_exp_data.withColumn(
        'end_date',
        F.coalesce(F.col('end_date'), F.current_date())  # If end_date is NULL, use the current date.
    )

    # Compute years of experience per job
    work_exp_data = work_exp_data.withColumn(
        "number_of_years",
        F.round((F.datediff(F.coalesce(F.col("end_date"), F.current_date()),
                        F.col("start_date")).cast("double") / 365), 1)
    )

    # Calculate gap days between jobs
    window_spec = Window.partitionBy("candidate_id").orderBy("start_date")
    work_exp_data = work_exp_data.withColumn(
        "prev_end_date", F.lag("end_date").over(window_spec)
    )
    work_exp_data = work_exp_data.withColumn(
        "gap_days_between_jobs",
        F.when(F.col("prev_end_date").isNotNull(), F.datediff(F.col("start_date"), F.col("prev_end_date"))).otherwise(0)
    )

    return work_exp_data
