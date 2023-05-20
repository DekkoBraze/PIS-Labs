import django.db.models
from django.db import models

import pandas


class Currency(models.Model):
    charCode = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    value = models.FloatField()

    @staticmethod
    def create_data():
        url = "http://www.cbr.ru/scripts/XML_daily.asp"

        df = pandas.read_xml(url, encoding='cp1251')

        for i in range(len(df['Value'])):
            df['Value'][i] = str(df['Value'][i]).replace(',', '.')

        model_instances = [Currency(
            charCode=df.iloc[i]['CharCode'],
            name=df.iloc[i]['Name'],
            value=float(df.iloc[i]['Value'])
        ) for i in range(len(df))]

        Currency.objects.bulk_create(model_instances)
