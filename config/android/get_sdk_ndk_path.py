#!/usr/bin/env python
# Copyright 2023 The Lynx Authors
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree.

import argparse
import os
import sys

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--env-var', type=str, required=True, help='Retrieve the value of the environment variable')
  parser.add_argument('-p', '--default-path', type=str, required=True, help='Default path')
  args = parser.parse_args()
  env_var = args.env_var
  file_path = args.default_path

  if(os.path.exists(file_path)):
    print(file_path, end='')
  else:
    env_var_value = os.getenv(env_var)
    env_var_value = env_var_value if env_var_value else os.getenv(env_var + "_HOME")
    print(env_var_value, end='')

if __name__ == '__main__':
  sys.exit(main())