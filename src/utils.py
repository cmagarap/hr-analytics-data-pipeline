from pyspark.sql import functions as F
from pyspark.sql import Window


def extract_data_from_mysql(spark, tables=None):
    """
    Extracts data from MySQL into PySpark DataFrames.

    Args:
        spark: The SparkSession object used for DataFrame operations.
        tables: A list of table names to extract (optional). Defaults to a predefined list.

    Returns:
        dict: A dictionary containing DataFrames for each table.
    """
    if tables is None:
        tables = ['candidates', 'work_experience', 'education', 'applications']

    data = {}
    for table in tables:
        data[table] = load_table(spark, table)

    return data


def fill_null_or_empty(df, column_names, replacement_value='Unknown'):
    """
    Fills NULL or empty string values in specified columns of a DataFrame with a replacement value.

    Args:
        df (DataFrame): The input PySpark DataFrame.
        column_names (list): A list of column names where NULL or empty values should be replaced.
        replacement_value (str, optional): The value to replace NULL or empty values with. Defaults to 'Unknown'.

    Returns:
        DataFrame: The DataFrame with NULL or empty values replaced in the specified columns.
    """
    for column_name in column_names:
        df = df.withColumn(
            column_name,
            F.when((F.col(column_name).isNull()) | (F.col(column_name) == ''),
                   F.lit(replacement_value)).otherwise(F.col(column_name))
        )
    return df


def handle_incorrect_format(candidates_data):
    """
    Corrects the phone and email formats in the candidates DataFrame.

    Args:
        candidates_data (DataFrame): The input DataFrame containing candidate data with phone and email columns.

    Returns:
        DataFrame: The DataFrame with corrected phone and email formats. Invalid entries are replaced with 'Unknown'.
    """
    return candidates_data.withColumn(
            'phone', F.when(F.col('phone').rlike(r"^\d{3}-\d{4}$"), F.col('phone')).otherwise('Unknown')
        ).withColumn(
            'email',
            F.when(F.col('email').rlike(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"), F.col('email')).otherwise(
                'Unknown')
        )


def load_table(spark, table_name, db_url='jdbc:mysql://pipeline_mysql_db:3306/hr_analytics_db',
               user='root', password='root123'):
    """
    Loads a table from a MySQL database into a PySpark DataFrame.

    Args:
        spark: The SparkSession object used for DataFrame operations.
        table_name: The name of the table to load from the database.
        db_url: The JDBC URL of the database. Default is 'jdbc:mysql://pipeline_mysql_db:3306/hr_analytics_db'.
        user: The username for the MySQL database. Default is 'root'.
        password: The password for the MySQL database. Default is 'root123'.

    Returns:
        A PySpark DataFrame containing the data from the specified MySQL table.
    """
    return spark.read \
        .format('jdbc') \
        .option('url',
                f'{db_url}?user={user}&password={password}&allowPublicKeyRetrieval=true&useSSL=false&requireSSL=false') \
        .option('dbtable', table_name) \
        .option('driver', 'com.mysql.cj.jdbc.Driver') \
        .load()


def write_to_mysql(spark, df, table_name):
    """
    Write a DataFrame to MySQL.

    Args:
        spark: The Spark session.
        df: The DataFrame to write.
        table_name: The target MySQL table name.
    """
    jdbc_url = "jdbc:mysql://pipeline_mysql_db:3306/hr_analytics_db?useSSL=false"
    properties = {
        "user": "root",
        "password": "root123",
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    df.write \
        .jdbc(jdbc_url, table_name, mode="overwrite", properties=properties)
