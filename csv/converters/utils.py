""" Script for converting a .bib file to .csv

    Update the .bib file you desire to run and Run All on the script

    Requires Python >= 3.9 with removesuffix function
"""
import bibtexparser
import numpy as np
import pandas as pd

def _reverse_author_order(name_list):
    """ Reverses author names to be first name (or initials) then last, returns
        string of results rather than list
    """
    new_list = []
    for name in name_list:
        if ',' in name:
            first_name = name.split(',')[1]
            last_name = name.split(',')[0]
            new_name = first_name+' '+last_name
            new_name = new_name.replace('  ', ' ').strip()

            if name_list.index(name) == (len(name_list)-1):
                new_list.append(new_name)
            else:
                new_list.append(new_name+',')
        else:
            new_list.append(name)

    new_list = ' '.join(name for name in new_list)
    new_list = new_list.replace('  ', ', ')
    return new_list

def _create_website_columns(df, topic):
    """ Create csv in format needed for Quantinuum website. """
    df['day'] = 1
    df['Date'] = pd.to_datetime(df[['year', 'month', 'day']])
    df['Date'] = (df['Date'].dt.strftime('%a') 
                  + ' ' + df['Date'].dt.strftime('%b') 
                  + ' ' + df['Date'].dt.strftime('%d') 
                  + ' ' + df['Date'].dt.strftime('%Y')
                  + ' 00:00:00 GMT+0000 (Coordinated Universal Time)')

    df['author'] = (df.author
                    .str.replace('\n', '', regex=True)
                    .str.replace('{', '', regex=True)
                    .str.replace('}', '', regex=True))
    df['author_list'] = df.author.str.split('and')
    df['Authors List'] = df.author_list.apply(lambda x: _reverse_author_order(x))

    if 'journal' not in df.columns:
        df['Journal'] = df.publisher.copy()
    else:
        df['Journal'] = df.journal.copy()
    df['Journal'] = np.where(df['Journal'].isin(['', ' ', '  ']), 
                             df.publisher, 
                             df.Journal)
    df['Journal'] = np.where(df['Journal'].isnull(), 
                             df.publisher, 
                             df.Journal)
    df['Journal'] = np.where(df.publisher == 'arXiv', 
                             'arXiv preprint', 
                             df.Journal)
    
    if topic == 'ai':
        topic = topic.upper()
    if topic == 'hardware':
        topic = 'Hardware'
    if topic == 'inquanto':
        topic = 'InQuanto'
    if topic == 'ml':
        topic = 'Machine Learning'
    if topic == 'nlp':
        topic = 'Natural Language Processing'
    if topic == 'other':
        topic = 'Other'
    if topic == 'qermit':
        topic = topic.upper()
    if topic == 'tket':
        topic = topic.upper()

    df['Tech Solution'] = topic

    df.rename(columns={'title':'Name', 
                       'url': 'Publication Link'}, 
              inplace=True)

    website = df[['Name', 'Date', 'Publication Link', 
                  'Authors List', 'Journal', 'Tech Solution']]

    return website

def bib_to_csv(topic, root_dir, bib_file='articles.bib', save=True):
    """ Function for converting and saving 1 .bib file as-is with no adjustments. 
        All BibTex entries are kept.
    """
    latex_dir = root_dir.joinpath('latex')
    csv_dir = root_dir.joinpath('csv')
    bib_dir = latex_dir.joinpath(topic)

    with open(bib_dir.joinpath(bib_file)) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        
    df = pd.DataFrame(bib_database.entries)

    if save:
        bib_csv = topic+'-'+bib_file.removesuffix('.bib')+'.csv'
        df.to_csv(csv_dir.joinpath(bib_csv), index=False)
        print("Finished saving csv:", bib_csv)
        # print("Save Directory:", csv_dir)

    return df

def create_website_csv(root_dir, save_topics=True):
    """ Create the website csv. 
    
        Convert all articles.bib files to csv, combine them, and transform 
        column formats.
    """
    latex_dir = root_dir.joinpath('latex')
    csv_dir = root_dir.joinpath('csv')
    bib_dir_topics = [f for f in latex_dir.iterdir() if f.is_dir()]

    website = pd.DataFrame()
    for topic in bib_dir_topics:
        df_topic = bib_to_csv(topic.name, root_dir, save=save_topics)
        df_website = _create_website_columns(df_topic, topic.name)
        website = pd.concat([website, df_website], ignore_index=True)

    website.to_csv(csv_dir.joinpath('website.csv'), index=False)
    print("Finished saving website.csv")
    print("Save Directory:", csv_dir)

    return website
