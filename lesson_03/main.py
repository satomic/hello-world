# coding=utf-8

import data_reader

peoples = data_reader.reader_csv("samples/data.csv", sep='\t')
print(peoples)

age_mean = peoples["age"].mean()
print(age_mean)

print(peoples["Saturday"])

peoples["holiday_sum"] = peoples.apply(lambda people: people["Saturday"] + people["Sunday"], axis=1)
print(peoples)

peoples.to_excel("output/new.xlsx", sheet_name="peoples")





















