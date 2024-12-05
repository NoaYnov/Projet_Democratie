import pandas as pd

def load_data():
    vote_df = pd.read_csv('csv/data.csv', sep=';', encoding='utf-8' , skiprows=1, na_values='N/A',low_memory=False)
    return vote_df






def main():
    data = load_data()
    print(data.head())


if __name__ == '__main__':
    main()