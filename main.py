import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import csv

#plt.style.use('dark_background')

def csv_reader(filename):
    """
    Read a csv file
    """
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row)
        return data

def csv_writer(data, filename):
    """
    Write data to a CSV file path
    """
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for row in data:
            writer.writerow(row)
data = csv_reader('time_series_covid19_confirmed_global.csv')
ans = []
count_sec = 0
count_zero = 0
count_us = 0
count_sp = 0

test = [212,150,133,249,70,78]

for o in range(1, len(data)):
    confirmed = data[o][:2] + data[o][4:]
    # 212 - RUSSIA
    # 150 - Ireland
    # 133 - Germany
    # 250 - Ukraine
    # 70 - China, Henan
    # 78

    if (confirmed[0] != ''):
        country = confirmed[0] + ', ' + confirmed[1]
    else:
        country = confirmed[1]

    confirmed = list(map(int, confirmed[2:]))
    #print(len(confirmed), country)
    #print(confirmed)


    def find_coef_for_quad_function(x_start, x_end):
        n = x_end-x_start
        a11 = 0
        X = range(x_start, x_end)
        for i in X:
            a11 += i**2
        a12 = 0
        for i in X:
            a12 += i
        a13 = n
        a21 = 0
        for i in X:
            a21 += i ** 3
        a22 = 0
        for i in X:
            a22 += i ** 2
        a23 = 0
        for i in X:
            a23 += i
        a31 = 0
        for i in X:
            a31 += i ** 4
        a32 = 0
        for i in X:
            a32 += i ** 3
        a33 = 0
        for i in X:
            a33 += i ** 2
        b1 = 0
        for i in X:
            b1 += confirmed[i]
        b2 = 0
        for i in X:
            b2 += confirmed[i]*i
        b3 = 0
        for i in X:
            b3 += confirmed[i]*i*i
        AA = np.array([[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]])
        BB = np.array([b1,b2,b3])
        return np.linalg.solve(AA, BB)[0], np.linalg.solve(AA, BB)[1], np.linalg.solve(AA, BB)[2]

    #plt.xlabel('Day')
    #plt.ylabel('Leap')
    #plt.title(country)
    #plt.plot(range(x_start, x_end), confirmed[x_start:x_end], range(x_start,x_end), [quad(a, b, c, i) for i in range(x_start, x_end)])
    #plt.show()
    X_tmp = []
    Y_tmp1 = []
    Y_tmp2 = []
    m = -99999999999999999
    i = 0
    while ((i + 2) * 7 + 5 < len(confirmed)):
        x_start = i * 7 + 5
        x_end = (i+2) * 7 + 5
        a, b, c = find_coef_for_quad_function(x_start, x_end)
        #print(a, b)
        X_tmp.append((2*i+1)*7/2+8.5)
        Y_tmp1.append(2*a*((2*i+1)*7/2+8.5)+b)
        Y_tmp2.append(a*2)
        m = max(m, abs(a*2))
        i += 1
    #Y_tmp2 = list(map(lambda x: x/m, Y_tmp2))

    #print(X_tmp)
    #print(Y_tmp1)
    #print(Y_tmp2)
    col1 = 0# высокое ускорение
    col2 = 0# текущее ускорение
    col3 = 0# текущая скорость
    col4 = 0# есть ли 2 волна?
    col5 = 0# остановилось ли заражение?
    Y_tmp3 = []
    for i in range(len(Y_tmp2)):
        Y_tmp3.append(Y_tmp2[i]/m)
        if(Y_tmp3[i] >= 0.5):
            Y_tmp3[i] = 1
        elif(Y_tmp3[i] >= -0.5):
            Y_tmp3[i] = 0
        else:
            Y_tmp3[i] = -1
    for i in range(len(Y_tmp3)-1):
        if (Y_tmp3[i] == 0 and Y_tmp3[i+1] == 1):
            col1 += 1
    count_tmp = 0
    tmp = confirmed[-1]
    for i in range(len(confirmed)-2, -1, -1):
        if(tmp == confirmed[i]):
            count_tmp += 1
            tmp = confirmed[i]
        if (count_tmp >= 14):
            col5 = 1
        else:
            col5 = 0
    col2 = round(Y_tmp2[-1], 2)
    col3 = round(Y_tmp1[-1], 2)
    if (col1 >= 2):
        col4 = 1
    else:
        col4 = 0


    ans.append([country,col1,col2,col3,col4,col5])

    count_sec += col4
    count_zero += col5
    count_us += col2
    count_sp += col3



    #plt.plot(X_tmp, Y_tmp2)
    #print(Y_tmp2)


    #plt.plot(range(len(confirmed)), confirmed)
    #plt.grid()
    #plt.show()

ans.append(['total', 0, round(count_us), round(count_sp), count_sec, count_zero])
csv_writer(ans, 'ans.csv')