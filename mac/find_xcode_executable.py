
#!/usr/bin/env python3
# Copyright 2020 The Lynx Authors. All rights reserved.

"""Find the full path to executable NAME in the provided SDK and toolchain of Xcode.

Usage:
  python find_xcode_executable.py clang
"""

import subprocess
import sys

from argparse import ArgumentParser


def main():
  parser = ArgumentParser()
  parser.add_argument("name", help="The name of the executable to find")
  args = parser.parse_args()

  job = subprocess.Popen(['xcodebuild', '-find-executable', args.name],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL)
  out, err = job.communicate()
  out = out.decode()
  if job.returncode != 0 and err != None:
    sys.stderr.writelines([out, err])
    raise Exception(('Error %d running xcodebuild, please check if you hava Xcode installed on your system') % job.returncode)

  return out.strip()


if __name__ == '__main__':
  if sys.platform != 'darwin':
    raise Exception("This script only runs on Mac")
  print((main()))
