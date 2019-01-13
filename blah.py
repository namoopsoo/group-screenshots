import re
import argparse
import os
import datetime

def make_clusters(files_vec):
    return map(to_date, 
        filter(is_screenshot, files_vec)
       )

def is_screenshot(x):
    return True if re.match('\d{4}-\d{2}-\d{2} \d{2}.\d{2}.\d{2}.png', x) else False
    
def to_date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d %H.%M.%S.png')


def random_points_create():
    w
    random.randint
    
def bake_options():
    return [
            [['--verbose', '-v'],
                {'action': 'store_true',
                    'help': 'pass to to be verbose with commands'},
                ],
            [['--dry-run', '-D'],
                {'action': 'store_true',
                    'help': 'Dry run. Just print the command.  '},],
                    [['--search-directory', '-d'], {
                    'action': 'store_true',
                    'help': 'Where to look for clusters',
                    'required': True
                    }]
                ]
    ##
    #             help='',
    #             default='',
    #             required='',
    #             choices='',
    #             action='',
    #             type='',
            

def do():
    parser = argparse.ArgumentParser()

    [parser.add_argument(*x[0], **x[1])
            for x in bake_options()]

    # Collect args from user.
    args = parser.parse_args()

    print vars(args)
    
do()

