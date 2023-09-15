from enum import Enum
import pickle
from google.cloud.exceptions import NotFound
from datetime import datetime
import pandas as pd
import numpy as np
from google.cloud import bigquery
import sys
import pandas_gbq
from sqlalchemy.orm import Query
import path
try:
    from unit_stake.unitPrototyping import Unit
    from linker import Session, SessionBase
except ModuleNotFoundError:
    # setting path so we can call this from the root level
    directory = path.Path(__file__).abspath()
    sys.path.append(directory.parent.parent)
    from unit_stake.unitPrototyping import Unit
    from linker import Session, SessionBase

class SnapshottedResources(Enum):
    CONTACTS="contact"
    BUILDINGS="building__c"
    ACCOUNTS="account"
    CAMPAIGNS="renter_campaign__c"
    RESIDENT_PAYMENT_HISTORIES="resident_payment_history__c"
    ESCROW_TRANSACTIONS="transaction__c"
    SVD_TRANSACTIONS="svd_transactions"

class Snapshotter:
    """A class to store and retrieve daily snapshots
    of our data for easy tracking over time
    """
    def __init__(self, verbose=False):
        # Create a session
        snapshot_session: SessionBase = Session()
        self.snapshot_session = snapshot_session
        self.verbose=verbose

    def get_snapshot_dataset_name(self, resource):
        return f"stake-customer-data.snapshots_{resource}.data"

    def process_df_for_storage(self, df: pd.DataFrame):
        """Handle common errors with sqlalchemy queries and format data in a
        way that GBQ will accept

        Args:
            df (pd.DataFrame): the dataframe to process
        """
        # Convert "object" columns to strings
        object_cols = df.select_dtypes(include=[np.object]).columns
        df[object_cols] = df[object_cols].astype(str)

        # Handle boolean columns separately
        bool_cols = df.select_dtypes(include=[np.bool]).columns
        for column in bool_cols:

            # Check if the column contains boolean strings
            unique_values = df[column].dropna().unique()
            if set(unique_values) in {'True', 'False'} or set(unique_values) == {True, False} or set(unique_values) == {False}:
                # df.drop(column)
                df[column] = df[column].apply(lambda x: 'True' if x else 'False').astype(str)

        for column_name in df.columns:
            print(f"{column_name} dtype is {df[column_name].dtype}")
            if df[column_name].dtype == 'datetime64[ns]':
                df = df.drop(column_name, axis=1)

        return df

    def generate_bigquery_schema(self, df: pd.DataFrame):
        schema = []

        for column_name in df.columns:
            column_schema = {"name": column_name, "type": "STRING"}
            schema.append(column_schema)

        return schema

    def get_processed_df_from_query(self, query: Query) -> pd.DataFrame:
        df: pd.DataFrame = pd.read_sql(
            sql=query.statement,
            con=self.snapshot_session.bind
        )
        df['snapshot_date']=datetime.today().date().isoformat()
        df = self.process_df_for_storage(df)
        if self.verbose:
            print(df.head(20))
        return df

    def validate_df(self, df_to_store):
        if len(df_to_store) < 1:
            raise ValueError("You're trying to store an empty dataframe.. everything ok?")

    def store_data_in_gbq(self, df_to_store, dataset_name, table_name, schema):
        self.validate_df(df_to_store)
        # Create a BigQuery client
        client = bigquery.Client()

        # Create a dataset reference object
        dataset_ref = bigquery.DatasetReference(client.project, dataset_name)
        # Check if the dataset exists
        try:
            client.get_dataset(dataset_name)
            print("Dataset {} already exists".format(dataset_name))

            # Get the reference to the table
            table_ref = dataset_ref.table(table_name)
            # Create the table if it does not exist
            try:
                table = client.get_table(table_ref)
            except NotFound:
                table = bigquery.Table(table_ref, schema=schema)
                client.create_table(table)

        except NotFound:
            print(f"Dataset {dataset_name} was not found. Creating...")
            # Create the dataset
            dataset = bigquery.Dataset(dataset_ref)
            dataset = client.create_dataset(dataset)
            print("Created dataset {}".format(dataset.dataset_id))
            # Create the table
            table_ref = dataset_ref.table(table_name)
            table = bigquery.Table(table_ref, schema=schema)
            error = client.create_table(table)
            if error:
                print(f"Encountered errors while creating table: {error}")
            else:
                print(f"Created table {table_name} in dataset {dataset_name}...")

        # Append rows to the table
        ## TODO: set timeout and retry parameters for rows of data that failed to insert
        ## TODO: refactor to upload rows one at a time so a single error does not cause the entire upload to fail
        try:
            errors = client.insert_rows_from_dataframe(
                table=table,
                dataframe=df_to_store
            )
            if errors[0]!=[]: # the function above returns something that looks like this: [[], [], []] when success
                print(f"Encountered errors while inserting rows: {errors}")
            else:
                print(f"Successfully inserted {len(df_to_store)} rows into {dataset_name}.{table_name}")
        except Exception as e:
            print(f"Encountered an error while inserting rows: {e}")

    def retrieve_raw_snapshotted_data(
        self,
        resource: SnapshottedResources,
        limit: int = None,
        pickle_locally_for_faster_dev=False
        ):
        dataset_table_name = self.get_snapshot_dataset_name(resource=resource.value)
        print(dataset_table_name)
        print(f"retrieving snapshots of {resource} from {dataset_table_name}")
        if pickle_locally_for_faster_dev:
            local_storage_file_name = f"{resource.value}-pickled_locally_for_faster_dev.data"
            try:
                print(f"Trying to grab {local_storage_file_name} from local files...")
                # df = pickle.load(open(local_storage_file_name, "rb" ))
                df = pd.read_csv(f'{resource}.csv')
                print(f'\nRead the cvs for {resource}')
            except Exception as e:
                print(f"Can't load object storage for {resource} because {e}... generating...")

                if limit is not None:
                    query=f'select * from {dataset_table_name} limit {limit}'
                    df = pandas_gbq.read_gbq(query)
                else:
                    df = pandas_gbq.read_gbq(dataset_table_name)
                pickle.dump(df, open(dataset_table_name, "wb+" ))
                df.to_csv(f'{resource}.csv')
                print(f"Cached {resource.value} locally for faster dev")

        else:
            if limit is not None:
                query=f'select * from {dataset_table_name} limit 1000'
                df = pandas_gbq.read_gbq(query)
            else:
                query=f"""select * from {dataset_table_name}"""
                df = pandas_gbq.read_gbq(query)

        return df

    def snapshot_postgres_model_resource(self, resource):
        """
        Shortcut function to snapshot an entire postgres table.
        Usage: self.snapshot_postgres_model_resource(resource=Contact)
        Args:
            resource (_type_): probably a class from pgModels2.py, but also any
            SQLalchemy class that inherits from a Declarative Base (see pgModels2...)
        """
        # query the db how we usually would
        query = self.snapshot_session.query(resource)
        # get a df and schema from it
        df = self.get_processed_df_from_query(query=query)
        # lets use a good string tablename for the resource
        resource_name = resource.__tablename__
        dataset_name = f"snapshots_{resource_name}"
        table_name = "data"

        print(f"Snapshotting {str(resource_name)}")
        self.snapshot_data(
            df_to_store=df,
            dataset_name=dataset_name,
            table_name=table_name
        )

    def flatten_dict(self, d: dict, parent_key='', sep='_') -> dict:
        """A recursive function to flatten an array of dictionaries into a 2D data structure

        Args:
            d (dict): _description_
            parent_key (str, optional): _description_. Defaults to ''.
            sep (str, optional): _description_. Defaults to '_'.

        Returns:
            dict: _description_
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.append((new_key, str(v)))
            else:
                items.append((new_key, str(v)))
        return dict(items)

    def dictionaries_to_dataframe(self, data: list[dict]) -> pd.DataFrame:
        flattened_data = [self.flatten_dict(d) for d in data]
        df = pd.DataFrame(flattened_data)
        print(f"flattened dics to df with columns {df.columns} {df.head(5)}")
        return df

    def snapshot_unit_transactions(self):
        unit_client = Unit()
        all_transactions = unit_client.getAllTransactions()
        transactions_df = self.dictionaries_to_dataframe(all_transactions)
        self.snapshot_data(
            df_to_store=transactions_df,
            dataset_name = f"snapshots_svd_transactions",
            table_name='data'
        )

    def snapshot_data(self, df_to_store, dataset_name, table_name):

        schema = self.generate_bigquery_schema(df_to_store)

        self.store_data_in_gbq(
            df_to_store=df_to_store,
            dataset_name=dataset_name,
            table_name=table_name,
            schema=schema
        )

def main():
    snapshotter = Snapshotter()
    snapshotter.retrieve_raw_snapshotted_data(SnapshottedResources.BUILDINGS)

if __name__=='__main__':
    main()
