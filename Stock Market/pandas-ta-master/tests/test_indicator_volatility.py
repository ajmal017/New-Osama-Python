from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestVolatility(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data['open']
        cls.high = cls.data['high']
        cls.low = cls.data['low']
        cls.close = cls.data['close']
        if 'volume' in cls.data.columns: cls.volume = cls.data['volume']

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, 'volume'): del cls.volume
        del cls.data


    def setUp(self): pass
    def tearDown(self): pass
    

    def test_accbands(self):
        result = pandas_ta.accbands(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'ACCBANDS_20')

    def test_atr(self):
        result = pandas_ta.atr(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'ATR_14')

        try:
            expected = tal.ATR(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_bbands(self):
        result = pandas_ta.bbands(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'BBANDS_20')

        try:
            expected = tal.BBANDS(self.close)
            expecteddf = DataFrame({'BBL_20': expected[0], 'BBM_20': expected[1], 'BBU_20': expected[2]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError as ae:
            try:
                bbl_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,0], expecteddf.iloc[:,0], col=CORRELATION)
                self.assertGreater(bbl_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,0], CORRELATION, ex)

            try:
                bbm_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,1], expecteddf.iloc[:,1], col=CORRELATION)
                self.assertGreater(bbm_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,1], CORRELATION, ex, newline=False)

            try:
                bbu_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,2], expecteddf.iloc[:,2], col=CORRELATION)
                self.assertGreater(bbu_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,2], CORRELATION, ex, newline=False)

    def test_donchian(self):
        result = pandas_ta.donchian(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'DC_10_20')

        result = pandas_ta.donchian(self.close, lower_length=20, upper_length=5)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'DC_20_5')


    def test_kc(self):
        result = pandas_ta.kc(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'KC_20')

    def test_massi(self):
        result = pandas_ta.massi(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'MASSI_9_25')

    def test_natr(self):
        result = pandas_ta.natr(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'NATR_14')

        try:
            expected = tal.NATR(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_true_range(self):
        result = pandas_ta.true_range(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'TRUERANGE_1')

        try:
            expected = tal.TRANGE(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)