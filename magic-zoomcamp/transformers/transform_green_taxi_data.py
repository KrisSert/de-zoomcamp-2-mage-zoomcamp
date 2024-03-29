import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def cols_to_snake(data: pd.DataFrame) -> None:
    # Function to convert Camel Case to Snake Case
    def camel_mixed_to_snake(column_name):
        result = ''
        for i, char in enumerate(column_name):
            if i > 0 and char.isupper() and not column_name[i - 1].isupper():
                result += '_'
            result += char.lower()
        return result

    original_column_names = data.columns.tolist()
    data.rename(columns=lambda x: camel_mixed_to_snake(x), inplace=True)
    new_column_names = data.columns.tolist()
    for index, (old_col_name, new_col_name) in enumerate(zip(original_column_names, new_column_names)):
        if old_col_name != new_col_name:
            print(f'Renamed {old_col_name} to snake case: {new_col_name}')


# compare 2 dataframes and get the nr of col names that are different in them
def find_nr_of_different_col_names(df1, df2) -> int:
    different_columns = set(df1.columns).symmetric_difference(set(df2.columns))
    return len(different_columns)

@transformer
def transform(data, *args, **kwargs):
    
    # remove rows w (passenger_count=0 OR trip_distance=0)
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    # create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # print out the unique value_ids 
    uniques = data['VendorID'].unique().astype(str)
    print(f'Unique ValueID list: {uniques}')

    # rename columns to snakecase
    cols_to_snake(data)

    uniques_dates = data['lpep_pickup_date'].unique()
    print(len(uniques_dates))

    desired_dates = [pd.to_datetime('2009-01-01'), pd.to_datetime('2021-01-01')]
    print(data[data['lpep_pickup_date'].isin(desired_dates)])


    return data


@test
def test_output(output, *args) -> None:
    #vendor_id is one of the existing values in the column (currently)
    assert 'vendor_id' in output.columns, 'There is no column "vendor_id" in the dataset'

@test
def test_output(output, *args) -> None:
    #passenger_count is greater than 0  
    w_passenger_cnt_greater_thn_zero = output[output['passenger_count'] > 0]
    assert output.equals(w_passenger_cnt_greater_thn_zero), 'There are rows with "passenger_count" <= 0 in the dataset'

@test
def test_output(output, *args) -> None:
    #trip_distance is greater than 0  
    w_trip_distance_cnt_greater_thn_zero = output[output['trip_distance'] > 0]
    assert output.equals(w_trip_distance_cnt_greater_thn_zero), 'There are rows with "trip_distance" <= 0 in the dataset'
