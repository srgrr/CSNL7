
def parse_arguments():
  import argparse
  parser = argparse.ArgumentParser(description = 'Do SIS simulations with different beta and gamma ratios')
  parser.add_argument(
    'filename', type = str, help = 'Path to input file'
  )
  parser.add_argument(
    '--reps', '-r', type = int, help = 'Repetitions per combination',
    default = 10
  )
  parser.add_argument(
    '--stepsize', '-s', type = float, help = 'Step size for beta',
    default = 0.05
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

def simulate(args, beta, gamma):
  from subprocess import check_output
  ret = 0
  for i in range(args.reps):
    output = check_output( \
      ['python', 'simulate.py', args.filename, '--beta', str(beta), '--gamma', str(gamma), '--max_iterations', '1000'] \
    ).decode('utf-8')
    if not 'eradicated' in output:
      ret += 1

  return ret / float(args.reps)

def main():
  args = parse_arguments()
  _, lambda1 = parse_graph(args.filename)
  import matplotlib.pyplot as plt
  plt.figure('Beta/gamma vs epidemic rate')
  plt.xlabel('Beta/gamma ratio')
  plt.ylabel('Epidemic rate')
  beta = 0.00
  plotx, ploty = [], []
  one = 0
  while beta <= 1.0 and one < 3:
    plotx.append(beta / 0.9)
    ploty.append(simulate(args, beta, 0.9))
    if ploty[-1]: 
      one += 1
    beta += args.stepsize
  plt.plot(plotx, ploty, color = 'blue')
  plt.scatter(plotx, ploty)
  plt.ylim([-0.05, 1.05])
  plt.plot([lambda1, lambda1], [-0.05, 1.05], color = 'red')
  plt.savefig('%s_epidemic.png'%args.filename)

if __name__ == "__main__":
  main()
