from pyspark.sql import functions as F
from utils import fill_null_or_empty

def transform_education_data(education_data, work_exp_data):
    """
    Transforms the education data by handling missing values, calculating time to degree completion,
    and computing the education gap, including the first degree start year and the highest degree completion year.

    Args:
        education_data (DataFrame): The input DataFrame containing education data with columns like
                                    'candidate_id', 'degree', 'institution', 'start_year', and 'completion_year'.
        work_exp_data (DataFrame): The input DataFrame containing work experience
                                   data (not used directly in the transformation here).

    Returns:
        DataFrame: The transformed education data with missing values handled, calculated
                   time to degree completion, first degree start year, and highest degree completion year.
    """
    # Handle missing or incomplete education data
    education_data = fill_null_or_empty(education_data, ['degree', 'institution', 'start_year', 'completion_year'])
    education_data = education_data.withColumn("start_year", F.year("start_year").cast("int"))
    education_data = education_data.withColumn("completion_year", F.year("completion_year").cast("int"))

    # Get the first degree start year (earliest start_year)
    first_degree_df = education_data.groupBy("candidate_id").agg(
        F.min("start_year").alias("first_degree_start_year")
    )

    # Get the highest degree completion year (latest completion_year)
    highest_degree_df = education_data.groupBy("candidate_id").agg(
        F.max("completion_year").alias("highest_degree_completion_year")
    )

    # Compute time to degree completion per degree
    education_data = education_data.withColumn(
        "time_to_degree_completion",
        (F.col("completion_year") - F.col("start_year"))
    )

    education_data = (education_data.join(first_degree_df, "candidate_id", "left")
                      .join(highest_degree_df, "candidate_id", "left"))

    return education_data
