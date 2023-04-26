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

            if name_list.index(name) == (len(name_list)-1):
                new_list.append(name)
            else:
                new_list.append(name+',')

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
    df['author_list'] = df.author.str.split(' and ') # keep spaces in, otherwise messes up those with name "Alexander"
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

    if '_' in topic:
        topic = topic.replace('_', ' ').title()
    else:
        topic = topic.title()

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

        if topic.name == 'hardware':
            df_citations = bib_to_csv(topic.name, root_dir, 
                                      bib_file='citations.bib', save=save_topics)
            df_citations = bib_to_csv(topic.name, root_dir, 
                                      bib_file='collaborations.bib', save=save_topics)
            df_citations = bib_to_csv(topic.name, root_dir,
                                      bib_file='algoteamcitations.bib', save=save_topics)

    website.to_csv(csv_dir.joinpath('website.csv'), index=False)
    print("Finished saving website.csv")
    print("Save Directory:", csv_dir)

    return website

def collate_topic(topic, root_dir, save=True):
    """ Collate all bib files for one team's topic. """
    csv_dir = root_dir.joinpath('csv')

    articles = pd.read_csv(csv_dir.joinpath(topic+'-articles.csv'))
    citations = bib_to_csv(topic, root_dir, bib_file='citations.bib', save=True)
    collaborations = bib_to_csv(topic, root_dir, bib_file='collaborations.bib', 
                                save=True)

    articles['csv-file'] = 'articles'
    citations['csv-file'] = 'citations'
    collaborations['csv-file'] = 'collaborations'

    all_references = pd.concat([articles, citations, collaborations], 
                               ignore_index=True)

    if topic == 'hardware':
        algoteamcitations = bib_to_csv(topic, root_dir, 
                                       bib_file='algoteamcitations.bib', 
                                       save=True)
        algoteamcitations['csv-file'] = 'algoteamcitations'
        all_references = pd.concat([all_references, algoteamcitations], 
                                   ignore_index=True)
        
        IonQ = bib_to_csv(topic, root_dir, 
                                       bib_file='IonQ.bib', 
                                       save=True)
        IonQ['csv-file'] = 'IonQ'
        all_references = pd.concat([all_references, IonQ], 
                                   ignore_index=True)
    all_references = all_references[['csv-file', 'title', 'author', 'journal', 
                                     'publisher', 'url', 'doi', 'month', 'year']]

    if save:
        all_csv = topic+'-references.csv'
        all_references.to_csv(csv_dir.joinpath(all_csv), index=False)

    return all_references