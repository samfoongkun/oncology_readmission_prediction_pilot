import pandas as pd
import numpy as np
import yaml
import os

CFG = yaml.safe_load(open('/Users/lajikf/Desktop/Python/Projectone/configs/excel_ingest.yaml','r',encoding='utf-8'))
def get_readmission_patients(df, cancer_codes, days_threshold=30, cfg = CFG, emergency = 'all'):
    """
    Identify patients who were readmitted within time limits after chemotherapy.
    This function does NOT filter for chemotherapy procedure. Use orders to filter chemotherapy visit_sn.
    Args:
        df (pd.DataFrame): DataFrame containing patient admission data.
        cancer_codes (list): ICD-10 code of cancer included.
        days_threshold (int): Number of days to consider for readmission.
        emergency (str): Code indicating emergency readmission. all for all, Y for emergency only, N for non-emergency only.
    Returns:
        (readmit_visit_sn,first_admit_visit_sn) (tuple): Tuple of two lists. 
        readmit_patient is visit_sn readmitted within the threshold after chemotherapy.
        first_admit_visit_sn is visit_sn of the first admission.
        

    """
    ## Convert date columns to datetime
    print(f'Getting readmission patients with cancer-code{cancer_codes}')
    df['B12'] = pd.to_datetime(df['B12'], errors='coerce')
    df['B15'] = pd.to_datetime(df['B15'], errors='coerce')
    if df['B12'].isna().sum() > 0:
        print("Date type conversion error in B12:")
        print(df[df['B12'].isna()][['patient_id','visit_sn','B12']])
    else:
        if df['B15'].isna().sum() > 0:
            print("date type conversion error in B15:")
            print(df[df['B15'].isna()][['patient_id','visit_sn','B15']])
        else:
            print("Date type conversion successful!")
    # df = df[['visit_sn','patient_id','B12','B15','B11C','C03C']].copy() # check the list, which colmn to keep

    ## calculate next visit date to identify readmission
    df = df.sort_values(by=['patient_id','B12'])
    df['next_admit_date'] = df.groupby('patient_id')['B12'].shift(-1)
    # df['next_admit_type'] = df.groupby('patient_id')['B11C'].shift(-1)
    df['next_visit_sn'] = df.groupby('patient_id')['visit_sn'].shift(-1)
    df = df[df['next_admit_date'].notna()]
    df['days_to_next_admit'] = df['next_admit_date'] - df['B15']
    df = df[df['days_to_next_admit'].dt.days < days_threshold]
    # df = df[df['C03C'].str.contains('|'.join(cancer_codes))] # filter cancer diagnosis
    if emergency == 'all':
        print(f'Total readmission patients in {days_threshold} days with cancer diag: {df["patient_id"].nunique()}\nTotal readmission visits in {days_threshold} days with cancer diag: {df["visit_sn"].nunique()}\n')
    elif emergency == 'Y':
        df = df[df['next_admit_type'] == '1']
        print(f'Total readmission EMERGENCY patients in {days_threshold} days with cancer diag: {df["patient_id"].nunique()}\nTotal readmission EMERGENCY visit in {days_threshold} days with cancer diag: {df["visit_sn"].nunique()}\n')
    elif emergency == 'N':
        df = df[df['next_admit_type'] != '1']
        print(f'Total readmission NON-EMERGENCY patients in {days_threshold} days with cancer diag: {df["patient_id"].nunique()}\nTotal readmission NON-EMERGENCY visits in {days_threshold} days with cancer diag: {df["visit_sn"].nunique()}\n')
    readmit_visit_sn_list = df['next_visit_sn'].unique().tolist()
    first_admit_patient_list = df['visit_sn'].unique().tolist()
    return list(zip(readmit_visit_sn_list, first_admit_patient_list)), readmit_visit_sn_list, first_admit_patient_list

def read_concat(time_frame,folder,file_name,features=None):
    '''
    Read and concat the same type of files from a range of different months.
    Example: In 'data/202401/data.xlsx' time_frame = ['202401'], folder = 'data', file_name = 'data.xlsx'
    Args:
    time_frame(list): YYYYMM(str) month list to read and concat
    folder(str): Base folder to read the file
    file_name(str): The file name that need to be proceed
    features(list): A list of features that you want to keep in the concat file
    Return:
    concat_df: A pd dataframe that concat all of the files
    '''
    concat_file = pd.DataFrame()
    count = 0
    for mon in time_frame:
        f = folder+'/'+mon+'/'+file_name
        print(f'Now reading{mon} {file_name}...')
        temp_file = pd.read_excel(f)
        if features:
            temp_file = temp_file[features]
        print(f'There are {len(temp_file)} entries in {mon} {file_name}')
        count = count + len(temp_file)
        if mon == time_frame[0]:
            concat_file = temp_file
        else:
            concat_file = pd.concat([concat_file,temp_file])
    print(f'Finished reading and concating files. There are {count} entries included!')
    return concat_file