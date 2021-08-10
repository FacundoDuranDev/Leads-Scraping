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
    site_choices = list(site_list.keys())
    parser.add_argument('--o',help='Operation',type=str)
    parser.add_argument(
                        'market_site',
                        help="Market Sites Available to Scrap",
                        type=str,
                        choices=site_choices,
                        default=None
                        )

    args = parser.parse_args()
    market_site = args.market_site
    operation = args.o
    
    module = None
    module = 'sites.' + market_site.lower()

    MODULE_NAME = module

    try:
        module = import_module(MODULE_NAME)
    
        SiteClass = getattr(module, market_site)
    except ModuleNotFoundError as exc:
        print(exc)
        print("\nThe name of the file and the class doesnt match\n")
        print(f'to import: "{market_site}"...')
        print(f'The file must be named "{market_site.lower()}.py')

    if market_site in site_choices:
        print(market_site)
    
    if operation in ('scraping', 'testing'):
       
        SiteClass(config,operation,market_site)
       