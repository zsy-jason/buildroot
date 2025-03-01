#!/usr/bin/env python3
# Copyright 2024 The Lynx Authors. All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree.

import os
import sys

def ndk_major_version(path) -> int:
  major_version = "0"
  if os.path.exists(path):
    with open(path, "r") as f:
      for line in f:
        line = line.strip()
        if line.startswith("Pkg.Revision"):
          full_version = line.split()[-1]
          major_version = full_version.split(".")[0]
          break
  return major_version


def main():
  sys.stdout.write(ndk_major_version(sys.argv[1]))
  return 0


if __name__ == '__main__':
  sys.exit(main())
