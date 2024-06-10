import pandas as pd
import glob

file_list = glob.glob('/home/manish/dev/trading/bhavcopy/*.csv')
#Notice the * which acts as a wildcard.
#This will give you the path of all files with .csv extension in that folder


final_df = pd.DataFrame() #empty dataframe

for csv_file in file_list:
    df = pd.read_csv(csv_file)
    csv_file_name = csv_file.split('/')[-1]
    print(csv_file)
    print('Processing File : {}'.format(csv_file_name))
    df.columns = df.columns.str.replace(' ', '')
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
    df.set_index(['TIMESTAMP'], inplace=True)
    
    if 'Unnamed:13' in df.columns:
        df.drop(['Unnamed:13'], axis=1, inplace=True)
   
    df_trim = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    new_df = df_trim[df_trim['SERIES'].isin(['EQ'])]
    final_df = pd.concat([df, final_df]) # df, final_df) # final_df.concat(new_df)

# final_df.sort_index(inplace=True) #to sort by dates
final_df = final_df.sort_values(by='SYMBOL')


final_df.to_csv('/home/manish/dev/trading/bhavcopy_2024_data.csv')