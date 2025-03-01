# Copyright 2022 The Lynx Authors. All rights reserved.

import argparse
import collections
import logging
import json
import os
import sys

def read_json_file(file_path):
  with open(file_path, 'r') as file:
    data = file.read()
  content = json.loads(data, object_pairs_hook=collections.OrderedDict)
  return content

def append_content_to_subspec(source_content, subspec_content, key):
  if key in source_content:
    source_result = source_content[key]
    if not key in subspec_content:
      if isinstance(source_result, list):
        source_result.sort()
      subspec_content[key] = source_result
    else:
      subspec_result = subspec_content[key]
      if isinstance(subspec_result, str):
        tmp_result = [subspec_result]
        if isinstance(source_result, str):
          tmp_result.append(source_result)
        elif isinstance(source_content, list):
          tmp_result.extend(source_result)
        subspec_content[key] = tmp_result
      elif isinstance(subspec_result, list):
        if isinstance(source_result, str):
          subspec_result.append(source_result)
        elif isinstance(source_result, list):
          subspec_result.extend(source_result)
        else:
          print("---%s" % (type(source_result)))
        subspec_result.sort()
      else:
        print("****%s - %s" % (subspec_result, key))
        # raise Exception('not support type %s' % (type(subspec_result)))
  return subspec_content

def format_dependencies(source_content):
  if not 'dependencies' in source_content:
    return source_content
  deps = source_content['dependencies']
  deps_map = {}
  for dep in deps:
    deps_map[dep] = []
  source_content['dependencies'] = deps_map
  return source_content

def find_target_subspec(name, subspecs):
  for subspec in subspecs:
    subspec_name = subspec['name']
    if subspec_name == None:
      return None
    if name == subspec_name:
      return subspec
  return None


def merge_podspec_file(base_file_path, root_path, output_path, check_module, module_name):
  base_content = read_json_file(base_file_path)
  if not 'subspecs' in base_content:
    logging.error('can not find subspecs in base file')
    return -1
  for root, dir_list, file_list in os.walk(root_path):
    for file_name in file_list:
      subspecs = base_content['subspecs']
      fullname = os.path.join(root, file_name)
      json_content = read_json_file(fullname)

      if check_module:
        if not 'module_name' in json_content:
          continue
        module = json_content['module_name']
        module_list = module.split('-')
        if not module_name in module_list:
          continue
      json_content.pop('module_name')

      if not 'parent_path' in json_content:
        logging.error('can not find parent path in file:%s' % (fullname))
        return -1
      parent_path = json_content['parent_path']
      path_list = parent_path.split('-')
      if len(path_list) > 1:
        for subspec_path in path_list[1:]:
          subspec = find_target_subspec(subspec_path, subspecs)
          if subspec == None:
            target = {}
            target['name'] = subspec_path
            target['subspecs'] = []
            subspecs.append(target)
            subspecs = target['subspecs']
          else:
            if not 'subspecs' in subspec:
              subspec['subspecs'] = []
              subspecs = subspec['subspecs']
            else:
              subspecs = subspec['subspecs']

      name = json_content['name']
      if name == None:
        logging.error('can not find name in file:%s' % (fullname))
        return -1
      json_content.pop('parent_path')
      json_content = format_dependencies(json_content)
      find_subspec = False
      for subspec in subspecs:
        if not 'name' in subspec:
          logging.error('can not find name in subspec_name')
          return -1
        subspec_name = subspec['name']
        if subspec_name == name:
          find_subspec = True
          subspec = append_content_to_subspec(json_content, subspec, 'compiler_flags')
          subspec = append_content_to_subspec(json_content, subspec, 'dependencies')
          subspec = append_content_to_subspec(json_content, subspec, 'exclude_files')
          subspec = append_content_to_subspec(json_content, subspec, 'frameworks')
          subspec = append_content_to_subspec(json_content, subspec, 'header_mappings_dir')
          subspec = append_content_to_subspec(json_content, subspec, 'libraries')
          subspec = append_content_to_subspec(json_content, subspec, 'pod_target_xcconfig')
          subspec = append_content_to_subspec(json_content, subspec, 'preserve_paths')
          subspec = append_content_to_subspec(json_content, subspec, 'private_header_files')
          subspec = append_content_to_subspec(json_content, subspec, 'public_header_files')
          subspec = append_content_to_subspec(json_content, subspec, 'source_files')
          break
      if not find_subspec:
        subspecs.append(json_content)

  result = json.dumps(base_content, indent=2, separators=(',', ':'))
  with open(output_path, 'w') as file:
    file.write(result)
      
  return 0

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--base_file_path')
  parser.add_argument('-c', '--check_module', type=bool, default=False)
  parser.add_argument('-m', '--module_name', type=str, default='')
  parser.add_argument('-r', '--root_path')
  parser.add_argument('-o', '--output_path')
  args = parser.parse_args()
  base_file_path = args.base_file_path
  check_module = args.check_module
  module_name = args.module_name
  root_path = args.root_path
  output_path = args.output_path
  result = merge_podspec_file(base_file_path, root_path, output_path, check_module, module_name)
  return result

if __name__ == '__main__':
  sys.exit(main())
