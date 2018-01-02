import sys

maximum_iterations = 10000

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
  return g, lambda1

def run_simulation(g, beta, gamma, p0, expname):
  n = len(g)
  initial_amount = int(p0 * float(n))
  print('Initial amount: %d' % initial_amount)
  infected = [False] * n
  from random import sample
  for u in sample(list(range(n)), initial_amount):
    infected[u] = True
  history = [initial_amount / float(n)]

  for _ in range(maximum_iterations):
    from copy import deepcopy
    from random import random
    old_infected = deepcopy(infected)
    infected_nodes = [y for (x,y) in enumerate(infected) if x]

    for u in infected_nodes:
      for neighb in g[u]:
        if random() <= beta:
          infected[neighb] = True

    for i in range(n):
      if old_infected[i] and random() <= gamma:
        infected[i] = False

    history.append(
      1.0 * len([x for x in infected if x]) / float(n)
    )
    if history[-1] == 0:
      print('Infection has been eradicated at iteration %d'%(_+1))
      break

  import matplotlib.pyplot as plt
  plt.figure('Infected ratio vs timestep')
  plt.xlabel('Timestep')
  plt.ylabel('Infected ratio')
  plt.plot(history)
  #plt.scatter(list(range(len(history))), history)
  plt.savefig('%s.png'%expname)

def main():
  filename = sys.argv[1]
  beta, gamma, p0 = map(float, sys.argv[2:])
  g, lambda1 = parse_graph(filename)
  print('Lambda1: %.04f'%lambda1)
  run_simulation(g, beta, gamma, p0, filename.split('.')[0])


if __name__ == "__main__":
  main()
