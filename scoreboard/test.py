total = 1000000
actual = total
for x in range(0, 366):
    total = total * 0.997
    print('   Day:' + str(x) + '         Amount:' + str(total) + '       Diff:' + str(actual - total))