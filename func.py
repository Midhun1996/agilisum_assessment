# write a function to print the alphbets no of time the leading numbers for eg: 'A2B4' -> 'AABBBB'

import re

def printalp(x):
  d = re.split('[A-Z]',x)
  alpha = [e for e in x if e.isalpha()]
  result = [] 
  for al,rep in zip(alpha,d[1:]):
    out = [str(al) for _ in range(int(rep))]
    result.extend(out)
  return "".join(result)




def printalp_1(x,defalut_rep=1):
  d = re.split('[A-Z]',x)
  alpha = [e for e in x if e.isalpha()]
  result = [] 
  for al,rep in zip(alpha,d[1:]):
    if rep == '':
      out = [str(al) for _ in range(defalut_rep)]
      result.extend(out)
      continue
    out = [str(al) for _ in range(int(rep))]
    result.extend(out)
  return "".join(result)
