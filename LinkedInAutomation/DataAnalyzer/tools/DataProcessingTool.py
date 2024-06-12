from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import numpy as np

class DataProcessingTool(BaseTool):
    """
    This tool utilizes data analysis libraries such as Pandas and NumPy to process the scraped data.
    It can load the data, clean it, and prepare it for further analysis.
    """

    # Define the fields with descriptions using Pydantic Field
    data: str = Field(
        ..., description="The raw data to be processed, provided as a CSV string."
    )

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform the task.
        """
        # Load the data into a Pandas DataFrame
        from io import StringIO
        data_io = StringIO(self.data)
        df = pd.read_csv(data_io)

        # Clean the data
        # Example: Remove rows with missing values
        df_cleaned = df.dropna()

        # Example: Convert columns to appropriate data types
        for col in df_cleaned.select_dtypes(include=['object']).columns:
            df_cleaned[col] = df_cleaned[col].astype(str)
        for col in df_cleaned.select_dtypes(include=['int', 'float']).columns:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

        # Example: Handle outliers
        for col in df_cleaned.select_dtypes(include=[np.number]).columns:
            df_cleaned[col] = np.where(
                (df_cleaned[col] - df_cleaned[col].mean()).abs() > 3 * df_cleaned[col].std(),
                df_cleaned[col].median(),
                df_cleaned[col]
            )

        # Prepare the data for further analysis
        # Example: Normalize numerical columns
        df_normalized = df_cleaned.copy()
        for col in df_normalized.select_dtypes(include=[np.number]).columns:
            df_normalized[col] = (df_normalized[col] - df_normalized[col].mean()) / df_normalized[col].std()

        # Return the processed data as a CSV string
        return df_normalized.to_csv(index=False)

# Example usage:
# raw_data = "column1,column2,column3\n1,2,3\n4,5,6\n7,8,9\n"
# tool = DataProcessingTool(data=raw_data)
# result = tool.run()
# print(result)