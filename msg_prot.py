def process(input):
    exe_start, exe_end, exe_type, exe_data = input

    prot_start, prot_end, prot_type, prot_data = [],[],[],[]
    prot_start_item, prot_end_item, prot_type_item, prot_data_item = [],[],[],[]

    for n in range(len(exe_start)):
        if exe_type[n] != 'TX' and exe_type[n] != 'RX':
            prot_start.append([exe_start[n]])
            prot_end.append([exe_end[n]])
            prot_type.append([exe_type[n]])
            prot_data.append([exe_data[n]])
        else:
            if exe_type[n] == 'TX' and len(exe_data[n]) == 10:
                if prot_data_item:
                    if exe_data[n][2:4] != 'C0':
                        prot_start.append(prot_start_item)
                        prot_end.append(prot_end_item)
                        prot_type.append(prot_type_item)
                        prot_data.append(prot_data_item)
                        prot_start_item, prot_end_item, prot_type_item, prot_data_item = [],[],[],[]
            prot_start_item.append(exe_start[n])
            prot_end_item.append(exe_end[n])
            prot_type_item.append(exe_type[n])
            prot_data_item.append(exe_data[n])
            # print("item", prot_data_item)
        # print("list", prot_data)
    return prot_start, prot_end, prot_type, prot_data


def rst(input):
    debug_mode = 0
    msg_all, prot_start, prot_type, prot_data, item_num = input
    start = prot_start[item_num]
    type = prot_type[item_num]
    data = prot_data[item_num]

    prot_rst = []
    if data[0]:
        for n in range(len(data)):
            rst_time = msg_all[start[n]].split('  ')[1].split('  [')[0]
            if 'RX' in type[n]: rst_type = '[RX]'
            elif 'TX' in type[n]: rst_type = '[TX]'
            rst_data = ''
            for m in range(len(list(data[n]))):
                if m%2 ==0 : rst_data += list(data[n])[m]
                else: rst_data += list(data[n])[m] + ' '
            prot_rst.append(rst_time + '  ' + rst_type + '  ' + rst_data)

            if debug_mode:
                print('rst_time :', rst_time)
                print('rst_type :', rst_type)
                print('rst_data :', rst_data)
                print()

    return prot_rst