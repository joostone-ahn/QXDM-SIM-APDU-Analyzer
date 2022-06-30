debug_mode = 0

def process(ins, file_name, data, sum_read, sum_remote, sum_remote_list):

    file_name = file_name.replace('[', '').replace(']', '')

    if ins == 'B0':
        sum_read.append([data[1][2:-4]])
        P2 = data[0][6:8].zfill(2)
        Le = data[0][8:10].zfill(2)
        sum_read[-1].append([P2,Le]) # sum_read[n][2] = [offset low, Number of bytes to be read]

        if file_name in sum_remote_list:
            ind = sum_remote_list.index(file_name)
            if data[1][2:-4] != sum_remote[ind][-1]:
                sum_remote[ind].append(data[1][2:-4])
                if debug_mode: print(sum_remote[ind])

    elif ins == 'B2':
        sum_read.append([data[1][2:-4]]) # sum_read[n][0] = file_name, sum_read[n][1] = file_data
        P1 = data[0][4:6].zfill(2)
        P2 = format(int(data[0][6:8], 16), 'b').zfill(8)  # ts102.221 table 11.11 Coding of P2
        if P2[-3:] == '100':
            sum_read[-1].append(P1) # sum_read[n][2] = record_num
        elif P2[-3:] == '010':
            sum_read[-1].append('Next')
        elif P2[-3:] == '011':
            sum_read[-1].append('Previous')
        Le = data[0][8:10].zfill(2)
        sum_read[-1].append(Le) # sum_read[n][3] = record length

        file_name = file_name + ' [%s]'%P1
        if file_name in sum_remote_list:
            ind = sum_remote_list.index(file_name)
            if data[1][2:-4] != sum_remote[ind][-1]:
                sum_remote[ind].append(data[1][2:-4])
                if debug_mode: print(sum_remote[ind])

    return sum_read, sum_remote

def init():
    sum_remote = []
    sum_remote.append(['MSISDN [01]'])
    sum_remote.append(['IMSI'])
    sum_remote.append(['ACC'])
    sum_remote.append(['IMPI'])
    sum_remote.append(['IMPU [01]'])
    sum_remote.append(['IMPU [02]'])
    sum_remote.append(['IMPU [03]'])
    sum_remote.append(['HPLMNwAcT'])
    sum_remote.append(['SUCI_Calc_Info'])
    sum_remote.append(['Routing_Indicator'])

    sum_remote_list = []
    for n in sum_remote:
        sum_remote_list.append(n[0])

    return sum_remote, sum_remote_list