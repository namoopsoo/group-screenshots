
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


In [27]: print df[df.label != -1].label.unique().tolist()
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]

In [28]: df[df.label == 0]
Out[28]: 
                        file        delta  label
328  2018-01-27 12.27.44.png  184777822.0      0
329  2018-01-27 12.28.06.png  184777844.0      0
330  2018-01-27 12.28.47.png  184777885.0      0
331  2018-01-27 12.29.46.png  184777944.0      0
332  2018-01-27 12.30.41.png  184777999.0      0
333  2018-01-27 12.32.11.png  184778089.0      0
334  2018-01-27 12.37.30.png  184778408.0      0
335  2018-01-27 12.37.54.png  184778432.0      0
336  2018-01-27 12.39.01.png  184778499.0      0
337  2018-01-27 12.41.24.png  184778642.0      0
338  2018-01-27 12.41.53.png  184778671.0      0
339  2018-01-27 12.42.32.png  184778710.0      0
340  2018-01-27 12.42.55.png  184778733.0      0
341  2018-01-27 12.43.26.png  184778764.0      0
342  2018-01-27 12.44.21.png  184778819.0      0
343  2018-01-27 12.46.28.png  184778946.0      0

In [29]: df[df.label == 1]
Out[29]: 
                        file        delta  label
379  2018-02-05 16.34.24.png  185570222.0      1
380  2018-02-05 16.38.33.png  185570471.0      1
381  2018-02-05 16.38.58.png  185570496.0      1
382  2018-02-05 16.39.21.png  185570519.0      1
383  2018-02-05 16.39.26.png  185570524.0      1
384  2018-02-05 16.40.08.png  185570566.0      1
385  2018-02-05 16.42.44.png  185570722.0      1
386  2018-02-05 16.43.30.png  185570768.0      1
387  2018-02-05 16.44.09.png  185570807.0      1
388  2018-02-05 16.44.30.png  185570828.0      1
389  2018-02-05 16.45.43.png  185570901.0      1
390  2018-02-05 16.46.03.png  185570921.0      1
391  2018-02-05 16.47.45.png  185571023.0      1
392  2018-02-05 16.48.39.png  185571077.0      1
393  2018-02-05 16.48.51.png  185571089.0      1
394  2018-02-05 16.49.38.png  185571136.0      1
395  2018-02-05 16.50.58.png  185571216.0      1
396  2018-02-05 16.51.29.png  185571247.0      1

In [30]: df[df.label == 2]
Out[30]: 
                        file        delta  label
403  2018-02-08 16.33.57.png  185829395.0      2
404  2018-02-08 16.34.30.png  185829428.0      2
405  2018-02-08 16.35.03.png  185829461.0      2
406  2018-02-08 16.35.08.png  185829466.0      2
407  2018-02-08 16.37.28.png  185829606.0      2
408  2018-02-08 16.41.50.png  185829868.0      2
409  2018-02-08 16.46.11.png  185830129.0      2
410  2018-02-08 16.46.52.png  185830170.0      2
411  2018-02-08 16.47.39.png  185830217.0      2
412  2018-02-08 16.48.25.png  185830263.0      2
413  2018-02-08 16.49.17.png  185830315.0      2
414  2018-02-08 16.50.21.png  185830379.0      2
415  2018-02-08 16.52.04.png  185830482.0      2
416  2018-02-08 16.52.31.png  185830509.0      2
417  2018-02-08 16.53.42.png  185830580.0      2


```
