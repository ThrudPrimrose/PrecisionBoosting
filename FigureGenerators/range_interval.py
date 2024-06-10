import numpy as np
import sympy as sp
from matplotlib import pyplot as plt


fp32_max = np.finfo(np.float32).max
fp32_min = np.finfo(np.float32).min
fp64_max = np.finfo(np.float64).max
fp64_min = np.finfo(np.float64).min

fp32_interval = sp.Interval(fp32_min, fp32_max)
fp64_interval = sp.Interval(fp64_min, fp64_max)

r_fp32 = fp32_interval.measure
r_fp64 = fp64_interval.measure


print("FP32 Interval:", fp32_interval)
print("FP64 Interval:", fp64_interval)
print("Range of FP32:", r_fp32)
print("Range of FP64:", r_fp64)
print("Factor:", r_fp64 / r_fp32)

# Create a plot
fig, ax = plt.subplots()

plt.plot((fp32_min, fp32_max),(0.1,0.1),'o-',color='orange', label='FP32 Interval')
plt.plot((fp64_min/16.0, fp64_max/16.0),(0,0),'o-',color='orange', label='FP64 Interval')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.tick_params(left=False, bottom=True)

ax.set_yticks([0, 0.1],["fp64", "fp32"])
ax.set_ylim(-0.01, 0.12)
print(fp32_min)
print(fp32_max)
print(fp64_min)
print(fp32_min)
xticks = [fp64_min, fp32_min, 0, fp32_max, fp64_max]
xtick_labels = [f"{fp64_min:.1e}", f"{fp32_min:.1e}", "0", f"{fp32_max:.1e}", f"{fp64_max:.1e}"]
ax.set_xticks(xticks, xtick_labels)
ax.set_xlim(fp64_min/16.0, fp64_max/16.0)

# Show the plot
# plt.show()


print("============")

max_8_bit = 0b11111111
print(max_8_bit)

max_11_bit = 0b11111111111
print(max_11_bit)
print((max_11_bit + 1)/(max_8_bit +1))

max_3_bit = 0b111
print(max_3_bit + 1)


fp32_set = sp.Interval(fp32_min, fp32_max, False, False)
fp64_set = sp.Interval(fp64_min, fp64_max, False, False)

print("Is 0 in FP32 set?", 0 in fp32_set)
print("Is 0 in FP64 set?", 0 in fp64_set)

#print("Cardinality of FP32 set:", fp32_set.cardinality())
#print("Cardinality of FP64 set:", fp64_set.cardinality())

# Define a symbolic representation for the floating-point number
x = sp.Symbol('x')

# Define the range of possible values for the 32-bit floating-point number
float_set = sp.Interval(-sp.Float(2**127), sp.Float(2**127))

print(float_set)

#
import struct

e_len = 4
f_len = 4

ticks = []


# 2 bits can represent
# 0,1,2,3
# -1 offset we have
# -1, 0, 1
# subnormal is when power is -2

interval_start = 0

def create_fp_interval(rb, re, prec, figsize):
    fig, ax = plt.subplots(figsize=figsize)
    # Plot the interval

    interval_end = 2**re
    ax.plot([interval_start, interval_end], [0, 0], color='paleturquoise', linewidth=2.4)

    for i in range(rb,re,1):
        x = 2**i
        this_interval_range = 2**(i+1) - 2**i if 2**(i+1) >= 2**i else 2**i - 2**(i+1)
        ax.plot(x, 0, marker='o', markersize=4, color="red")
        step = this_interval_range / 4.0
        ticks.append(x)
        for j in range(1, prec, 1):
            y = x + j*step
            ticks.append(y)
            ax.plot(y, 0, marker='o', markersize=4, color="orange")


    x = 0
    this_interval_range =  2**(rb) - 0
    ax.plot(x, 0, marker='o', markersize=4, color="green")
    step = this_interval_range / 4.0
    ticks.append(x)
    for j in range(1, prec, 1):
        y = x + j*step
        ticks.append(y)
        ax.plot(y, 0, marker='o', markersize=4, color="lightgreen")

    ticks.append(0)
    ax.plot(0, 0, marker='o', markersize=4, color="black")
    ticks.append(2**re)
    ax.plot(2**re, 0, marker='o', markersize=4, color="black")


    # Set the ticks and tick labels
    ax.set_xticks(ticks)
    ax.set_xticklabels([f'{tick}' for tick in ticks][:-1] + ['+inf'])
    ax.set_ylim(-0.1,0.1)
    ax.set_xlim(interval_start-0.1, interval_end+0.1)
    ax.set_yticks([])
    ax.set_yticklabels([])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.tick_params(left=False, bottom=True)
    plt.xticks(rotation=80)

    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"{rb}_{re}_fp.pdf")

plt.clf()
rb = -1
re =  2
prec = 4
create_fp_interval(rb, re, prec, (6, 1.5))
plt.clf()

# 3 bits, 0,1,2,3,4,5,6,7 -> 0 reserved for subnormal and special val?
# -4,-3,-2,-1,0,1,2,3,
rb = -3
re =  3
prec = 4
create_fp_interval(rb, re, prec, (12, 1.5))
plt.clf()
