import sys

def parse_arguments():
  import argparse
  parser = argparse.ArgumentParser(description='Simulate SIS process')
  parser.add_argument(
    'filename', type = str, help = 'Path to input file'
  )
  parser.add_argument(
    '--beta', '-b', type = float, default = 0.1,
    help = 'Probability to infect neighbors'
  )
  parser.add_argument(
    '--gamma', '-g', type = float, default = 0.9,
    help = 'Probability to recover'
  )
  parser.add_argument(
    '--p0', '-p', type = float, default = 0.1,
    help = 'Fraction of initially infected nodes'
  )
  parser.add_argument(
    '--max_iterations', '-m', type = int, default = 10**4,
    help = 'Maximum iterations of the SIS process'
  )
  parser.add_argument(
    '--plot_ratio', '-r', action = 'store_true',
    help = 'Plot results'
  )
  return parser.parse_args()

def parse_graph(filename):
  lines = [x.strip() for x in open(filename, 'r').readlines()]
  n, lambda1 = lines[0].split(' ')
  n = int(n)
  lambda1 = float(lambda1)
  g = []
  for i in range(n): g.append([])
  for i in range(n):
    nums = map(float, lines[i + 1].split(' '))
    for j in range(n):
      if nums[j] > 0:
        g[i].append(j)
  return g, 1.0 / lambda1

def run_simulation(g, args, expname):
  n = len(g)
  initial_amount = int(args.p0 * float(n))
  print('Initial amount: %d' % initial_amount)
  infected = [False] * n
  from random import sample
  initial_infected = sample(list(range(n)), initial_amount)
  for u in initial_infected:
    infected[u] = True
  
  if args.plot_ratio:
    history = [initial_amount / float(n)]

  epidemic = True

  for it in range(args.max_iterations):
    from copy import deepcopy
    from random import random
    old_infected = deepcopy(infected)
    infected_nodes = [x for (x,y) in enumerate(infected) if y]

    for u in infected_nodes:
      for neighb in g[u]:
        if random() <= args.beta:
          infected[neighb] = True

    for i in range(n):
      if old_infected[i] and random() <= args.gamma:
        infected[i] = False

    infected_amount = len([x for x in infected if x])

    if args.plot_ratio:
      history.append(
        1.0 * infected_amount / float(n)
      )

    if infected_amount == 0:
      epidemic = False
      break

  if epidemic:
    print('Infection remained through all the simulation')
  else:
    print('Infection was eradicated in iteration %d'%it)

  if args.plot_ratio:
    import matplotlib.pyplot as plt
    plt.figure('Infected ratio vs timestep')
    plt.xlabel('Timestep')
    plt.ylabel('Infected ratio')
    plt.plot(history)
    plt.savefig('%s_infected_ratio.png'%expname)

def main():
  args = parse_arguments()
  g, lambda1 = parse_graph(args.filename)
  print('Lambda1: %.04f'%lambda1)
  print('Beta / Gamma: %.04f'%(args.beta / args.gamma))
  run_simulation(g, args, args.filename.split('.')[0])


if __name__ == "__main__":
  main()
