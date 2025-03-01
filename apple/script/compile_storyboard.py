# Copyright 2019 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Compiles a .storyboard file.
"""

import argparse
import os
import subprocess
import sys


def CompileStoryboard(storyboard, out, deployment_target, platform):
  """Compiles |storyboard| storyboard to |out| for |deployment_target|."""
  if platform == 'ios':
    subprocess.check_call([
        'ibtool', '--target-device', 'iphone', '--target-device', 'ipad',
        '--auto-activate-custom-fonts', '--minimum-deployment-target',
        deployment_target, '--compilation-directory', out,
        storyboard,
    ])
  elif platform == 'mac':
    subprocess.check_call([
        'ibtool', '--target-device', 'mac', '--auto-activate-custom-fonts', 
        '--minimum-deployment-target', deployment_target, 
        '--compilation-directory', out, storyboard,
    ])

def ParseArgs(argv):
  """Parses command line arguments."""
  parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument(
      'input',
      help='path to the .storyboard file to compile')
  parser.add_argument(
      '-o', '--output', required=True,
      help='path to the result')
  parser.add_argument(
      '-p', '--platform', required=True,
      help='target platform of the .storyboard file to compile')
  parser.add_argument(
      '-t', '--minimum-deployment-target', required=True,
      help='iOS deployment target')

  return parser.parse_args(argv)


def main(argv):
  args = ParseArgs(argv)

  CompileStoryboard(
      os.path.abspath(args.input),
      os.path.dirname(os.path.abspath(args.output)),
      args.minimum_deployment_target,
      args.platform)

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
