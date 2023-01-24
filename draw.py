import matplotlib.pyplot as plt

if __name__ == "__main__":
    x = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5]
    y = [0.177, 0.535, 0.892, 1.251, 1.61, 1.97, 2.32, 2.7, 3.05, 3.41, 3.77, 4.13, 4.49, 4.85, 5.21, 5.52, 5.87, 6.23,
         6.59, 6.94]

    plt.figure(dpi=200)

    plt.plot(x, y)
    plt.tick_params(axis="both", labelsize=6)

    plt.xticks(x)
    plt.yticks(y)

    plt.show()
