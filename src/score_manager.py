import csv
from operator import itemgetter

def read_scores(file_path='scores.csv'):
  try:
    with open(file_path, mode='r', newline='') as csvfile:
      reader = csv.reader(csvfile)
      return sorted([row for row in reader], key=itemgetter(1), reverse=True)
  except FileNotFoundError:
    return []
  
def write_scores(scores, file_path='scores.csv'):
  with open(file_path, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(scores)