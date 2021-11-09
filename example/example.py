import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os


class CravatAnnotator(BaseAnnotator):

    def setup(self):
        """
        Set up data sources. 
        Cravat will automatically make a connection to 
        data/example_annotator.sqlite using the sqlite3 python module. The 
        sqlite3.Connection object is stored as self.dbconn, and the 
        sqlite3.Cursor object is stored as self.cursor.
        """
        pass

    def annotate(self, input_data, secondary_data=None, tertiary_data=None):
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref_base = input_data['ref_base']
        alt_base = input_data['alt_base']
        so = input_data['so']
        is_clinvar = 1

        # getting appropriate values from input data sources
        if secondary_data['gnomad'] is None:
            return None
        else:
            gnomad_arr = secondary_data['gnomad']
            gnomad_dict = gnomad_arr[0]
            global_af = gnomad_dict['af']

        if secondary_data['clinvar'] is None:
            is_clinvar = 0
        else:
            clinvar_arr = secondary_data['clinvar']
            clinvar_dict = clinvar_arr[0]
            clinvar_sig = clinvar_dict['sig']

        # Logic to handle gnomad/clinvar analysis of variants
        if is_clinvar == 1:
            if clinvar_sig == "Benign" or clinvar_sig == "Likely benign":
                classification = "Benign"
                reason = "clinvar"
            elif clinvar_sig == "Pathogenic" or clinvar_sig == "Likely pathogenic":
                classification = "Pathogenic"
                reason = "clinvar"
            elif global_af > .05:
                classification = "Benign"
                reason = "gnomad"
            elif so == 'FSD' or so == 'FSI' or so == 'INI' or so == 'IND' or so == 'STR' or so == 'STL' or so == 'STG' or so == 'SPL':
                classification = "Pathogenic"
                reason = "gnomad"
            else:
                classification = "VUS"
                reason = "gnomad"
            return {
                'classification': classification,
                'reason': reason
            }
        else:
            if global_af > .05:
                classification = "Benign"
                reason = "gnomad"
            elif so == 'FSD' or so == 'FSI' or so == 'INI' or so == 'IND' or so == 'STR' or so == 'STL' or so == 'STG' or so == 'SPL':
                classification = "Pathogenic"
                reason = "gnomad"
            else:
                classification = "VUS"
                reason = "gnomad"
            return {
                'classification': classification,
                'reason': reason
            }


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
