import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import linalg
from lib.plot_tools import to_precision, autolabel

def solve():
# Component failure rates and repair rate
  comp_rep_rate = 26        # 2 weeks' time
  sys_rep_rate =  365.25     # 1 days' time
  component_rate = 0.333  # 
  psu_rate = 0.2

# Subsystem failure rates
  _1Aor1B = component_rate
  _2A = component_rate
  _2B = component_rate
  _2Cor2D = component_rate
  _2Cor2Dor2B = component_rate
  _2Cor2Dor2A = component_rate

# Equations
  e1  = [ _1Aor1B + _2A + _2B + _2Cor2D + psu_rate + comp_rep_rate, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, comp_rep_rate -sys_rep_rate]
  e2  = [ -_2A, _1Aor1B + _2B + _2Cor2D + psu_rate + comp_rep_rate, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  e3  = [-_2B, 0, _1Aor1B + _2A + _2Cor2D + psu_rate + comp_rep_rate, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  e4  = [-_1Aor1B, 0, 0,  + psu_rate + comp_rep_rate, 0, 0, 0, 0, 0, 0, 0, 0]
  e5  = [-_2Cor2D, 0, 0, 0, _2A + _2B + _1Aor1B + psu_rate + comp_rep_rate, 0, 0, 0, 0, 0, 0, 0]
  e6  = [0, -_2B, -_2A, 0, 0, _1Aor1B + _2Cor2D + psu_rate + comp_rep_rate, 0, 0, 0, 0, 0, 0]
  e7  = [0, -_2A, 0, -_1Aor1B, 0, 0, _2Cor2Dor2B + psu_rate + comp_rep_rate, 0, 0, 0, 0, 0]
  e8  = [0, 0, -_1Aor1B, -_2B, 0, 0, 0, _2Cor2Dor2A + psu_rate + comp_rep_rate, 0, 0, 0, 0]
  e9  = [0, -_2Cor2D, 0, 0, -_2A, 0, 0, 0, _1Aor1B + _2B + psu_rate + comp_rep_rate, 0, 0, 0]
  e10 = [0, 0, -_2B, 0, -_2Cor2D, 0, 0, 0, 0, _1Aor1B + _2A + psu_rate + comp_rep_rate, 0, 0]
  e11 = [0, 0, 0, 0, 0, -_2Cor2D, 0, 0, -_2B, -_2A, _1Aor1B + psu_rate + comp_rep_rate, 0]
  e12 = [0, 0, 0, _2Cor2D, 0, _1Aor1B, _2Cor2Dor2B, _2Cor2Dor2A, _1Aor1B, _1Aor1B, _1Aor1B, -sys_rep_rate]
  e13 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  Bprime = [comp_rep_rate, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -psu_rate, 1]

# Set up our matrices in the form Ax = B
  A = np.array([ e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e13 ])

  B = np.array([comp_rep_rate, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
  validation_set = [0.9296, 0.01112, 0.01112, 0.02507, 0.02507, 0.0002692, 
         0.0005482, 0.0005482, 0.0005482, 0.0005482, 0.00002028, 0.000635] # From the author's analysis

# Solve for state probabilities
  LU = linalg.lu_factor(A)
  P = linalg.lu_solve(LU, B)

# Plot results
  labels = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12']
  bar_width = 0.5
  fig, ax = plt.subplots()
  rects1 = ax.bar(np.arange(len(labels)) - bar_width/2, P, bar_width, label='result')
  rects2 = ax.bar(np.arange(len(labels)) + bar_width/2, validation_set, bar_width, label='validation_set')

# Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel('Percentage Time in State')
  ax.set_title('Gross Dependability Analysis')
  ax.set_xticks(np.arange(len(labels)))
  ax.set_xticklabels(labels)
  ax.set_yscale('log')
  ax.legend()
  autolabel(rects1, ax)
  autolabel(rects2, ax)

  plt.rcParams['figure.figsize'] = [16, 8]
  plt.show()

if __name__ == "__main__":
    solve()
