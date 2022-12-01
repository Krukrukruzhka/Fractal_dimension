# import pandas as pd
#
#
# class Loader(object):
#     @staticmethod
#     def parse_data(filename: str):
#         data = pd.read_csv(filename)
#         data = data.iloc[:40, :-1]
#         for counter in range(len(data)):
#             with open(f'Кардиограммы\\{filename.split(".")[0]}_{counter + 1}.txt', 'w+') as file:
#                 file.writelines(list(map(lambda x: str(x) + '\n', list(data.iloc[counter]))))
#
#
# Loader.parse_data('normal.csv')
# Loader.parse_data('abnormal.csv')
#
# # a = []
# # b = []
# # with open(f'Кардиограммы\\Dlya_Mishi.txt', 'r+') as file:
# #     a = file.readlines()
# # a = [x.split()[1].replace(',', '.')+'\n' for x in a]
# # with open(f'Кардиограммы\\file.txt', 'w+') as file:
# #     file.writelines(a)

