# Quantinuum Publications

A repository for tracking publications produced by the Quantinuum teams.

This project is set up for both business and technical teams. The business teams
are using this for tracking and keeping the Quantinuum website up to date while
the technical teams may use this the `latex` files for pulling in to their 
research papers.

## Project Organization

- The `csv` folder contains csv files with publications in a format suitable for 
the website.
- The `latex` folder contains BibTex files by topic as found on the website.

The steps for adding to this project is as follows:

- Add publication in a BibTex file in the `latex` folder.
- Update the pdf file by running the TeX file in that folder.
- Update the csv files by running `create-csv.ipynb` notebook in the in the `csv` folder.                     

## Updates

You are welcome to contribute and add your publications in the appropriate folder 
as long as you follow the guidelines below. 
- Publications will be checked and added once a month. 
- About once a quarter, arXiv publications will be checked to see if any have 
now been published in a journal.

## Formatting Guidelines for `.bib` files

Here are a few notes on how the `.bib` files are organized and formatted, to keep
new entries consistent.

### Chronological Ordering: Oldest to Newest

Entries are given in chronological order with oldest articles at the top, newest
articles at the bottom. While this isn't necessary for LaTex, this will help
keep straight which articles have been added yet or not.

### Month Field

Note the month field should be present, in numeric version of the month listed. 
If the month listed is `{Apr}`, the field should be updated to `{4}`.

### Abstract Field

If an `abstract` field exists, remove it.

### Format

Make sure entries are surrounded by 1 set of curly braces. Sometimes there are 
no braces while other times entries have double braces. `year = {2022}`

### Exporting Citations from arXiv

If you click on `Export BibTex Citation` on an article page on arXiv, note that
the BibTex type is `misc`. Update this to `article`. In addition, the ordering
of the entries doesn't follow the ordering here. Make sure to update this and
add the month entry in numeric format.

### Updating arXiv References once Published

Once a journal has been accepted, such as to the American Physical Society (APS)
or Nature, any previously entered arXiv references should be replaced. Note that
the order should be updated to align with the journal's publishing date.

### Checking if Articles have been Published in a Journal

The easiest way to check if a paper on arXiv has been published in a journal is 
to click on *Google Scholar* on the paper's arXiv page. This is on the 
right-hand side under *References & Citations*. This will bring you to a page 
listing the article on Google Scholar. Under the paper abstract click "All XX 
versions" where XX is the number of versions Google Scholar found. This will 
bring you to a page where all websites where the article is available on the web
is listed. Look for true peer-reviewed journals such as Phys Rev. and Nature. 
You may update the reference for any articles that have now been published in
peer-reviewed journals. 

## Creating Website File

A Jupyter notebook called `create-csv.ipynb` is located in the `csv` folder. 
This notebook assumes you are running the it from the `csv` folder. Inside the 
noteboook are cells for converting the `.bib` file to `.csv`. The python 
installations you need to run the notebook are in the `requirements.txt` file. 