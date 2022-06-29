def process(ins, file_name, data, sum_read):
    if ins == 'B0':
        sum_read.append([file_name, data[1][2:-4]])
    elif ins == 'B2':
        sum_read.append([file_name, data[1][2:-4]])
        P1 = data[0][4:6].zfill(2)
        P2 = format(int(data[0][6:8], 16), 'b').zfill(8)  # ts102.221 table 11.11 Coding of P2
        if P2[-3:] == '100':
            sum_read[-1].append(P1)
        elif P2[-3:] == '010':
            sum_read[-1].append('Next')
        elif P2[-3:] == '011':
            sum_read[-1].append('Previous')
    else:
        sum_read.append(['', ''])
    return sum_read