import apdu_parsing
import SELECT
debug_mode = 1

def rst(input):
    msg_all, prot_start, prot_end, prot_type, prot_data = input

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
                sum_detail = apdu_parsing.process(msg_all, prot_start, prot_end, prot_data)
            else:
                sum_cmd = "Unknown (INS '%s')"%sum_ins

            if len(prot_data[m][-1]) >= 4:
                sum_sw = prot_data[m][-1][-4:]
            else: # ERROR
                sum_sw = ''
                sum_detail = '(incomplete)'

            sum_rst.append(sum_time + '  ' + sum_cmd)
            if sum_detail != '' : sum_rst[-1] += ' ' + sum_detail
            if sum_sw != '9000':
                sum_rst[-1] += ' ***'

            if debug_mode:
                print('sum_time :', sum_time)
                print('sum_type :', sum_type)
                print('sum_ins  :', sum_ins)
                print('sum_cmd  :', sum_cmd)
                print('sum_sw   :', sum_sw)
                print('')

    return sum_rst

