def parse_arguments():
  import argparse
  parser = argparse.ArgumentParser(description='Generate random graph')
  parser.add_argument(
    '--vertices', '-v', type = int, default = 1000,
    help = 'Number of vertices'
  )
  parser.add_argument(
   '--type', '-t', type = str, default = 'tree', choices = ['tree', 'bam'],
   help = 'Type of graph'
  )
  return parser.parse_args()


import numpy as np
def generate_tree(args):
  ret = np.zeros((args.vertices, args.vertices))
  for i in range(1, args.vertices):
    from random import randint
    j = randint(0, i - 1)
    ret[i, j] = ret[j, i] = 1
  return ret

def generate_bam(args):
  pass

def print_graph(g):
  print('%d %.04f'%(g.shape[0], np.max(np.linalg.eig(g)[0])))
  for row in g:
    print(' '.join(str(x) for x in row))

def main():
  args = parse_arguments()
  type2func = {
    'tree': generate_tree,
    'generate_bam': generate_bam
  }
  g = type2func[args.type](args)
  print_graph(g)


if __name__ == "__main__":
  main()
