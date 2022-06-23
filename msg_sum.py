import apdu_parsing
debug_mode = 2

def rst(input):
    msg_all, prot_start, prot_type, prot_data = input

    sum_rst = []
    for m in range(len(prot_start)):

        sum_time = msg_all[prot_start[m][0]].split('  ')[1].split('  [')[0]
        sum_type = prot_type[m][0]

        if sum_type != 'TX' and sum_type != 'RX':
            sum_rst.append(sum_time + '  ' + sum_type)
        else: # sum_type == 'TX'
            sum_ins = prot_data[m][0][2:4]

            if sum_ins in apdu_parsing.cmd_name:
                sum_cmd = apdu_parsing.cmd_name[sum_ins]
                sum_detail = apdu_parsing.process(prot_data[m], sum_cmd)
            else:
                sum_cmd = 'Unknown INS'
                sum_detail = "'%s'"%sum_ins

            sum_rst.append(sum_time + '  ' + sum_cmd)
            if sum_detail != '' : sum_rst[-1] += ' (' + sum_detail + ')'

            # (TBD) R-APDU Analysis
            if len(prot_data[m][-1]) >= 4:
                sum_sw = prot_data[m][-1][-4:]
            else:  # ERROR
                sum_sw = ''
                sum_rst[-1] += ' (incomplete)'
            if sum_sw != '9000': sum_rst[-1] += ' ***'

            if debug_mode == 1:
                print('sum_time   :', sum_time)
                print('sum_type   :', sum_type)
                print('sum_ins    :', sum_ins)
                print('sum_cmd    :', sum_cmd)
                print('sum_detail :', sum_detail)
                print('sum_sw     :', sum_sw)
                print('')

            if debug_mode == 2: # SELECTED FILE ID LIST
                if sum_ins == 'A4':
                    if len(prot_data[m]) > 2:
                        print(prot_data[m][2])

    return sum_rst

