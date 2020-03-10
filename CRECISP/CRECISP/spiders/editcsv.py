if __name__ == 'MAIN':
    import pandas as pd

    processed = pd.read_csv('CRECISP\creci_det.csv', encoding='UTF-8')
    total = pd.read_csv('CRECISP\crecisp.csv',  encoding='UTF-8')
    processed_list = [item.strip() for item in processed['CRECI']]
    data_to_drop = total.loc[total['CRECI'].isin(processed_list)]

    data_to_process = total.drop(data_to_drop.index)

    data_to_process.to_csv('dat_to_process.csv')

