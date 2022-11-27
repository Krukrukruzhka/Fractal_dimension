import pandas as pd

def parseData(filename: str):
    data = pd.read_csv(filename)
    data = data.iloc[:, :132]
    for counter in range(len(data)):
        with open(f'Кардиограммы\\{filename.split(".")[0]}_{counter + 1}.txt', 'w+') as file:
            file.writelines(list(map(lambda x: str(x) + '\n', list(data.iloc[counter]))))


parseData('Нормальные.csv')
parseData('Ненормальные.csv')