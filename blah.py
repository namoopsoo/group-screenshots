import re
import ipdb
import argparse
import os
import datetime
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import random

DESTINATION_PARENT_DIR = os.getenv('DESTINATION_PARENT_DIR')

def make_clusters(files_vec):
    screenshots = sorted(filter(is_screenshot, files_vec))
    dates = [to_date(x) for x in screenshots]
    
    first_date = dates[0]
    deltas = [(d - first_date).total_seconds() for d in dates]
    
    db = DBSCAN(eps=600, min_samples=10).fit([[x] for x in deltas])
    out = zip(screenshots, deltas, db.labels_)
    return pd.DataFrame.from_records(out, columns=['file', 'delta', 'label'])

def more_do(search_directory, dry_run=True):
    
    df = make_clusters(os.listdir(search_directory))

    firsts_vec = list(
            df[df.label != -1].drop_duplicates(
                subset='label')[['label', 'file']
                    ].to_records(index=False))
    firsts_filenames = [x[1] for x in firsts_vec]
    new_dirs = [new_dir_name_from_filename(x) for x in firsts_filenames]

    print('labels: '
            + str(list(df.label.value_counts())[:10]))

    print('Will create new dirs'
            + str(new_dirs))
    if not dry_run:
        [create_new_group_dir(x) for x in new_dirs]

    print('Done.')
    
    
   
def is_screenshot(x):
    return True if re.match('\d{4}-\d{2}-\d{2} \d{2}.\d{2}.\d{2}.png', x) else False
    
def to_date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d %H.%M.%S.png')

def new_dir_name_from_filename(x):
    assert is_screenshot(x)
    d = to_date(x)
    return os.path.join(DESTINATION_PARENT_DIR,
                        '{}-{}'.format(
                            d.strftime('%Y-%m-%d-%H%M'),
                            random.randint(10,99)))

def create_new_group_dir(dirname):
    os.mkdir(dirname)
    
def plot_distances_between_clusters(clusters_df):
    pass

def random_points_create():
    # This quick experiment shows that the input to DBSCAN doesnt actually need to be StandardScaled . 
    X = reduce(lambda x,y:x+y, [[a + random.randint(0, 100) for x in range(100)] for a in [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]])

    pd.DataFrame.from_records([[x] for x in X]).to_csv('/Users/michal/Downloads/2019-01-13--dbscan--folder-clusters/X.csv')
    db = DBSCAN(eps=10, min_samples=10).fit([[x] for x in X])
    
    # ==> 
    # In [33]: len(db.labels_), Counter(db.labels_)
    # Out[33]: 
    # (1000,
    #  Counter({0: 100,
    #           1: 100,
    #           2: 100,
    #           3: 100,
    #           4: 100,
    #           5: 100,
    #           6: 100,
    #           7: 100,
    #           8: 100,
    #           9: 100}))

    
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
                    'type': str,
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
            


    
    
import numpy as np

from bokeh.plotting import figure, show, output_file
def doplot(x, y, labels):
    # import ipdb; ipdb.set_trace()
    N = x.shape[0]
    radii = np.array([10,]*N)

    colors = [
        "#%02x%02x%02x" % (int(50+2*label), 
        int(30+2*label), 150) for label in labels]
       
    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
    p = figure(tools=TOOLS)

    p.scatter(x, y, radius=radii,
          fill_color=colors, fill_alpha=0.6,
          line_color=None)
    filename = datetime.datetime.now().strftime(
            '%Y-%m-%dT%H.%M.%S.html')
    output_file(filename, title="color_scatter.py example")

    show(p)  # open a browser



def do():
    parser = argparse.ArgumentParser()

    [parser.add_argument(*x[0], **x[1])
            for x in bake_options()]

    # Collect args from user.
    args = vars(parser.parse_args())

    print(args)

    with ipdb.launch_ipdb_on_exception():
        more_do(search_directory=args['search_directory'])
    
do()

