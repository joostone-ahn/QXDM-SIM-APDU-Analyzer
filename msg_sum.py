import SELECT

def rst(input):
    debug_mode = 0
    msg_all, prot_start, prot_end, prot_type, prot_data = input
    sum_rst = []
    for m in range(len(prot_start)):
        sum_time = msg_all[prot_start[m][0]].split('  ')[1].split('  [')[0]
        sum_type = prot_type[m][0]

        if debug_mode: print('')
        if debug_mode: print('sum_time     :',sum_time)
        if debug_mode: print('sum_type     :',sum_type)

        sum_apdu = []
        apdu_count = 0
        for n in range(len(prot_start[m])):
            apdu_parsing = False
            for a in range(prot_start[m][n], prot_end[m][n]+1):
                if 'APDU Parsing' in msg_all[a]:
                    apdu_parsing = True
                    apdu_count += 1
                if apdu_parsing :
                    if apdu_count == 1:
                        sum_apdu.append(msg_all[a])
            if debug_mode: print('[%d]'%(n+1), prot_start[m][n])
        if debug_mode: print('sum_apdu     :',sum_apdu)
        if debug_mode: print('sum_apdu_cnt :',sum_apdu.count('APDU Parsing'))

        if sum_apdu.count('APDU Parsing') == 0:
            if sum_type != 'TX' and sum_type != 'RX':
                sum_rst.append(sum_time + '  ' + sum_type)
            if sum_type == 'TX':
                sum_rst.append(sum_time + '  ' + 'No Parsing')
        else:
            sum_cmd = sum_apdu[3].replace('  ','')
            if 'incomplete APDU' in sum_cmd:
                sum_cmd = sum_apdu[4].replace('  ','')
            sum_sw = sum_apdu[-2]
            if sum_sw == '  ':
                sum_sw = sum_apdu[-3]

            if debug_mode: print('sum_cmd      :',sum_cmd)
            if debug_mode: print('sum_sw       :',sum_sw)

            sum_rst.append(sum_time + '  ' + sum_cmd)

            # if sum_cmd == 'SELECT':
            #     File_name, File_id = SELECT.process(m + 2, prot_end[n] + 1, msg_all)
            #     sum_rst = SELECT.rst(sum_all, sum_time, Command, File_name, File_id, SW_code)
            # else:
            #     sum_rst.append(sum_time + '  ' + sum_cmd)

    return sum_rst

# def rst(input):
#     msg_all, prot_start, prot_end, prot_type = input
#     msg_sum = []
#     for n in range(len(prot_start)):
#         Time = msg_all[prot_start[n]].split('  ')[1].split('  [')[0]
#         if prot_type[n] == 'RX' or prot_type[n] == 'TX':
#             for m in range(prot_start[n] + 1, prot_end[n] + 1):
#                 if 'Transaction Start' in msg_all[m]:
#                     Command = msg_all[m+2].replace('  ','')
#                     if Command == 'SELECT':
#                         File_name, File_id = SELECT.process(m + 2, prot_end[n] + 1, msg_all)
#                 if 'Status Words' in msg_all[m]:
#                     SW_code = msg_all[m].split('-')[1].split('-')[0].replace('0x', '').replace(' ', '')
#             if Command == 'SELECT':
#                 # print([File_name, File_id, SW_code])
#                 msg_sum = SELECT.rst(msg_sum, Time, Command, File_name, File_id, SW_code)
#             else:
#                 msg_sum.append(Time + '  ' + Command)
#         else:
#             msg_sum.append(Time + '  ' + prot_type[n])
#     return msg_sum

