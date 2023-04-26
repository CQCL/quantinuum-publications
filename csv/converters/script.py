"""
Script to create an updated view of the website.csv file. 

Also automatically updates the individual topic csv files.

"""
import pathlib
from utils import create_website_csv, collate_topic

root_dir = pathlib.Path.cwd()
print("root_dir:", root_dir)
website = create_website_csv(root_dir, save_topics=True)

topic = 'hardware'
hardware_references = collate_topic(topic, root_dir)

topic = 'IonQ'
hardware_references = collate_topic(topic, root_dir)