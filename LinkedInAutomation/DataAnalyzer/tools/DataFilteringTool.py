from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
from datetime import datetime

class DataFilteringTool(BaseTool):
    """
    This tool filters the data to identify relevant posts based on specified criteria.
    It allows for filtering by keywords, date ranges, and other relevant parameters.
    """

    # Define the fields with descriptions using Pydantic Field
    data: str = Field(
        ..., description="The data to be filtered, provided as a CSV string."
    )
    keywords: str = Field(
        None, description="Comma-separated keywords to filter the posts."
    )
    start_date: str = Field(
        None, description="Start date for filtering posts (format: YYYY-MM-DD)."
    )
    end_date: str = Field(
        None, description="End date for filtering posts (format: YYYY-MM-DD)."
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

        # Filter by keywords
        if self.keywords:
            keywords_list = [kw.strip() for kw in self.keywords.split(',')]
            keyword_filter = df.apply(lambda row: any(kw in row.to_string() for kw in keywords_list), axis=1)
            df = df[keyword_filter]

        # Filter by date range
        if self.start_date or self.end_date:
            if 'date' not in df.columns:
                return "Error: 'date' column not found in the data."

            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            if self.start_date:
                start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
                df = df[df['date'] >= start_date]
            if self.end_date:
                end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
                df = df[df['date'] <= end_date]

        # Return the filtered data as a CSV string
        return df.to_csv(index=False)

# Example usage:
# raw_data = "date,content\n2023-01-01,This is a test post about AI.\n2023-02-01,Another post about machine learning.\n"
# tool = DataFilteringTool(data=raw_data, keywords="AI,machine learning", start_date="2023-01-01", end_date="2023-12-31")
# result = tool.run()
# print(result)