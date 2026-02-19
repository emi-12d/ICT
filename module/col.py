import pandas as pd
import copy

def kake():
  col = []
  ind = []
  for i in range(1,10):
    for j in range(1,10):
      col.append(i * j)
    ind.append(copy.copy(col))
    col.clear()
  df = pd.DataFrame(ind)
  df.index = [i for i in range(1, 10)]
  df.columns = [i for i in range(1, 10)]
  yield df

