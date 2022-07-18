# MLS_Scraper
Scraper to collect Multiple Listing Services output into organized manner

## Description
Multiple Listing Services (MLS) is a platform of real estate source used by agents to post and discover units that were under sale or lease for their customer's interest.

While the platform is rich in content, customers were mainly got access to the filtered site provided by real estate professionals, which were in report format and hard to navigate, to filter and to compare between different opportunities.

A tool is developed to convert the report into machine-readiable format, so to facilitate search and comparison by clients.

## Instruction
A sample website is provided as an example

1. Download the html file (To avoid any disruption to the platform, it is advised to perform the conversion on a downloaded website

2. In command line environment, run the executible file with the following input:
- input: Input path of the MLS html file
- output: Desired output directory location of the outcomes
- -t: Save the output as csv files (default)
- -nt: Save the output as json files (mutually exclusive with -t)

```
MLS_scraper.exe [-t | -nt] input output

positional arguments:
  input               Input file path of MLS html file
  output              Output directory of scraped results

optional arguments:
  -h, --help          show this help message and exit
  -t, --tabular       Save as csv format
  -nt, --non_tabular  Save as json format
```

Example:
```Batchfile
MLS_scraper.exe sample/input/Dummy_MLS_Website_html  sample/output -t
```

3. The tool will provided the number of succeeded and failed cases
	
4. Two files will be generated to the location advised in 'output' parameter

