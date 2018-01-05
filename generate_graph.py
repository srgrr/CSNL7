def parse_arguments():
  import argparse
  parser = argparse.ArgumentParser(description='Generate random graph')
  parser.add_argument(
    '--vertices', '-v', type = int, default = 1000,
    help = 'Number of vertices'
  )
  parser.add_argument(
   '--type', '-t', type = str, default = 'tree', choices = ['tree', 'bam', 'complete'],
   help = 'Type of graph'
  )
  parser.add_argument(
    '--n0', '-n', type = int, default = 10,
    help = 'Initial vertices in Barabasi-Albert model'
  )
  parser.add_argument(
    '--m0', '-m', type = int, default = 5,
    help = 'Edges per new vertex in Barabasi-Albert model'
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
  ret = np.zeros((args.vertices, args.vertices))
  stubs = []
  # Start with a simple cycle
  for i in range(args.n0):
      j = (i + 1) % args.n0
      ret[i, j] = ret[j, i] = 1
      stubs += [i, j]
  # Add new vertices following the pref attachment rule
  for i in range(args.n0, args.vertices):
      from random import choice
      to_add = set([])
      while len(to_add) < args.m0:
          j = choice(stubs)
          if not j in to_add:
              ret[i, j] = ret[j, i] = 1
              to_add.add(j)
              stubs += [i, j]
  return ret

def generate_complete(args):
    return \
    np.ones((args.vertices, args.vertices)) \
    - np.eye(args.vertices)

def print_graph(g):
  print('%d %.04f'%(g.shape[0], np.linalg.norm(np.max(np.linalg.eig(g)[0]))))
  for row in g:
    print(' '.join(str(x) for x in row))

def store_degseq(g, outp):
    import matplotlib.pyplot as plt
    plt.figure('Degree sequence')
    degseq = [np.sum(x) for x in g]
    plt.hist(degseq)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.savefig('%s.png'%outp)

def main():
  args = parse_arguments()
  type2func = {
    'tree': generate_tree,
    'bam': generate_bam,
    'complete': generate_complete
  }
  g = type2func[args.type](args)
  print_graph(g)
  store_degseq(g, args.type)

if __name__ == "__main__":
  main()
