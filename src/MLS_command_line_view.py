# -*- coding: utf-8 -*-
"""
Name: MLS_command_line_view
Description: Command line view of MLS Scraper
Created on Fri Jul 15 15:25:19 2022
Update Date: 17/07/2022

@author: hinwm
"""

"""
Class: MLS_Command_Line_View
"""

class MLS_Command_Line_View:
    
    def __init__(self):
        """
        Initialize command line view

        Returns
        -------
        None.

        """
        self.param_alias = {'input': 'Input file path',
                            'output': 'Output directory',
                            'tabular': 'Output as tabular format'}
        
    def initialization(self, args):
        """
        Display of MLS scraper initialization

        Parameters
        ----------
        args : namespace
            Namespace of parsed arguments.

        Returns
        -------
        None.

        """
    
        self._print_heading()
        print("Initializing...")
        self._print_parameters(args)
        print("")
        
    
    def _print_heading(self):
        """
        Internal function to print the heading
        
        Returns
        -------
        None.
        """
        heading =["===========",
                  "MLS Scraper",
                  "===========",
                  ""]
        print('\n'.join(heading))
        
    def _print_parameters(self, args):
        """
        Initial function to print the list of parameters

        Parameters
        ----------
        args : namespace
            Namespace of parsed arguments.

        Returns
        -------
        None.

        """
        
        for param, value in args.__dict__.items():
            if value is not None:
                print(f"{self.param_alias[param]}: {value}")
                
    def read_html_view(self, func):
        """
        Decorator to display information in the view during read_html()

        Parameters
        ----------
        func : function
            read_html() function of MLS_scraper.

        Returns
        -------
        wrapper : function
            read_html() function with command line view display.

        """
        
        def wrapper():
            print(f"Reading MLS website from {self.param_alias['input']}...")
            try:
                func
                print("MLS website is loaded successfully")
            except:
                print("Issue arised in loading MLS website")
                print("Please check if it is in valid format")
            print("")
                
        return wrapper()
    
    def error_file_not_exist(self, path):
        """
        Display error message when file does not exist

        Parameters
        ----------
        path : Str
            File path that does not exist.

        Returns
        -------
        None.

        """
        print(f"Error: {path} does not exist")
        print("Please check if the path is correct")
        print("")
        
    def get_all_rental_view(self, func):
        """
        Decorator to display information in the view during get_all_rental()

        Parameters
        ----------
        func : function
            get_all_rental() function of MLS_scraper.

        Returns
        -------
        wrapper : function
            get_all_rental() function with command line view display.

        """
        
        def wrapper():
            print("Scraping rental information from website...")
            try:
                func
                print("Rental information is collected")
            except:
                print("Issue arised in scraping")
                print("Please check if it is in valid format")
            print("")
                
        return wrapper()
        
    def scraping_summary_view(self, scraping_result):
        """
        Display summary of success and failure cases

        Parameters
        ----------
        scraping_result : Dict
            Dictionary of success and failure cases from MLS_scraper.

        Returns
        -------
        None.

        """
        
        print("Summary:")
        print(f"Succeed: {len(scraping_result['success'])}")
        print(f"Failure: {len(scraping_result['failure'])}")
        print("")
        
    def output_rental_information_view(self, func):
        """
        Decorator to display information in the view
        during output_rental_information()

        Parameters
        ----------
        func : function
            output_rental_information() function of MLS_scraper.

        Returns
        -------
        wrapper : function
            output_rental_information() function with command line view display.

        """
        
        def wrapper():
            print("Output rental information to {self.param_alias['output']}...")
            try:
                func
                print("Unit and room attributes were saved")
            except:
                print("Issue arised in scraping")
                print("Please check the directory of file output")
            print("")
        
    def ending(self):
        """
        Display ending message

        Returns
        -------
        None.

        """
        
        print("MLS website information were collected")
        print("Feel free to browse the output with spreadsheet software")