#!/usr/bin/env python
"""
Andrew Hill
MacArthur Lab - 2014

General utility functions for working with data.
"""

import re


def get_pmid(link_url):
    """
    Given a URL to a publication listed on PUBMED, return a string containing the PUBMED ID of the publication.

    @param link_url: URL to the publication on PUBMED. Assumed to be a valid link to a publication on PUBMED.
    For example, U(http://www.ncbi.nlm.nih.gov/pubmed/19562689) is a valid pubmed publication URL. The url must
    contain the PMID in the URL (19562689 in the example here) and contain no other 4 digit or longer numbers.
    @type link_url: string
    @return: PUBMED ID associated with link_url (as specified by the N digit ID included in PUBMED URLs).
    @rtype: string
    @raise: ValueError if there is no 4+ digit number in link_url
    """

    # Search for sequences of digits that are four digits or longer in length.
    m = re.compile('\d{4,}')
    results = m.search(link_url)

    # Return entire matched sequence (PMID)
    if results is not None:
        return results.group()
    else:
        raise ValueError('Input URL did not contain 4+ digit number.')


def get_omimid(link_url):
    """
    Given a URL to an entry on OMIM, return a string containing the OMIM ID for the entry.

    @param link_url: URL to the entry on OMIM. Assumed to be a valid link to an entry on PUBMED.
    For example, U(http://www.omim.org/entry/102610#0003) is a valid link to an OMIM entry on the ACTA1 gene.
    The url must contain the gene ID followed by the entry number in the URL separated by a hash mark
    (such as, 102610#0003 in the example URL). URL may not contain other instances of this pattern.
    @type link_url: string
    @return: OMIM entry associated with the URL. This consists of the gene ID (such as 102610 for ACTA1 and a
    specific entry number (0003) separated by a hash mark (102610#0003 in the example above).
    @rtype: string
    @raise: Value Error if link does not contain a valid OMIM ID.
    """

    # Search for sequences of digits separated only by a hash mark
    m = re.compile('\d+#\d+')
    results = m.search(link_url)

    # Return entire matched sequence (OMIM ID)
    if results is not None:
        return results.group()
    else:
        raise ValueError('Input URL did not contain valid OMIM ID.')


def remove_times_reported(hgvs_notation):
    """
    Removes (Reported N times)substring from input if exists. Comparison is not case sensitive.

    @param hgvs_notation: String, typically an entry in the DNA Change column in table_data for a given variant on
    an lovd installation.
    @type hgvs_notation: string
    @return: hgvs_notation with instances of (Reported N times) removed. Whitespace surrounding this substring is
    removed in returned string.
    @rtype: string
    """
    # Compile case-insensitive regex to match pattern
    m = re.compile('\s*\(Reported \d+ Times\)\s*', re.IGNORECASE)

    # Replace pattern in original string with empty string
    return m.sub('', hgvs_notation)


def find_string_index(string_list, search_string):
    """
    Given a list of strings and a string to search for, returns the index of the first element in the list
    that contains the search string. Note that the comparison is not sensitive to case or leading or trailing
    whitespace characters.

    @param string_list: list of strings
    @type string_list: list of strings
    @param search_string: a string to search for in elements of string_list
    @type search_string: string
    @return: index of the first instance of search_string as a substring of element in string_list. Returns -1 if
    search_string is not found in the string_list.
    @rtype: number
    """

    # Remove leading/trailing whitespace and convert to lowercase before comparisons
    string_list = [x.lower().strip() for x in string_list]
    search_string = search_string.lower().strip()

    for i in range(0, len(string_list)):
        entry = string_list[i]

        if search_string in entry:
            return i

    # search_string not found, return -1
    return -1


def swap(list, i, j):
    """
    Swaps elements at indices i and j in list. Indices must be within bounds of array. Index swapped with itself
    leaves the list unchanged.

    @param list: list of elements
    @type list: list
    @param i: index of element to be swapped with element at index j. Must be within bounds of array.
    @param j: index of element to be swapped with element at index i. Must be within bounds of array.
    @return: list with elements at indices i and j swapped. If i and j are equal, list is unchanged.
    @rtype: list
    """

    list[i], list[j] = list[j], list[i]
    return list


def deep_copy(nested_list):
    """
    Makes a deep copy of lists that may or may not contain nested lists. Nested items that are not lists will not
    be deep copied, they will be shallow copied.

    @param nested_list: a list that may or may not contain nested lists. Nested lists may contain additional nested
    lists.
    @type nested_list: list or list of lists
    @return: deep copy of nested_list
    @rtype: same as input. Can handle lists of arbitrary dimension.
    """
    copy = []
    for item in nested_list:
        if isinstance(item, list):
            copy.append(deep_copy(item))
        else:
            copy.append(item)
    return copy
