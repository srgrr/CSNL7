import argparse


def main():
  import subprocess
  # Generate graphs, and their degree sequences
  '''
  pbam = subprocess.Popen(['python', 'generate_graph.py', '--type', 'bam'],
  stdout = open('bam.txt', 'w'))
  ptree = subprocess.Popen(['python', 'generate_graph.py', '--type', 'tree'],
  stdout = open('tree.txt', 'w'))
  pcomplete = subprocess.Popen(['python', 'generate_graph.py', '--type', 'complete'],
  stdout = open('complete.txt', 'w'))
  pbam.wait()
  ptree.wait()
  pcomplete.wait()

  # Simulate for the fixed parameter set
  pbam1 = subprocess.Popen(['python', 'simulate.py', 'bam.txt', '--plot_ratio'])
  ptree1 = subprocess.Popen(['python', 'simulate.py', 'tree.txt', '--plot_ratio'])
  pcomplete1 = subprocess.Popen(['python', 'simulate.py', 'complete.txt', '--plot_ratio'])
  '''
  # Simulate for epidemic threshold
  pbam2 = subprocess.Popen(['python', 'progress.py', 'bam.txt', '--stepsize', '0.01'])
  ptree2 = subprocess.Popen(['python', 'progress.py', 'tree.txt', '--stepsize', '0.01'])
  pcomplete2 = subprocess.Popen(['python', 'progress.py', 'complete.txt', '--stepsize', '0.01'])

  #pbam1.wait();
  pbam2.wait();
  #ptree1.wait();
  ptree2.wait();
  #pcomplete1.wait();
  pcomplete2.wait();

if __name__ == "__main__":
  main()
