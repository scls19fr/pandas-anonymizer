#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from faker import Factory

class Anonymizer(object):
    def __init__(self, locale):
        self._fake = Factory.create(locale)

    def seed(self, seed=None):
        """Calls faker.seed

        When using Anonymizer for unit testing, you will often want to generate the same data set. 
        The generator offers a seed() method, which seeds the random number generator. 
        Calling the same script twice with the same seed produces the same results.

        Parameters
        ----------
        seed : `int` or `str`
            None or no argument seeds from current time or from an operating
            system specific randomness source if available.

        Returns
        -------
        None
        """
        self._fake.seed(seed)

    def anonymize(self, data, columns=None):
        """Returns anonymized data

        Parameters
        ----------
        data : `pd.DataFrame`
            Pandas DataFrame to anonymize

        columns : `list`
            Columns to anonymize

        Returns
        -------
        `pd.DataFrame`
            Anonymized data

        """
        if columns is None:
            columns_to_anonyize = data.columns
        else:
            columns_to_anonyize = columns
        for colname in columns_to_anonyize:
            faker_func_name = colname.lower().replace(' ', '_')
            if hasattr(self._fake, faker_func_name) and colname in columns_to_anonyize:
                data = self._anonymize_dataframe(data, colname, faker_func_name=faker_func_name)
        return data

    def _anonymize_dataframe(self, df, colname, faker_func_name=None, f_anon=None):
        """Returns anonymized DataFrame

        Parameters
        ----------
        df : `pd.DataFrame`
            Pandas DataFrame to anonymize

        colname : `str`
            Name of column to anonymize

        faker_func_name : `str`
            Name of faker method to use to anonymize

        f_anon : `callable`
            Function method to use to anonymize

        Returns
        -------
        `pd.DataFrame`
            Anonymized DataFrame

        """

        ser = df[colname]
        ser_anon = self._anonymize_serie(ser, faker_func_name=faker_func_name)
        df[colname] = ser_anon
        return df

    def _anonymize_serie(self, ser, faker_func_name=None, f_anon=None):
        """Returns anonymized pd.Series
        ser : `pd.Series`
            Pandas Series to anonymize

        faker_func_name : `str`
            Name of faker method to use to anonymize

        f_anon : `callable`
            Function method to use to anonymize

        Returns
        -------
        `pd.Series`
            Anonymized Series

        """
        col_uniq = ser.unique()
        if f_anon is None:
            f_anon = lambda s: getattr(self._fake, faker_func_name)()
        print(col_uniq)
        d_anon, d_anon_reversed = self._d_anon(col_uniq, f_anon)
        print(d_anon)
        print(d_anon_reversed)
        ser_anon = ser.map(d_anon)
        return ser_anon


    def _d_anon(self, a, f_anon):
        """Returns a dict of anonymized data

        Parameters
        ----------
        a : `np.array`
            NumPy array to anonymize

        f_anon : `callable`
            function used to anonymize data

        Returns
        -------
        `np.array`
            Anonymized NumPy array

        """
        f_vct_anon = np.vectorize(f_anon)
        while True:
            a_anon = f_vct_anon(a)
            if len(a_anon) == len(np.unique(a_anon)):
                break
        d_anon = {val: a_anon[i] for i, val in enumerate(a)}
        d_anon_reversed = {a_anon[i]: val for i, val in enumerate(a)}
        return d_anon, d_anon_reversed
