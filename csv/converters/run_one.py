"""
Script to create a csv file from bib file.

"""
import pathlib
from utils import bib_to_csv

root_dir = pathlib.Path.cwd()
print("root_dir:", root_dir)
hw_citations = bib_to_csv('hardware', root_dir, bib_file='citations.bib', save=True)
hw_collaborations = bib_to_csv('hardware', root_dir, bib_file='collaborations.bib', save=True)