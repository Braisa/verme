import numpy as np
import matplotlib.pyplot as plt

rho = 1
a = 0.5
W = 0.01
M = W / 1.42953

x = lambda l : 2*(np.abs(l) - a)/(np.pi*M)
r = lambda l : rho + np.heaviside(np.abs(l)/a -1, 1) * M * (x(l)*np.arctan(x(l)) - .5*np.log(1+x(l)**2))


fig, ax = plt.subplots()

l_lin = np.linspace(0.95*a, 1.3*a, 1000)
rs_lin = np.linspace(0, 1.3*a - a, 1000)

ax.plot(l_lin - a, r(l_lin) - rho, ls = "solid", color = "tab:orange", label = "Burato de verme")
ax.plot(rs_lin, rs_lin - 2*M, ls = "dashed", color = "tab:blue", label = "Schwarzschild")

ax.legend(loc = "best")

ax.set_xticks(np.array((0.95*a, 1.0*a, 1.1*a, 1.2*a, 1.3*a, 2*M + a)) - a)
ax.set_xticklabels(("-0.05a", "0", "0.1a", "0.2a", "0.3a", "2M"))

ax.set_xlabel(r"$|l| - a$")
ax.set_ylabel(r"$r(l) - \rho$")

ax.set_xlim(left = np.min(-.05*a), right = np.max(rs_lin))
ax.set_ylim(bottom = -2*M)

fig.savefig("results/metric_comparison.pdf", dpi = 300, bbox_inches = "tight")
