from pyspark.sql import functions as F
from utils import fill_null_or_empty

def transform_applications_data(applications_data):
    """
    Transforms the applications data by handling missing values, formatting corrections,
    and adding a new column for the number of days since the application was submitted.

    Args:
        applications_data (DataFrame): The input DataFrame containing application data
                                       with columns like 'status' and 'application_date'.

    Returns:
        DataFrame: The transformed applications data with missing values handled,
                   and a new 'days_since_application' column.
    """
    applications_data = fill_null_or_empty(applications_data, ['status'])
    applications_data = applications_data.withColumn(
        "days_since_application",
        F.datediff(F.current_date(), F.col("application_date"))
    )

    return applications_data
