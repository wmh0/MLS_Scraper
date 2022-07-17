# -*- coding: utf-8 -*-
"""
Name: MLS_Scraper_Module
Description: Core module of converting MLS HTML into tabular format
Created on Sun May 29 12:05:25 2022
Update Date: 15/07/2022

@author: hinwm
"""

from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import json

"""
Class: MLS_Scraper_Module
"""


class MLS_Scraper_Module:

    def __init__(self):
        """
        Initialize MLS Scraper module

        Returns
        -------
        None.

        """

        # initialize parameters

        # Variable name of the address
        self.address_variable = ['Street Number',
                                 'Unit Number',
                                 'City',
                                 'Province',
                                 'Postal Code']

        # Variable name of the room table
        self.room_attribute_variable = ['Room Index',
                                        'Room',
                                        'Level',
                                        'Length',
                                        'Width',
                                        'Description 1',
                                        'Description 2',
                                        'Description 3']

        # Saving the succeeded and failed trail
        self.scrap_MLS_number = {'success': [],
                                 'failure': []}

    def read_html(self, html_path):
        """
        Read the MLS information in html format.

        Parameters
        ----------
        html_path : String
            Path of the MLS html.

        Returns
        -------
        None.

        """

        # Save the html and create a beautiful soup parser
        self.html_path = html_path

        with open(self.html_path, errors="ignore") as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        # pick up information that is related to the rentals
        self.MLS_info = soup.find_all("div",
                                      {"class": re.compile("^link-item status-")})

    def get_all_rental(self):
        """
        Scrap and tidy information of all the rental

        Returns
        -------
        None.

        """

        # Dictionary to store unit attributes and room attributes
        MLS_unit_attrs_dict = {}
        MLS_room_dict = {}

        for MLS_info_section in self.MLS_info:

            # Get the MLS number
            MLS_num = self.get_MLS_number(MLS_info_section)

            try:
                # Read the unit and room attributes from the section
                attribute_dict, room_table = self.get_rental_information(
                    MLS_info_section)
                MLS_unit_attrs_dict[MLS_num] = attribute_dict
                MLS_room_dict[MLS_num] = room_table
                self.scrap_MLS_number['success'].append(MLS_num)
            except:
                # If there is issue, prompt the user and record the failed MLS
                #print(
                #    f'Warning: information of MLS#:{MLS_num} cannot be found')
                self.scrap_MLS_number['failure'].append(MLS_num)

        self.MLS_dict = {
            'MLS_unit_attrs_dict': MLS_unit_attrs_dict,
            'MLS_room_dict': MLS_room_dict}
        
    def get_rental_scraping_status(self):
        """
        Return the MLS number of record that is success or failure

        Returns
        -------
        scrap_MLS_number : Dict
            Dictionary of MLS number of succeeded and failed records.

        """
        return self.scrap_MLS_number
        
        

    def output_rental_information(self, directory=None, as_df=False):
        """
        Return or save all the rental information

        Parameters
        ----------
        directory : Str, optional
            Directory of the output to be saved.
            Unit attributes and room attributes will be saved in specific folder.
            If it is None, attributes will be return in the program instead.
            The default is None.
            
        as_df : Bool, optional
            Whether the table should be return as tabular format.
            if as_df is True, return pandas dataframe or save as csv
            if as_df is False, return dictionary or save as json
            The default is False.

        Returns
        -------
        MLS_output : Dict
            MLS_output will be returned only if directory is None.
            If as_df is True, return a dictionary of dataframes
            If as_df is False, return a dictionary of dictionary

        """

        if as_df:
            MLS_output = self._convert_output_to_dataframe()
        else:
            MLS_output = self.MLS_dict

        if directory is None:
            return MLS_output
        else:
            for file_name, file in MLS_output.items():
                if as_df:
                    file_path = os.path.join(directory, file_name + '.csv')
                    file.to_csv(file_path)
                else:
                    file_path = os.path.join(directory, file_name + '.json')
                    with open(file_path, 'w') as fp:
                        json.dump(file, fp)

    def _convert_output_to_dataframe(self):
        """
        Convert all internal output from dictionary to pandas dataframe
        
        Returns
        -------
        Dict
            MLS_unit_attrs_df: Dataframe of unit attributes
            MLS_room_df: Dataframe of room attributes
        """

        # Convert unit attribute dictionary into dataframe
        unit_attrs_df = self._convert_unit_attrs_to_dataframe(
            self.MLS_dict['MLS_unit_attrs_dict'])

        # Convert room attribute dictionary into dataframe
        room_df = self._convert_room_attrs_to_dataframe(
            self.MLS_dict['MLS_room_dict'])

        return {'MLS_unit_attrs_df': unit_attrs_df, 'MLS_room_df': room_df}

    def _convert_unit_attrs_to_dataframe(self, unit_attrs_dict):
        """
        Convert unit attributes from dictionary to pandas dataframe
        
        Parameters
        ----------
        unit_attrs_dict : Dict
            Dictionary of unit attributes.
        
        Returns
        -------
        unit_attrs_df : pandas dataframe
            Dataframe of unit attributes
        """

        unit_attrs_df = pd.DataFrame.from_dict(unit_attrs_dict, orient='index')

        return unit_attrs_df

    def _convert_room_attrs_to_dataframe(self, room_dict):
        """
        Convert room attributes from dictionary to pandas dataframe
        
        Parameters
        ----------
        room_dict : Dict
            Dictionary of room attributes.
        
        Returns
        -------
        room_df : pandas dataframe
            Dataframe of room attributes
        """

        room_df_dict = {}

        for MLS_num, table_dict in room_dict.items():
            room_df_dict[MLS_num] = pd.DataFrame.from_dict(
                table_dict, orient='index')
            room_df_dict[MLS_num] = room_df_dict[MLS_num].reset_index().rename(columns={
                'index': 'Room Index'})
        room_df = pd.concat(room_df_dict).droplevel(1)

        return room_df

    def get_rental_information(self, MLS_info_section):
        """
        Get rental information from a specific MLS information section

        Parameters
        ----------
        MLS_info_section : bs4.element.Tag
            Html text of a particular MLS information section.

        Returns
        -------
        attribute_dict : Dict
            Unit attributes of rental.
        room_table : Dict
            Room attributes of rental.

        """

        # get the address of rental
        attribute_dict = self.get_rental_address(MLS_info_section)

        # get the rental attribute (without room information)
        attribute_dict.update(self.get_rental_attribute(MLS_info_section))

        # get the room information
        room_table = self.get_rental_room_information(MLS_info_section)

        return attribute_dict, room_table

    def get_MLS_number(self, MLS_info_section):
        """
        Get the MLS number from a specific MLS information section
        
        Parameters
        ----------
        MLS_info_section : bs4.element.Tag
            Html text of a particular MLS information section.

        Returns
        -------
        id : str
            MLS number of the rental
        """

        # Find the MLS number from the section
        return MLS_info_section.attrs['id']

    # Function to scrap an individual rental address
    def get_rental_address(self, MLS_info_section):
        """
        Get the address from a specific MLS information section
        
        Parameters
        ----------
        MLS_info_section : bs4.element.Tag
            Html text of a particular MLS information section.

        Returns
        -------
        attribute_dict : Dict
            Dictionary of rental address
            
        """

        attribute_dict = {}

        for lab in MLS_info_section.find_all("div", {"class": "formitem formgroup vertical",
                                                     "style": "width:325px"}):

            # find all text in bold - they are the address
            location_query = lab.find_all("span", {"class": "value",
                                                   "style": "font-weight:bold"})

            # save the address attribute
            for count, value in enumerate(self.address_variable):
                attribute_dict[value] = location_query[count].text

        return attribute_dict

    # Function to scrap an individual rental attribute
    def get_rental_attribute(self, MLS_info_section):
        """
        Get the unit attributes from a specific MLS information section
        
        Parameters
        ----------
        MLS_info_section : bs4.element.Tag
            Html text of a particular MLS information section.

        Returns
        -------
        attribute_dict : Dict
            Dictionary of unit attributes
            
        """

        attribute_dict = {}

        # rental attribute
        for table in MLS_info_section.find_all("div", {"class": re.compile("^formitem formgroup"),
                                                       "style": re.compile("^width:\d+[px|\%]")}):
            attribute_dict.update(self._get_label_value_pair(table))

        # rental remarks
        for table in MLS_info_section.find_all("div", {"class": "formitem formgroup vertical"})[-2:]:
            attribute_dict.update(self._get_label_value_pair(table))

        return attribute_dict

    def _get_label_value_pair(self, value_table):
        """
        Scrap the information in form of label-value pairs

        Parameters
        ----------
        value_table : bs4.element.Tag
            Html text of values with label tag.

        Returns
        -------
        attribute_dict : Dict
            Dictionary of attributes.

        """

        attribute_dict = {}

        # for all label value pairs, get the label and the associated value
        for lab in value_table.find_all("label"):
            label = lab.text[:-1]   # remove the colon
            attribute_dict[label] = lab.find_next_sibling().text

        return attribute_dict

    def get_rental_room_information(self, MLS_info_section):
        """
        Get the room attributes from a specific MLS information section
        
        Parameters
        ----------
        MLS_info_section : bs4.element.Tag
            Html text of a particular MLS information section.

        Returns
        -------
        room_dict : dict
            Dictionary of room attributes
            
        """

        # get number of rooms
        number_of_room = self._get_rental_number_of_room(MLS_info_section)

        # Start scrapping
        room_dict = {}
        for row in MLS_info_section.find_all("div",
                                             {"class": "formitem formgroup horizontal"})[(-2 - number_of_room + 1):-1]:

            room_query = row.find_all("span", {"class": "value"})
            idx = room_query[0].text
            room_dict[idx] = {}
            for count, value in enumerate(self.room_attribute_variable):
                if count == 0:
                    idx = room_query[count].text
                    continue
                room_dict[idx][value] = room_query[count].text

        return room_dict

    def _get_rental_number_of_room(self, MLS_info_section):
        """
        Get the number of rooms of a unit

        Parameters
        ----------
        MLS_info_section : bs4.element.Tag
            Html text of a particular MLS information section.

        Returns
        -------
        int
            Number of rooms.

        """

        # Find the last row of room table
        last_room_row = MLS_info_section.find_all(
            "div", {"class": "formitem formgroup horizontal"})[-2]
        last_room_index = last_room_row.find("span", {"class": "value"}).text

        return int(last_room_index)



