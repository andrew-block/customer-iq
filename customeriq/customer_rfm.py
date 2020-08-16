import pandas as pd
from datetime import timedelta


class CustomerRFM:


    def convert_to_dataframe(self, filename, customer, date, trans_id, value):
        """
        :param filename:
        :param customer: Name of field which indicates the customer
        :param date: Name of field which indicates the date (Recency)
        :param trans_id: Name of field which indicates the id of the transaction (Frequency)
        :param value: Name of field which indicates the value (Monetary)
        :return:
        """
        period = 365
        quintiles = {}

        if 'csv' in filename.partition('.')[2]:
            df = pd.read_csv(filename, parse_dates=[date])
            df = df.dropna(subset=[customer])
            orders = df.groupby([trans_id, date, customer]).agg({value: lambda x: x.sum()}).reset_index()
            NOW = orders[date].max() + timedelta(days=1)
            orders['DaysSinceOrder'] = orders[date].apply(lambda x: (NOW - x).days)

            aggr = {
                # the number of days since last order (Recency)
                'DaysSinceOrder': lambda x: x.min(),
                # the total number of orders in the last period (Frequency)
                F"{date}": lambda x: len([d for d in x if d >= NOW - timedelta(days=period)]),
            }

            rfm = orders.groupby(customer).agg(aggr).reset_index()
            rfm.rename(columns={'DaysSinceOrder': 'Recency', F"{date}": 'Frequency'}, inplace=True)
            rfm['Monetary'] = rfm[F"{customer}"].apply(lambda x: orders[(orders[F"{customer}"] == x) & \
                            (orders[F"{date}"] >= NOW - timedelta(days=period))][F"{value}"].sum())

            return rfm

        if 'xls' in filename.partition('.')[2]:
            df = pd.read_excel(filename, parse_dates=[date])
            df = df.dropna(subset=[customer])
            orders = df.groupby([trans_id, date, customer]).agg({value: lambda x: x.sum()}).reset_index()
            NOW = orders[date].max() + timedelta(days=1)
            orders['DaysSinceOrder'] = orders[date].apply(lambda x: (NOW - x).days)

            aggr = {
                # the number of days since last order (Recency)
                'DaysSinceOrder': lambda x: x.min(),
                # the total number of orders in the last period (Frequency)
                F"{date}": lambda x: len([d for d in x if d >= NOW - timedelta(days=period)]),
            }

            rfm = orders.groupby(customer).agg(aggr).reset_index()
            rfm.rename(columns={'DaysSinceOrder': 'Recency', F"{date}": 'Frequency'}, inplace=True)
            rfm['Monetary'] = rfm[F"{customer}"].apply(lambda x: orders[(orders[F"{customer}"] == x) & \
                                                                        (orders[F"{date}"] >= NOW - timedelta(days=period))][F"{value}"].sum())

            return rfm

        else:
            'Please use a csv or xls file type'
