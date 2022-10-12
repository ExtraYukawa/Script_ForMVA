import os
import sys
import optparse
import subprocess
import json
from collections import OrderedDict

if __name__ == '__main__':

  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e', '--era', dest='era', help='[all/2016apv/2016postapv/2017/2018]',default='all',type='string')
  (args,opt) = parser.parse_args()


  Eras_List = ['2016postapv','2016apv','2017','2018']
  Eras = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)

  for era in Eras:
    final_dict = OrderedDict()
    json_directory_path = "data/%s/"%era
    dirs = os.listdir(json_directory_path)
    for f in dirs:
      jsonfile = open(os.path.join(json_directory_path + f))
      samples = json.load(jsonfile, encoding = 'utf-8', object_pairs_hook=OrderedDict).items()
      jsonfile.close()
      for sample, desc in samples:
        final_dict[sample] = desc
  
    json_string = json.dumps(final_dict)
    json_string = json_string.replace(",",",\n").replace("{","{\n ").replace("}","\n}")
    print(json_string)
    with open('input_das_events_%sUL.json'%era, 'w') as outfile:
      outfile.write(json_string)
