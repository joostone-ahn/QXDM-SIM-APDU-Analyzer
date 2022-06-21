import SELECT
debug_mode = 0

def rst(input):
    msg_all, prot_start, prot_end, prot_type, prot_data = input

    sum_rst = []
    for m in range(len(prot_start)):
        sum_time = msg_all[prot_start[m][0]].split('  ')[1].split('  [')[0]
        sum_type = prot_type[m][0]

        if debug_mode: print('')
        if debug_mode: print('sum_time  :',sum_time)
        if debug_mode: print('sum_type  :',sum_type)

        if sum_type != 'TX' and sum_type != 'RX':
            sum_rst.append(sum_time + '  ' + sum_type)
        else:
            sum_ins_1 = prot_data[m][0][2:4]
            sum_sw_1 = prot_data[m][1]

            sum_ins_2 = ''
            sum_sw_2 = ''
            if len(prot_data[m]) > 2:
                sum_ins_2 = prot_data[m][2]
                sum_sw_2 = prot_data[m][-1][-4:]

            if debug_mode: print('sum_ins_1 :',sum_ins_1)
            if debug_mode: print('sum_sw_1  :',sum_sw_1)
            if debug_mode: print('sum_ins_2 :',sum_ins_2)
            if debug_mode: print('sum_sw_2  :',sum_sw_2)

            # if sum_cmd:
            #     sum_rst.append(sum_time + '  ' + sum_cmd)

    return sum_rst

