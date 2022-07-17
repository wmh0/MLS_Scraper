# -*- coding: utf-8 -*-
"""
Name: MLS_Scraper_Module
Description: Main script of converting MLS HTML into tabular format
Created on Fri Jul 15 14:47:22 2022
Update Date: 17/07/2022

@author: hinwm
"""
import argparse
from os.path import exists
from sys import exit
from MLS_scraper_module import MLS_Scraper_Module
from MLS_command_line_view import MLS_Command_Line_View

"""
Class: MLS_Scraper
"""

class MLS_Scraper:
    
    def __init__(self, args):
        """
        Initialize MLS Scraper module
        
        Parameters
        ----------
        args : namespace
            Input arguments of the program

        Returns
        -------
        None.

        """
        
        self.args = args
        
        # Initialize scraper module
        self.scraper = MLS_Scraper_Module()
        
        # Initialize command line view
        self.view = MLS_Command_Line_View()
        
        # Display initialization message
        self.view.initialization(self.args)
        
    def read_html(self):
        """
        Read the html file

        Returns
        -------
        None.

        """
        html_path = self.args.input
        
        if self.check_file_exist(html_path):
            self.view.read_html_view(self.scraper.read_html(html_path))
        else:
            self.view.error_file_not_exist(html_path)
            exit()
        
    def get_all_rental(self):
        """
        Scrap all rental information
        
        Returns
        -------
        None.
        
        """
        self.view.get_all_rental_view(self.scraper.get_all_rental())
        
    def scraping_summary(self):
        """
        Show scraping summary: Number of succeeded and failure MLS cases

        Returns
        -------
        None.

        """
        scraping_result = self.scraper.get_rental_scraping_status()
        self.view.scraping_summary_view(scraping_result)
        
    def output_rental_information(self):
        """
        Output the rental information as files

        Returns
        -------
        None.
        """
        output_path = self.args.output
        if self.check_file_exist(output_path):
            self.view.output_rental_information_view(
                self.scraper.output_rental_information(self.args.output,
                                                   self.args.tabular)
                )
        else:
            self.view.error_file_not_exist(output_path)
            exit()
        
        
    def ending(self):
        """
        Display the end of program
        
        Returns
        -------
        None.
        """
        self.view.ending()
        
    def check_file_exist(self, path):
        """
        Check if the file path exist

        Parameters
        ----------
        path : Str
            File path to check if it exists in the system.

        Returns
        -------
        Bool
            Whether the path exist in the system.

        """
        return exists(path)
        
def arguement_parsing():
    """
    Parse the input arguments

    Returns
    -------
    args : namespace
        input: path of MLS html file
        output: path of directory to save the rental attributes
        -t: Save the files as csv (default)
        -nt: Save the files as json, mutually exclusive to -t

    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input',
                        type=str,
                        help='Input file path of MLS html file')
    
    parser.add_argument('output',
                        type=str,
                        help='Output directory of scraped results')
    
    feature_parser  = parser.add_mutually_exclusive_group(required=False)
    feature_parser .add_argument('-t', '--tabular', dest = 'tabular', action='store_true', help="Save as csv format")
    feature_parser .add_argument('-nt', '--non_tabular', dest='tabular', action='store_false', help="Save as json format")
    parser.set_defaults(tabular=True)

    args = parser.parse_args()
    
    return args
    
        
def main():
    args = arguement_parsing()
    
    scraper = MLS_Scraper(args)

    # read in example html file
    scraper.read_html()
    
    # get the rental information
    scraper.get_all_rental()
    scraper.scraping_summary()
    
    # Output as desired format
    scraper.output_rental_information()
    
    scraper.ending()


if __name__ == "__main__":
    main()