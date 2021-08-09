import argparse
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
import os
from importlib import import_module


dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path+'\config.yaml') as f:
    config = yaml.load(f, Loader=SafeLoader)
site_list = config['Sites']


if __name__ == "__main__":
    initialized = datetime.now()
    parser = argparse.ArgumentParser()
    site_choices = site_list
    parser.add_argument('--s',help='Site to Scrap',type=str)
    parser.add_argument('--o',help='Operation',type=str)
    parser.add_argument(
                        'market_sites',
                        help="Market Sites Available to Scrap",
                        type=str,
                        choices=site_choices,
                        default=None
                        )

    args = parser.parse_args()

    website = args.s
    market_sites = args.market_sites
    website_operation = args.o
    
    if website in site_choices:
        print(website)