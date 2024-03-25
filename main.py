'''from classes.Game import *

if __name__ == '__main__':
  game = Game()
  game.onExecute()'''




from classes.Game import *



def main():
  game = Game()
  game.onExecute()

  

if __name__ == '__main__':
  import cProfile
  
  cProfile.run('main()', 'output.dat')
  
  import pstats
  from pstats import SortKey

  with open('output_time.txt', 'w') as f:
    p = pstats.Stats('output.dat', stream=f)
    p.sort_stats('time').print_stats()

  with open('output_calls.txt', 'w') as f:
    p = pstats.Stats('output.dat', stream=f)
    p.sort_stats('calls').print_stats()
