import pandas as pd
import sys

coverage_result, stat_result, infotable, output_file, min_readnum = sys.argv[1:]

'''
min_readnum = 2
infotable = '~/VHDB_Vertebrate/db_file/vhdb_info.csv'
coverage_result = '/home/renzirui/VHDB_Vertebrate/testoutput/2.coverage/chip_head1M_coverage.txt'
stat_result = '/home/renzirui/VHDB_Vertebrate/testoutput/0.stats/chip_head1M.seqkit.stats.txt'
output_file = 'testout.csv'
'''

num_millionreads = pd.read_table(stat_result, sep='\s+', thousands=',')['num_seqs'].sum() / 1e6

coverage = pd.read_table(coverage_result, names=['accession', 'startpos', 'ref_length', 'numreads', 'covbases', 'coverage', 'meandepth', 'meanbaseq', 'meanmapq']).drop('startpos', axis=1)
coverage = coverage[coverage['numreads'] > int(min_readnum)]
coverage['RPM'] = coverage['numreads'] / num_millionreads
coverage['RPKM'] = coverage['numreads'] / num_millionreads / coverage['ref_length'] * 1e3

info = pd.read_csv(infotable)
info.merge(coverage).to_csv(output_file, index=False)


