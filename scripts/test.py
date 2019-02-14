import pandas as pd
from scipy import stats

est = [6507.75700934579,6523.17757009346,6653.08411214953,6664.29906542056,6751.68224299065,6446.54205607477,5926.44859813084,6740,6808.22429906542,6679.93364485981,6561.40560747663,6617.96728971963,5791.64672897196,5242.76822429907,6476.78364485981,6505.0761682243,6485.79439252336,6556.35514018692,6472.71028037383,6033.4579439253,5435.79439252336,7135.32710280374,7347.47663551402,7128.83738317757,6900.83224299065,6747.44719626168,6444.20560747664,5813.83177570093,7233.92523364486,7197.94392523364,7109.6261682243]
pred = [6482.00514098, 6652.59438229, 6527.92706015, 6619.03445409, 6552.45279429, 6601.11094628, 6565.55136783, 6591.53845463, 6572.54698426, 6586.42602925, 6576.28316585, 6583.69561232, 6578.27856582, 6582.23736577, 6579.34425842, 6581.45855322, 6579.91341784, 6581.04260916, 6580.21739148, 6580.82046397, 6580.37973611, 6580.70182185, 6580.46644026, 6580.6384581, 6580.51274675, 6580.60461712, 6580.53747787, 6580.58654351, 6580.55068614, 6580.57689086]

print(len(est))

print(len(pred))

sum = []

for idx, el in enumerate(pred):
    sum.append(abs(1-el/est[idx]))
    print(idx,abs(1-el/est[idx]))

#print(stats.hmean(sum))
#print(sum)