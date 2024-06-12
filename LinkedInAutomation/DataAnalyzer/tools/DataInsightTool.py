from agency_swarm.tools import BaseTool
from pydantic import Field
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class DataInsightTool(BaseTool):
    """
    This tool extracts meaningful insights from the data, such as trends, patterns, and key information.
    It generates summary statistics, visualizations, and other forms of insights.
    """

    # Define the fields with descriptions using Pydantic Field
    data: str = Field(
        ..., description="The data to be analyzed, provided as a CSV string."
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

        # Generate summary statistics
        summary_stats = df.describe(include='all').to_string()

        # Generate visualizations
        visualizations = []

        # Example: Histogram of numerical columns
        for col in df.select_dtypes(include=[np.number]).columns:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[col], kde=True)
            plt.title(f'Histogram of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            visualizations.append(f'<img src="data:image/png;base64,{image_base64}" />')
            plt.close()

        # Example: Correlation heatmap
        plt.figure(figsize=(12, 8))
        corr = df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        visualizations.append(f'<img src="data:image/png;base64,{image_base64}" />')
        plt.close()

        # Example: Time series plot if 'date' column exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df.set_index('date', inplace=True)
            plt.figure(figsize=(12, 6))
            df.resample('M').mean().plot()
            plt.title('Time Series Plot')
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            visualizations.append(f'<img src="data:image/png;base64,{image_base64}" />')
            plt.close()

        # Combine summary statistics and visualizations into a single report
        report = f"<h1>Data Insights Report</h1><h2>Summary Statistics</h2><pre>{summary_stats}</pre><h2>Visualizations</h2>"
        report += ''.join(visualizations)

        return report

# Example usage:
# raw_data = "date,value\n2023-01-01,10\n2023-02-01,15\n2023-03-01,7\n"
# tool = DataInsightTool(data=raw_data)
# result = tool.run()
# print(result)