import command
import SELECT
debug_mode = 0

def rst(input):
    msg_all, prot_start, prot_type, prot_data = input

    sum_rst, sum_log_ch, sum_abnormal = [], [], []
    log_ch = [['','']] # log_ch[n] = [current DF, current EF]
    for m in range(len(prot_start)):
        abnormal_msg = ''
        sum_time = msg_all[prot_start[m][0]].split('  ')[1].split('  [')[0]
        sum_type = prot_type[m][0]

        if sum_type != 'TX' and sum_type != 'RX': # RESET, ATR
            sum_rst.append(sum_time + '  ' + sum_type)
            sum_log_ch.append(['',''])
        else: # sum_type == 'TX'
            if len(prot_data[m][-1]) >= 4:
                sum_sw = prot_data[m][-1][-4:]
            else:  # Incomplete APDU
                sum_sw = ''

            if prot_data[m][0][0] == '4':  # ETSI ts102.221 Table 10.4a extended logical channels
                log_ch_id = int(prot_data[m][0][1]) + 16  # excluding 00~0F
            else:
                log_ch_id = int(prot_data[m][0][1])
            if log_ch_id > len(log_ch) - 1:
                for n in range(log_ch_id - len(log_ch) + 1):
                    log_ch.append(['',''])

            sum_ins = prot_data[m][0][2:4]
            if sum_ins in command.cmd_name:
                sum_cmd = command.cmd_name[sum_ins]
                if sum_cmd == 'SELECT':
                    if sum_sw != '':
                        log_ch, file_name, abnormal_msg = SELECT.process(prot_data[m], log_ch, log_ch_id)
                    else:
                        file_name = ' [N/A]'
                        abnormal_msg = '(3) Incomplete APDU'
            else:
                sum_cmd = 'Unknown INS [%s]'%sum_ins

            if debug_mode == 1:
                print('sum_time   :', sum_time)
                print('sum_type   :', sum_type)
                print('sum_ins    :', sum_ins)
                print('sum_cmd    :', sum_cmd)
                print('sum_sw     :', sum_sw)
                print('')

            sum_rst.append(sum_time + '  ' + sum_cmd)
            if sum_cmd == 'SELECT': sum_rst[-1] += file_name

            if sum_sw == '9000' or sum_ins[0] == '2':  # PIN CMD
                sum_log_ch.append(log_ch[log_ch_id][0:2])
            else:
                sum_log_ch.append(sum_log_ch[-1])

            sum_abnormal.append(abnormal_msg)

        if debug_mode == 2:
            print('sum_rst    :', sum_rst[-1])
            print('prot_data  :', prot_data[m])
            print('log_ch     :', log_ch)
            print('sum_log_ch :', sum_log_ch[-1])
            print()

    return sum_rst, sum_log_ch, sum_abnormal

