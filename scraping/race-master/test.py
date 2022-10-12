import numpy as np

horseList = np.random.rand(11,11)
print(horseList)
print(horseList.shape)

for y in 4,5,7,8,9,10:
    std = (horseList[:,y] - np.mean(horseList[:,y]) ) / np.std(horseList[:,y])
#    print(std)
    print(std.shape)
    print("-----")
    new = np.column_stack([horseList,std])
    print(new.shape)
    break
#4,5,7,8,9,10