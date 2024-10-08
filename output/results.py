import pandas as pd

def write_results_to_excel(results, output_file):
    """Convert results to a pandas DataFrame and write the table to an Excel file."""
    df = _create_dataframe(results)
    df.to_excel(output_file, index=False)

def print_results(results):
    """Convert results to a pandas DataFrame and print the table."""
    df = _create_dataframe(results)
    if df.empty:
        print("No roles with permissions found on the RDS databases.")
    else:
        # Configure pandas to display the entire DataFrame without truncation
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print(df)

def _create_dataframe(results):
    """Create a pandas DataFrame."""
    return pd.DataFrame(results, columns=['service', 'resource', 'role', 'allowed_actions', 'description'])
