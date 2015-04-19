# ccsv2mongo
Utility to convert a CSV file to a MongoDB JSON dump.

Usage: `ccsv2mongo -f data.csv -o data.json`

Tested with:
* Python 2.7.9, PyPy 2.5.1 and IronPython 2.7.5 (works).
* Jython 2.5.3 (use Jython tweaked version): 
* `jython ccsv2mongo.jy.py -f data.csv -o data.json`
