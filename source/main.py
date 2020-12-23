"""
Copyright 2020 Lihao WANG.

Licensed under Mozilla Public License, version 2.0. You may not use this file except in compliance with the License.
You may obtain a copy of the License at:

https://www.mozilla.org/en-US/MPL/2.0/

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import numpy as np

def f(delta, simu_times):
    a1 = 35
    b1 = 1 / 800
    a2 = 45
    b2 = 1 / 300
    c = 20
    years = 30
    n1 = np.random.poisson(lam=years, size=simu_times)
    n2 = np.random.poisson(lam=years, size=simu_times)
    k = []   # k是方案2中厂商2在第几次博弈时偏离垄断产量
    for i in range(simu_times):
        k_i = np.random.randint(1, n2[i])
        k.append(k_i)

    pi_star = 1 / 9 * ((a1 - c) ** 2 / b1 + (a2 - c) ** 2 / b2)  # 纳什均衡利润π*
    pi_mono = 1 / 8 * ((a1 - c) ** 2 / b1 + (a2 - c) ** 2 / b2)  # 垄断利润π
    pi_p = 9 / 64 * ((a1 - c) ** 2 / b1 + (a2 - c) ** 2 / b2)  # 厂商2采取偏离触发策略时的一次得益πp
    # print(pi_star, pi_mono, pi_p)

    profit_1 = []
    profit_2 = []
    for n1_i in n1:
        profit_1_i = pi_mono * ((1 - delta ** n1_i) / (1 - delta))
        profit_1.append(profit_1_i)

    for n2_i, k_i in zip(n2, k):
        profit_2_i_part_1 = pi_mono * ((1 - delta ** (k_i - 1)) / (1 - delta))    # 厂商2偏离之前的利润
        profit_2_i_part_2 = pi_p * delta ** (k_i - 1)     # 厂商2采取偏离触发策略时的一次得益
        profit_2_i_part_3 = pi_star * ((delta ** k_i) * (1 - delta ** (n2_i - k_i)) / (1 - delta))   # 厂商2偏离之后的利润
        profit_2_i = profit_2_i_part_1 + profit_2_i_part_2 + profit_2_i_part_3
        profit_2.append(profit_2_i)

    return int(round(np.mean(n1))), round(np.mean(profit_1), 3), np.std(profit_1, ddof=1), \
           int(round(np.mean(n2))), int(round(np.mean(k))), round(np.mean(profit_2), 3), round(np.std(profit_2, ddof=1), 3)

simu_times = 100
for delta in range(1, 10):
    delta = delta / 10
    print(delta, *f(delta, simu_times))

