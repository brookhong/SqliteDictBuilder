import sqlite3
import os, sys, re
import fnmatch
import argparse

MIME_TYPES = {
    "html": 'text/html',
    "txt": 'text/plain',
    "inc": 'text/plain',
    "js": 'application/javascript',
    "css": 'text/css',
    "mp3": "audio/mpeg",
    "json": "application/json",
    "woff": "application/font-woff",
    "svg": "image/svg+xml",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "ttf": "application/x-font-ttf",
    "ttc": "application/x-font-ttf",
    "otf": "application/x-font-opentype"
}

def recursive_glob(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        goodfiles = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in goodfiles)
    return results

def generateResDb(conn, path, dryrun, patch):
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists resources
                 (name text PRIMARY KEY, type text, content blob)''')

    for f in recursive_glob(path, "*"):
        filename, file_extension = os.path.splitext(f)
        if os.path.isfile(f):
            tp = MIME_TYPES[file_extension[1:]]
            name = re.sub(r'^[^/]*/', '~/', f)
            if patch == None:
              if dryrun:
                  print(f + " inserted")
              else:
                  c.execute("INSERT INTO resources VALUES (?, ?, ?)", (name, tp, sqlite3.Binary(open(f).read())))
            elif f == patch:
              if dryrun:
                  print(f + " updated")
              else:
                  c.execute("UPDATE resources SET content = ? WHERE name = ?", (sqlite3.Binary(open(f).read()), name))

    conn.commit()

def generateDb(args):
  conn = sqlite3.connect(args.output_file)
  conn.text_factory = str
  c = conn.cursor()
  c.execute('''CREATE TABLE if not exists words
               (key text PRIMARY KEY, value text)''')
  with open(args.input_file) as fp:
    line = fp.readline()
    entryState = "Key"
    while line:
        line = line.strip()
        if entryState == "Key":
            key = line
            value = ""
            entryState = "Value"
        elif entryState == "Value":
            if line == "</>":
              if args.patch == None:
                if args.dryrun:
                  print(key + " inserted")
                else:
                  c.execute("INSERT INTO words VALUES (?, ?)", (key, value))
              elif key == args.patch:
                if args.dryrun:
                    print(key + " updated")
                else:
                    c.execute("UPDATE words SET value = ? WHERE key = ?", (value, key))
              entryState = "Key"
            else:
                value += line
        line = fp.readline()
    conn.commit()

    if args.resource_dir:
        generateResDb(conn, args.resource_dir, args.dryrun, args.patch)

    conn.close()

parser = argparse.ArgumentParser(
    prog='gen-dict',
    description='generate sqlite3 dict'
)
parser.add_argument('input_file', help="input text file")
parser.add_argument('output_file', help="file name for generated db")
parser.add_argument('--resource_dir', help="resource files in the dir will be inserted into the db")
parser.add_argument('--patch', help="specify the keywords for which to patch")
parser.add_argument('--dryrun', default=False, action='store_true', help="specify the keywords for which to patch")

args = parser.parse_args()
generateDb(args)
