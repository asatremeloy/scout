#!/usr/bin/env python3

""" Tests for commercial microsegment data processing code """

# Import code to be tested
import com_mseg as cm

# Import needed packages
import unittest
import numpy as np


class PercentageCalculationTest(unittest.TestCase):
    """ Test function that converts service demand data from the EIA
    data file into percentages of the total reported energy use for the
    specified census division, building type, end use, and fuel type. """
    # Note that the service demand is only characterized for some end uses

    # Define lists that specify the census division, building type,
    # end use, and fuel type from which to select the desired data
    selection1 = [1, 3, 2, 1]  # New England, Food Sales, Cooling, Electricity
    selection2 = [4, 7, 6, 1]  # West North Central, Large Office, Lighting

    # Define a numpy array of sample service demand data, including a
    # limited number of year columns (compared to the actual service
    # demand data) for the sake of simplicity
    service_demand = np.array([
        (1, 3, 2, 1, 1, 13, 4, 0.28, 0.29, 0.37,
         'reciprocating_chiller 2013 mid-range', 4.4),
        (1, 3, 2, 1, 2, 13, 4, 0.0, 0.0, 0.01,
         'reciprocating_chiller 2013 mid-range', 4.4),
        (1, 3, 2, 1, 3, 13, 4, 0.02, 0.03, 0.04,
         'reciprocating_chiller 2013 mid-range', 4.4),
        (1, 3, 2, 1, 1, 52, 2, 0.18, 0.25, 0.27,
         'rooftop_AC 2012 installed base', 3.11),
        (1, 3, 2, 1, 2, 52, 2, 0.19, 0.19, 0.21,
         'rooftop_AC 2012 installed base', 3.11),
        (1, 3, 2, 1, 3, 52, 2, 0.0, 0.01, 0.01,
         'rooftop_AC 2012 installed base', 3.11),
        (1, 3, 2, 1, 1, 53, 5, 0.72, 0.15, 0.08,
         'wall-window_room_AC 2014 standard/ 2020 typi', 3.22),
        (1, 3, 2, 1, 2, 53, 5, 0.02, 0.05, 0.06,
         'wall-window_room_AC 2014 standard/ 2020 typi', 3.22),
        (1, 3, 2, 1, 3, 53, 5, 0.01, 0.03, 0.03,
         'wall-window_room_AC 2014 standard/ 2020 typi', 3.22),
        (4, 7, 6, 1, 1, 24, 7, 0.0, 0.0, 0.0,
         '100W incand 2003 installed base', 10.0),
        (4, 7, 6, 1, 2, 24, 7, 1.28, 1.35, 1.36,
         '100W incand 2003 installed base', 10.0),
        (4, 7, 6, 1, 3, 24, 7, 1.23, 1.18, 1.15,
         '100W incand 2003 installed base', 10.0),
        (4, 7, 6, 1, 1, 24, 7, 0.27, 0.26, 0.24,
         '23W CFL 2011 typical', 42.4),
        (4, 7, 6, 1, 2, 24, 7, 0.93, 0.91, 0.88,
         '23W CFL 2011 typical', 42.4),
        (4, 7, 6, 1, 3, 24, 7, 0.15, 0.14, 0.13,
         '23W CFL 2011 typical', 42.4),
        (4, 7, 6, 1, 1, 24, 14, 0.39, 0.43, 0.47,
         '90W Halogen Edison 2030 typical', 21.36),
        (4, 7, 6, 1, 2, 24, 14, 0.27, 0.27, 0.26,
         '90W Halogen Edison 2030 typical', 21.36),
        (4, 7, 6, 1, 3, 24, 14, 0.18, 0.19, 0.21,
         '90W Halogen Edison 2030 typical', 21.36),
        (4, 7, 6, 1, 1, 25, 7, 0.53, 0.55, 0.56,
         'F28T8 HE 2020 typical - 2012 stnd', 62.56),
        (4, 7, 6, 1, 2, 25, 7, 0.48, 0.43, 0.42,
         'F28T8 HE 2020 typical - 2012 stnd', 62.56),
        (4, 7, 6, 1, 3, 25, 7, 0.09, 0.13, 0.14,
         'F28T8 HE 2020 typical - 2012 stnd', 62.56)],
        dtype=[('r', '<i4'), ('b', '<i4'), ('s', '<i4'), ('f', '<i4'),
               ('d', '<i4'), ('t', '<i4'), ('v', '<i4'),
               ('2012', '<f8'), ('2013', '<f8'), ('2014', '<f8'),
               ('Description', '<U50'), ('Eff', '<f8')])
    # The columns specifying the census division, building type, etc.
    # in this sample array correctly match the description text, but
    # the data reported are fabricated and only for the purposes of
    # testing the calculations in the function

    # Define the anticipated outputs from the function based on the
    # inputs specified above
    selection1_technames = ['reciprocating_chiller',
                            'rooftop_AC',
                            'wall-window_room_AC']
    selection1_pct = np.array([[0.211267606, 0.32, 0.388888889],
                               [0.26056338, 0.45, 0.453703704],
                               [0.528169014, 0.23, 0.157407407]])

    selection2_technames = ['100W incand',
                            '23W CFL',
                            '90W Halogen Edison',
                            'F28T8 HE']
    selection2_pct = np.array([[0.432758621, 0.433219178, 0.431271478],
                               [0.232758621, 0.224315068, 0.214776632],
                               [0.144827586, 0.15239726, 0.161512027],
                               [0.189655172, 0.190068493, 0.192439863]])

    # Run both example selections with the service demand reprocessing
    # function and save outputs for testing
    def setUp(self):
        (self.a, self.b) = cm.sd_mseg_percent(
            self.service_demand, self.selection1)
        (self.c, self.d) = cm.sd_mseg_percent(
            self.service_demand, self.selection2)

    # Test technology type name capture/identification
    def test_service_demand_name_identification(self):
        self.assertEqual(self.b, self.selection1_technames)
        self.assertEqual(self.d, self.selection2_technames)

    # Test energy percentage contribution calculation (correcting for
    # potential floating point precision problems)
    def test_service_demand_percentage_conversion(self):
        self.assertTrue(
            (np.round(self.a - self.selection1_pct, decimals=5) == 0).all())
        self.assertTrue(
            (np.round(self.c - self.selection2_pct, decimals=5) == 0).all())


class StructuredArrayStringProcessingTest(unittest.TestCase):
    """ Test function that processes strings stored in a column of a
    structured array to eliminate extraneous spaces and double quotes. """

    # Define a test array with strings like those in the Description
    # column of KSDOUT (with double quotes and extraneous spaces
    # both inside and outside of the quotes)
    string_format1 = np.array([
        (' "appliance_name 2012 minimum                "', 5),
        (' "other_device-model 2019 design standard    "', 3),
        (' "final product-2010 w/price $50 cond applied"', 9)],
        dtype=[('Column Name', '<U60'), ('Other', '<i4')])

    # Define the corresponding array with the strings cleaned up
    string_format1_clean = np.array([
        ('appliance_name 2012 minimum', 5),
        ('other_device-model 2019 design standard', 3),
        ('final product-2010 w/price $50 cond applied', 9)],
        dtype=[('Column Name', '<U60'), ('Other', '<i4')])

    # Define a test array with strings like those in the Label column
    # of KDBOUT (without double quotes)
    string_format2 = np.array([
        (' GenerallyNoSpaces            ', 12),
        (' With Spaces Just In Case     ', 39),
        (' WithSome&pecial/Chars        ', 16)],
        dtype=[('The Column', '<U50'), ('Other', '<i4')])

    # Define the corresponding array with the strings cleaned up
    string_format2_clean = np.array([
        ('GenerallyNoSpaces', 12),
        ('With Spaces Just In Case', 39),
        ('WithSome&pecial/Chars', 16)],
        dtype=[('The Column', '<U50'), ('Other', '<i4')])

    # Test processing of strings that have double quotes
    def test_string_processing_with_double_quotes(self):
        self.assertCountEqual(
            cm.str_cleaner(self.string_format1, 'Column Name'),
            self.string_format1_clean)

    # Test processing of strings that only have extra spaces
    def test_string_processing_with_no_extraneous_quotes(self):
        self.assertCountEqual(
            cm.str_cleaner(self.string_format2, 'The Column'),
            self.string_format2_clean)


# Offer external code execution (include all lines below this point in all
# test files)
def main():
    # Triggers default behavior of running all test fixtures in the file
    unittest.main()

if __name__ == '__main__':
    main()
