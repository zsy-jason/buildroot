# Copyright 2022 The Lynx Authors. All rights reserved.

import argparse
import logging
import os
import sys

def read_file_names_and_print(paths, base_path, exclude):
  file_list = []
  path_len = len(base_path)
  path_list = paths.split(";")
  for path in path_list:
    if path == '':
      continue
    files = os.listdir(path)
    for f in files:
      if isinstance(exclude, list):
        find = False
        for item in exclude:
          if item in f:
            find = True
            break
        if find:
          continue

      if not ((f.endswith('.h') 
          or f.endswith('.hpp') 
          or f.endswith('.cc') 
          or f.endswith('.cpp') 
          or f.endswith('.m') 
          or f.endswith('.mm') 
          or f.endswith('.S'))):
        continue
      full_path = os.path.join(path, f) 
      if not os.path.isdir(full_path):
        full_path = full_path[path_len:]
        file_list.append(full_path)
      else:
        continue
  file_list.sort()

  for source in file_list:
    print(source)
  return 0

def main():
  logging.info("test")
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--paths')
  parser.add_argument('-b', '--base_path')
  parser.add_argument('-e', '--exclude', nargs='*', type=str)
  args = parser.parse_args()
  paths = args.paths
  base_path = args.base_path
  exclude = args.exclude
  return read_file_names_and_print(paths, base_path, exclude)

if __name__ == '__main__':
  sys.exit(main())
