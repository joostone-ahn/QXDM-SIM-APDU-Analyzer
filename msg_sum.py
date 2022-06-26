import command
import SELECT
debug_mode = 0

def rst(input):
    msg_all, prot_start, prot_type, prot_data = input

    sum_rst, sum_log_ch, sum_log_ch_id, sum_abnormal = [], [], [], []
    log_ch = [['','']] # log_ch[n] = [current DF, current EF]
    for m in range(len(prot_start)):
        abnormal_msg = ''
        time = msg_all[prot_start[m][0]].split('  ')[1].split('  [')[0]
        type = prot_type[m][0]

        if type != 'TX' and type != 'RX': # RESET, ATR
            sum_rst.append(time + '  ' + type)
            sum_log_ch.append(['',''])
            sum_log_ch_id.append('')
            sum_abnormal.append('')
        else: # sum_type == 'TX'
            if len(prot_data[m][-1]) >= 4:
                sw = prot_data[m][-1][-4:]
            else:  # Incomplete APDU
                sw = ''

            # sum_log_ch_id
            if prot_data[m][0][0] == '4':  # ETSI ts102.221 Table 10.4a extended logical channels
                log_ch_id = 4 + int(prot_data[m][0][1])  # logical channel number from 4 to 19
            else:
                log_ch_id = int(prot_data[m][0][1]) # logical channel number from 0 to 3
            sum_log_ch_id.append(log_ch_id)
            if log_ch_id > len(log_ch) - 1:
                for n in range(log_ch_id - len(log_ch) + 1):
                    log_ch.append(['',''])

            ins = prot_data[m][0][2:4]
            if ins in command.cmd_name:
                cmd = command.cmd_name[ins]
                if cmd == 'SELECT':
                    if sw != '':
                        log_ch, file_name, abnormal_msg = SELECT.process(prot_data[m], log_ch, log_ch_id)
                    else:
                        file_name = ' [N/A]'
                        abnormal_msg = '(3) Incomplete APDU'
            else:
                cmd = 'Unknown INS [%s]' % ins

            if debug_mode == 1:
                print('time   :', time)
                print('type   :', type)
                print('ins    :', ins)
                print('cmd    :', cmd)
                print('sw     :', sw)
                print('')

            # sum_rst
            sum_rst.append(time + '  ' + cmd)
            if cmd == 'SELECT': sum_rst[-1] += ' ' + file_name

            # sum_log_ch
            sum_log_ch.append(log_ch[log_ch_id][0:2])

            # sum_abnormal
            sum_abnormal.append(abnormal_msg)

        if debug_mode == 2:
            print('sum_rst     :', sum_rst[-1])
            print('prot_data   :', prot_data[m])
            print('log_ch      :', log_ch)
            print('sum_log_ch  :', sum_log_ch[-1])
            print()

    return sum_rst, sum_log_ch, sum_log_ch_id, sum_abnormal

