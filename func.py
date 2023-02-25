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

# last one most suitable and readable

# without default value

def print_seq1(seq):
  alp = seq[0::2]
  rep = seq[1::2]
  result = [v*int(r) for v,r in zip(alp,rep)]
  return "".join(result)

# with default value

def print_seq(string,rep=1):
  result = []
  for e,v in enumerate(string):
    if v.isalpha():
      try:
        val = v * int(string[e+1])
        result.append(val)
      except Exception as e:
        val = v * rep
        result.append(val)
  else:
    return "".join(result)