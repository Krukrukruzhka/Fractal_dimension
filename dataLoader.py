import pandas as pd


class Loader(object):
    @staticmethod
    def parse_kardio(filename: str):
        data = pd.read_csv(filename)
        filename = filename.split("\\")[1]
        data = data.iloc[:30, :-1]
        for counter in range(len(data)):
            with open(f'Кардиограммы\\{filename.split(".")[0]}_{counter + 1}.txt', 'w+') as file:
                file.writelines(list(map(lambda x: str(x) + '\n', list(data.iloc[counter]))))


Loader.parse_kardio('src\\normal.csv')
Loader.parse_kardio('src\\abnormal.csv')
