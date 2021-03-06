# -*- coding: utf-8 -*-
"""
GENE FINDER PROJECT 1

@author: ALEX CHAPMAN

"""

import random
from amino_acids import aa, codons, aa_table
from load import load_seq
dna_master = load_seq("./data/X73525.fa")


def shuffle_string(s):
    """Shuffles the characters in the input string
        NOTE: this is a helper function, you do not
        have to modify this in any way """
    return ''.join(random.sample(s, len(s)))

# YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide
        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """

    # Because python doesnt have case statements :(
    if nucleotide == 'A':
        return 'T'
    elif nucleotide == 'T':
        return 'A'
    elif nucleotide == 'C':
        return 'G'
    elif nucleotide == 'G':
        return 'C'
    else:
        return 'NA'


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
    sequence
    dna: a DNA sequence represented as a string
    returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    reversed_dna = dna[::-1]            # reverses string
    list_dna = list(reversed_dna)       # creates list from string
    blank_to_return = ''
    for i in range(0, len(list_dna)):
        blank_to_return += get_complement(list_dna[i])
    return blank_to_return


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start
        codon and returns the sequence up to but not including the
        first in frame stop codon.  If there is no in frame stop codon,
        returns the whole string.

        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("ATGATATTCG")
    'ATGATATTCG'
    """
    # List of stop codons
    stop_codons = ['TAG', 'TAA', 'TGA']
    list_dna = []
    ended = False
    i = 0
    while ended is False:
        # Searches by 3-char intervals
        i += 3
        to_append = dna[i-3:i]
        list_dna.append
        for stop_codon in stop_codons:
            if(to_append == stop_codon):
                ended = True
            if(i > len(dna)):
                return(dna)
                ended = True
    # Returns the string instead of the list of codons
    to_return = dna[0:i-3]
    return to_return


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA
        sequence and returns them as a list.  This function should
        only find ORFs that are in the default frame of the sequence
        (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("GCATGAATGTAG")
    ['ATG']

    >>> find_all_ORFs_oneframe("CCCATGTAG")
    ['ATG']
    """
    list_dna = []
    hold = dna
    length = int(len(dna)/3)
    for i in range(0, length):      # Seperates out string into codons
        list_dna.append(dna[:3])    # Adds codon to list
        dna = dna[3:]               # Modifies original DNA string
    list_dna.append(dna)            # Adds the remaining characters back in
    dna = hold
    to_return = []
    ended = False
    index = 0
    while ended is False:           # Similar to previous loop
        start_index = -1
        sample = list_dna[index]
        if sample == 'ATG':
            start_index = index     # Establishes where the codon starts
            found_ORF = rest_of_ORF(dna[start_index*3:])
            to_return.append(found_ORF)
            found_ORF_length = len(found_ORF)
            # Sets the cursor index to the end of the found ORF
            index += int(found_ORF_length/3)
        if index >= len(list_dna)-1:
            ended = True
        index += 1
    return to_return


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in
        all 3 possible frames and returns them as a list.  By non-nested we
        mean that if an ORF occurs entirely within another ORF and they are
        both in the same frame, it should not be included in the returned list
        of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']

    This test makes sure that if the dna doesn't start with a start codon, it
    still runs
    >>> find_all_ORFs("AAAATGCCCTAG")
    ['ATGCCC']
    """
    first = find_all_ORFs_oneframe(dna)
    second = find_all_ORFs_oneframe(dna[1:])
    third = find_all_ORFs_oneframe(dna[2:])
    solution = first + second + third
    return solution


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    base_pair = get_reverse_complement(dna)
    base = find_all_ORFs(dna)
    paired = find_all_ORFs(base_pair)
    to_add = [base, paired]
    solution = []
    for i in to_add:
        if i is not None:
            solution += i
    return solution


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    solution = find_all_ORFs_both_strands(dna)
    return(max(solution, key=len))


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence

        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    longest = 0
    to_test = []
    for i in range(num_trials):
        shuffled_dna = shuffle_string(dna)
        to_test.append(longest_ORF(shuffled_dna))
    longest = len(max(to_test, key=len))
    return longest


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).

        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    solution = ''
    for i in range(0, int(len(dna)/3)):
        tested = dna[:3]
        dna = dna[3:]
        solution += aa_table[tested]
    return solution


def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna

        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    threshold = longest_ORF_noncoding(dna, 1500)
    longest = find_all_ORFs_both_strands(dna)
    threshold = 600
    protiens = []
    for i in longest:
        if(len(i) > threshold):
            protiens.append(coding_strand_to_AA(i))
    print('PROTIENS BEGIN:', protiens)
    return protiens


if __name__ == "__main__":
    gene_finder(dna_master)
    import doctest
    doctest.testmod()
