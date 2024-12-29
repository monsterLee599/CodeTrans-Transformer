

# Data Processing and Code Transformation

This repository contains scripts for downloading, processing, and transforming CodeSearchNet datasets for Java and Python. The datasets are downloaded into respective folders, e.g., the test file path for Python is `./dataset/CodeSearchNet/python/test.jsonl`.


## Examples of Code Transformation

<img width="656" alt="image" src="https://github.com/user-attachments/assets/c8cf1f88-0918-4915-b623-79a1072259bb" />


## Data Download and Processing



Since the raw data includes some unnecessary information, we need to run `extract_csn.py` to process the dataset. The processed data will be stored in the `./csn_data` folder.

For example, to process the Python test set file, use the following command:

```sh
python extract_csn.py --language python --info test
```

This will process the Python test set file and output four files in the `./csn_data/python/test` folder:
- `code_test.json`: Contains the extracted code in key-value pairs, where the key is the data ID.
- `file_path_test.txt`: Contains the paths to the code repositories.
- `target_test.txt`: Contains the summaries of the code.
- `parse_test.json`: Contains the parsed AST (Abstract Syntax Tree) of the extracted code.

**Note**: Some parts of the CodeSearchNet dataset are written in Python 2 and cannot be processed directly. These can be converted to Python 3 before processing.

## Directory Structure

- `build and venv`: Environments required for tree-sitter.
- `dataset`: Data storage path.
- `java`: Implementation of code transformation for Java.
- `python`: Implementation of code transformation for Python.
- `scripts`: Scripts for code to AST conversion, transformation to tree structure representation, parsing, etc.
- `extract_csn.py`: Extracts the CodeSearchNet dataset.
- `python_trans.py`: Performs code transformation on Python code.
- `java_trans.py`: Performs code transformation on Java code.

## Code Transformation Application

Currently, only code transformation numbers are supported as input, such as `I-2` for variable renaming.

To apply a code transformation, use the following command:

```sh
python python_trans.py --language python --info test --code_trans I-2 
```

### Example

**Input:**

```python
def sina_xml_to_url_list(xml_data):
    rawurl = []
    dom = parseString(xml_data)
    for node in dom.getElementsByTagName('durl'):
        url = node.getElementsByTagName('url')[0]
        rawurl.append(url.childNodes[0].data)
    return rawurl
```

**Output:**

```python
def sina_xml_to_url_list(var_0):
    var_1 = []
    var_2 = parseString(var_0)
    for node in var_2.getElementsByTagName('durl'):
        var_3 = node.getElementsByTagName('url')[0]
        var_1.append(var_3.var_4[0].var_5)
    return var_1
```




## Code transformation Statistics

The edit distance and the number of transformable code for all code transformation strategies. The number of
test sets of Java and Python are 10955 and 14918, respectively.

For Java testset:

|  No.  |                    Mode                   |  Num.  | Dist.  |
|:-----:|:-----------------------------------------:|:------:|:------:|
|  B-1  |        For to While                       |  1086  |  13.95 |
|  B-2  |        While to For                       |   714  |   3.43 |
|  B-3  |     Elseif to Else If                     |   618  |   3.60 |
|  B-4  |      Elseif to Else If                    |    89  |   2.13 |
|  B-5  |        If-Else Swap                       |  2096  |  37.00 |
|  B-6  |   Decompose Complex If                   |  1451  |  13.29 |
|  B-7  |      Extract Function                     |      - |      - |
| ID-1  |       Insert Comments                     | 10955  |   5.00 |
| ID-2  |     Insert Junk Code                      | 10955  |  65.08 |
| ID-3  |   Append Return Statement                 |  3758  |   2.09 |
| ID-4  | Import Unrelated Library                  | 10955  |  70.00 |
| ID-5  |       Remove Comments                     |     -  |      - |
| ID-6  |  Replace Print with Pass                  |   156  |  26.64 |
| ID-7  |  Delete Unused Variable                   |    40  |  12.45 |
| GS-1  |         Refactor Return Statement         |   617  |  18.40 |
| GS-2  |     Internalize For Loop Declaration      |     6  |   4.00 |
| GS-3  |      Externalize For Loop Declaration     |   982  |   7.42 |
| GS-4  | Separate Declaration and Initialization   |  6965  |   5.34 |
| GS-5  |           Wrap with Logical NOT           |  6228  |   9.31 |
| GS-6  |       Reverse Comparison Operator         |  2176  |   6.49 |
| GS-7  |      Explicitize Assignment Operator      |   438  |   6.87 |
| GS-8  |          Expand Unary Operator            |  1334  |   6.10 |
| GS-9  |        Encapsulate in Curly Braces        |  2006  |   4.03 |
| GS-10 |          Remove Redundant Braces          |  4964  |   4.15 |
| GT-1  |            Boolean to Integer             |     -  |      - |
| GT-2  |             Integer to Boolean            |     -  |      - |
| GT-3  |          Promote Integral Type            |  2352  |   1.95 |
| GT-4  |           Promote Floating Type           |  2106  |   1.87 |
| GT-5  |            Refactor Input API             |     -  |      - |
| GT-6  |           Refactor Output API             |   226  |   5.78 |
|  I-1  |       function rename                     | 10955  |  16.92 |
|  I-2  |      variable rename                      | 10955  |  16.32 |



For Python testset:
|  No.  |                    Mode                   |  Num.  |  Dist.  |
|:-----:|:-----------------------------------------:|:------:|:-------:|
|  B-1  |        For to While                       |   311  |  15.54  |
|  B-2  |        While to For                       |     -  |     -   |
|  B-3  |     Elseif to Else If                     |  1353  |   5.57  |
|  B-4  |      Elseif to Else If                    |   151  |   3.22  |
|  B-5  |        If-Else Swap                       |  4138  |  31.07  |
|  B-6  |   Decompose Complex If                   |  1335  |   8.96  |
|  B-7  |      Extract Function                     |  2088  |  24.35  |
| ID-1  |       Insert Comments                     | 14918  |   5.00  |
| ID-2  |     Insert Junk Code                      | 14918  |  31.97  |
| ID-3  |   Append Return Statement                 |  6550  |   2.04  |
| ID-4  | Import Unrelated Library                  | 14918  |  20.53  |
| ID-5  |       Remove Comments                     |     -  |     -   |
| ID-6  |  Replace Print with Pass                  |   533  |  21.02  |
| ID-7  |  Delete Unused Variable                   |   164  |  12.84  |
| GS-1  |         Refactor Return Statement         |  1086  |   6.71  |
| GS-2  |     Internalize For Loop Declaration      |     -  |     -   |
| GS-3  |      Externalize For Loop Declaration     |     -  |     -   |
| GS-4  | Separate Declaration and Initialization   |     -  |     -   |
| GS-5  |           Wrap with Logical NOT           |  4345  |   8.02  |
| GS-6  |       Reverse Comparison Operator         |  1638  |   6.52  |
| GS-7  |      Explicitize Assignment Operator      |  1051  |  10.17  |
| GS-8  |          Expand Unary Operator            |     -  |     -   |
| GS-9  |        Encapsulate in Curly Braces        |     -  |     -   |
| GS-10 |          Remove Redundant Braces          |     -  |     -   |
| GT-1  |            Boolean to Integer             |  3775  |   1.90  |
| GT-2  |             Integer to Boolean            |  4829  |   2.85  |
| GT-3  |          Promote Integral Type            |  2431  |   2.42  |
| GT-4  |           Promote Floating Type           |  2431  |   2.42  |
| GT-5  |            Refactor Input API             |   145  |   1.81  |
| GT-6  |           Refactor Output API             |   520  |   9.87  |
|  I-1  |       function rename                     | 14691  |   7.87  |
|  I-2  |      variable rename                      | 14918  |  19.12  |
