===============================
leiden_sc
===============================

.. image:: https://badge.fury.io/py/leiden_sc.png
    :target: http://badge.fury.io/py/leiden_sc
    
.. image:: https://travis-ci.org/andrewhill157/leiden_sc.png?branch=master
        :target: https://travis-ci.org/andrewhill157/leiden_sc

.. image:: https://pypip.in/d/leiden_sc/badge.png
        :target: https://crate.io/packages/leiden_sc?version=latest


Tools for extracting, remapping, and validating variants from Leiden Open Variation Database Installations.

* Free software: BSD license
* Documentation: http://leiden_sc.rtfd.org. (Not Complete)

# Modules

This project contains a number of number of modules within leiden_sc/:

## lovd

### macarthur_core/lovd/leiden_database.py:

These classes allow a user to extract tables of data (mutations listed for a specific gene in the database) and other useful information from any Leiden Open Variation Database installation, such as http://www.dmd.nl/nmdb2/. Unfortunately, it has been necessary to do this by downloading the HTML for relevant pages on the database and parsing out the necessary data, as they do not have an easy way to access the data otherwise. Therefore, I have added an external dependency - beautifulsoup4 - for HTML parsing. 

Basically, the usage for these classes goes like this:
```
leiden_url = 'http://www.dmd.nl/nmdb2/'
gene_id = 'ACTA1'

database = make_leiden_database(leiden_url)
database.set_gene_id(gene_id)
column_labels = leiden_database.get_table_headers()
table_entries = leiden_database.get_table_data()
...
```
Note that make_leiden_database acts as a factory method to generate the right subclass of LeidenDatabase for the detected version number. 

### macarthur_core/lovd/utilities.py:

These are general utility functions, some of which are used in leiden_database.py. 

## remapping

### macarthur_core/remapping/remapping.py

Genetic mutations are often listed in one of two formats, HGVS and VCF. HGVS is compact and has its own (relatively complex) syntax for describing mutations. However, for large scale analysis projects HGVS is extremely difficult to use effectively for a number of reasons. We are interested in converting data from the Leiden Open Variation Databases from one format to the other. This is a non-trivial conversion. 

The class ```VariantRemapper``` in ```macarthur_core/remapping/remapping.py``` wraps a third party module (hgvs) to make it easier to use within this project. The third party module documentation and description HGVS vs. VCF notation is described here: https://github.com/counsyl/hgvs

Unfortunately, the third-party tool depends on two relatively large files that I cannot easily host on github. These are normally housed in a folder called resources within the module. One is a human genome reference sequence (```macarthur_core/remapping/resources/hg19.fa```) and the other is a file containing definitions of transcript sequences that are needed to facilitate conversion between the HGVS and VCF 
(```macarthur_core/remapping/resources/genes.refSeq```). These two files are hosted at: http://www.broadinstitute.org/~ahill. Note that the files will need to decompressed using gunzip and placed in ```macarthur_core/remapping/resources/```. The first time these functions are used, two additional files will be generated (takes some time). Subsequent runs will not require this process to be repeated. 

# Scripts

I have included several scripts that I use to extract, remap, and validate data from LOVD databases. 

## extract_data.py
This is a script that I use in my overall project that makes use of the macarthur_core/lovd and macarthur_core/web_io to extract data from all data from a given LOVD URL. 

The script makes use of argparse to provide a user interface. The string provided for the command-line interface should hopefully provide an explanation of how it is used. It should save a tab-delimited file for each gene's table data, where each output file is named according to the gene name.

From command line generally it is used in the following way:
```
python extract_data.py --all --leiden_url http://www.dmd.nl/nmdb2/ --output_directory results
```
Users can also print a list of all available genes using:
```
python extract_data.py --genes_available --leiden_url http://www.dmd.nl/nmdb2/
```

