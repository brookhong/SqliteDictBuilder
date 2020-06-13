A python script to build dictionary for Dictorium.

The input_file is a plain text file, each item is described in three lines. The 1st line of which is the key of the item, the 2nd is the value, and the 3rd is a delimiter line as `</>`. Please see [test.txt](https://github.com/brookhong/SqliteDictBuilder/tstdata/test.txt) for example.

The out_file is a sqlite file, you could use sqlite3 cli to check its schema.

## Usage

    usage: gen-dict [-h] [--resource_dir RESOURCE_DIR] [--patch PATCH] [--dryrun]
                    input_file output_file

    generate sqlite3 dict

    positional arguments:
      input_file            input text file
      output_file           file name for generated db

    optional arguments:
      -h, --help            show this help message and exit
      --resource_dir RESOURCE_DIR
                            resource files in the dir will be inserted into the db
      --patch PATCH         specify the keywords for which to patch
      --dryrun              specify the keywords for which to patch

## examples

* build dictionary `test.db` from `test.txt`

        cd tstdata/
        python ../gen-dict.py test.txt test.db --resource_dir res


* patch dictionary `test.db` by replacing a resource file `res/js/main.js`

        cd tstdata/
        python ../gen-dict.py test.txt test.db --resource_dir res --patch res/js/main.js

### Verify the test.db
1. install Brook's Chromium build.
2. access `dictorium://query/the` with the Chromium.
