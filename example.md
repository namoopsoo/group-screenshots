
#### Nice first stab at this
* In this quick and dirty `DBSCAN` , I take my iphone screenshots dropbox folder and use DBSCAN with `600 seconds`. 
* Output looks pretty accurate when I inspected the files themselves.
```python
import re
import argparse
import os
import datetime

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import random

def make_clusters(files_vec):
    screenshots = sorted(filter(is_screenshot, files_vec))
    dates = map(to_date, screenshots)
    
    first_date = dates[0]
    deltas = [(d - first_date).total_seconds() for d in dates]
    
    db = DBSCAN(eps=600, min_samples=10).fit([[x] for x in deltas])
    return zip(screenshots, deltas, db.labels_)

   
def is_screenshot(x):
    return True if re.match('\d{4}-\d{2}-\d{2} \d{2}.\d{2}.\d{2}.png', x) else False
    
def to_date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d %H.%M.%S.png')

```

```python
In [13]: out = make_clusters(os.listdir('.'))

In [14]: len(out)
Out[14]: 3669

In [15]: import pandas as pd

In [21]: df = pd.DataFrame.from_records(out, columns=['file', 'delta', 'label'])

In [22]: df.to_csv('/Users/me/Downloads/2019-01-13--dbscan--folder-clusters/output.csv')

In [22]: df[df.label != -1].shape
Out[22]: (899, 3)

In [23]: df[df.label != -1].head()
Out[23]: 
                        file        delta  label
328  2018-01-27 12.27.44.png  184777822.0      0
329  2018-01-27 12.28.06.png  184777844.0      0
330  2018-01-27 12.28.47.png  184777885.0      0
331  2018-01-27 12.29.46.png  184777944.0      0
332  2018-01-27 12.30.41.png  184777999.0      0

In [24]: df[df.label != -1].label.value_counts()
Out[24]: 
7     41
8     37
34    35
12    27
32    26
25    26
28    25
11    22
9     21
13    19
53    18
16    18
43    18
1     18
26    18
22    17
41    17
15    16
17    16
0     16
48    16
23    15
2     15
31    15
30    15
20    15
52    15
10    15
27    13
33    13
46    12
14    12
47    12
36    12
49    12
44    12
6     12
54    12
45    12
18    12
35    12
38    12
19    12
5     11
21    11
42    11
37    11
40    11
3     11
4     10
51    10
29    10
55    10
50    10
39    10
24    10
56     9
Name: label, dtype: int64


```
