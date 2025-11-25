import pandas as pd

df = pd.read_csv('etl/processed/processed_data.csv')

print('Total rows:', len(df))
print('\nDate column type:', df['Date'].dtype)
print('\nUnique dates:', df['Date'].nunique())
print('\nDate range:', df['Date'].min(), 'to', df['Date'].max())
print('\nRows per date (first 10):')
print(df['Date'].value_counts().sort_index().head(10))
print('\nSample data:')
print(df.head(10))
