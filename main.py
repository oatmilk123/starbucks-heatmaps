import matplotlib.pyplot as plt
import calendar

data = []

max_data, min_data = max(data), min(data)

days = list(range(1, 32))
months = list(calendar.month_name)[1:]

month_lens = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


start = 0
monthly_subsets = []
for i in month_lens:
    current_subset = data[start : start + i]
    if len(current_subset) < 31:
        current_subset += [0] * (31 - len(current_subset))
    monthly_subsets.append(current_subset)
    start += i

figure, axes = plt.subplots(figsize=(14, 8))
image = axes.imshow(monthly_subsets, cmap="Oranges")

axes.set_xticks(range(len(days)), days)
axes.set_yticks(range(len(months)), months)


cbar = figure.colorbar(image, ticks=[min_data, max_data], orientation="horizontal")
cbar.ax.set_xticklabels([min_data, max_data])

font = {"family": "serif", "color": "black", "size": 25}
cbar.set_label("Number of tweets about the drink (per day)", fontdict=font)
axes.set_title("How popular was the Caramel Brulée in 2022?", fontdict=font)

plt.xlabel("Days", fontdict=font)
plt.ylabel("Months", fontdict=font)
figure.tight_layout()
plt.savefig("heat_brulee.png")