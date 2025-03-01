# Copyright 2023 The Lynx Authors. All rights reserved.
#

"""
Use metal command to compile a .metal file to .metallib files
"""

import argparse
import os
import subprocess
import sys

def LinkMetal(metal_path, air_path, target, output_path):
  """
  link an .air file to .metallib file
  """
  output = output_path + '/default.metallib'
  command = [metal_path,
             '-target',
             target,
             '-MO',
             '-o',
             output,
             air_path
            ]

  job = subprocess.Popen(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL)
  out, err = job.communicate()
  return job.returncode

def CompileMetal(metal_path, input_path, output_path, include_paths, deps_paths, sysroot, deployment_target, type, target_os):
  """
  compile a .metal file to .dia and .air files
  """
  dir_name, file_name = os.path.split(input_path)
  name, ext = os.path.splitext(file_name)
  dia_path = os.path.join(output_path, name + '.dia')
  air_path = os.path.join(output_path, name + '.air')
  dat_path = os.path.join(output_path, name + '.dat')
  target = 'air64-apple-%s%s' % (target_os, deployment_target)
  if type == 'simulator':
    target = target + '-simulator'
  includes = []
  for include_path in include_paths:
    includes.append('-I'+include_path)
  deps = []
  for deps_path in deps_paths:
    deps.append('-F'+deps_path)

  command = [metal_path,
             '-c',
             '-target',
             target,
             '-gline-tables-only',
             '-frecord-sources',
             '-isysroot',
             sysroot,
             '-serialize-diagnostics',
             dia_path,
             '-o',
             air_path
            ]

  for i in includes:
    command.append(i)
  for d in deps:
    command.append(d)
  command.extend(['-MMD', '-MT', 'dependencies', '-MF'])
  command.append(dat_path)
  command.append(input_path)
  job = subprocess.Popen(command,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL)
  out, err = job.communicate()
  if job.returncode != 0:
    return job.returncode
  return LinkMetal(metal_path, air_path, target, output_path)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--metal-path', help='The path of metal tool')
  parser.add_argument('--input-path', help='The input path of .metal file')
  parser.add_argument('--output-path', help='The output path of build product')
  parser.add_argument('--include-paths', nargs='+', help='Headers search path')
  parser.add_argument('--deps-paths', nargs='+', help='dependencies path')
  parser.add_argument('--sysroot', help='sysroot path')
  parser.add_argument('--minimum-deployment-target', help='minimum deployment target')
  parser.add_argument('--type', help='target type. simulator or device')
  parser.add_argument('--target-os', help='target os. ios or tvos')
  args = parser.parse_args()
  metal_path = args.metal_path
  input_path = args.input_path
  output_path = args.output_path
  include_paths = args.include_paths
  deps_paths = args.deps_paths
  sysroot = args.sysroot
  minimum_deployment_target = args.minimum_deployment_target
  type = args.type
  target_os = args.target_os

  return CompileMetal(metal_path, input_path, output_path, include_paths, deps_paths, sysroot, minimum_deployment_target, type, target_os)

if __name__ == '__main__':
  sys.exit(main())
