import command
import SELECT
import file_system
import short_file_id
debug_mode = 0
def rst(input):
    msg_all, prot_start, prot_type, prot_data = input

    sum_rst, sum_log_ch, sum_log_ch_id, sum_error = [], [], [], []
    log_ch = [['','']] # log_ch[n] = [current DF, current EF]

    for m in range(len(prot_start)):
        file_name, error = '', ''
        num_max = len(str(len(prot_start)))+1 # including '['
        num = ' '*(num_max-len(str(m+1))) + '[' + str(m+1) + ']'
        time = msg_all[prot_start[m][0]].split('  ')[1].split('  [')[0]
        type = prot_type[m][0]

        if type != 'TX' and type != 'RX': # RESET, ATR
            sum_rst.append(num + '  ' + time + '  ' + type)
            sum_log_ch.append(['',''])
            sum_log_ch_id.append('')
            sum_error.append('')
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
            if log_ch_id > len(log_ch) - 1:
                for n in range(log_ch_id - len(log_ch) + 1):
                    log_ch.append(['',''])
            sum_log_ch_id.append(log_ch_id)

            ins = prot_data[m][0][2:4]
            if ins in command.cmd_name:
                cmd = command.cmd_name[ins]
                if cmd == 'SELECT':
                    if sw != '':
                        log_ch, file_name, error = SELECT.process(prot_data[m], log_ch, log_ch_id)
                        last_file_id = prot_data[m][2]
                    else:
                        file_name = ' [N/A]'
                        error = '(3) Incomplete APDU'
                elif ins in short_file_id.cmd_SFI_list :
                    file_name, error = file_system.process(log_ch[log_ch_id][0], log_ch[log_ch_id][1], last_file_id)
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
            cmd_len_max = len(command.cmd_name['AA'])  # TERMINAL CAPABILITY
            cmd_len = len(cmd)
            sum_rst.append(num + '  ' + time + '  ' + cmd + ' '*(cmd_len_max-cmd_len))
            if file_name: sum_rst[-1] += '  ' + file_name

            # sum_log_ch
            sum_log_ch.append(log_ch[log_ch_id][0:2])

            # sum_abnormal
            sum_error.append(error)

        if debug_mode == 2:
            print('sum_rst       :', sum_rst[-1])
            print('prot_data     :', prot_data[m])
            print('log_ch        :', log_ch)
            print('sum_log_ch_id :', sum_log_ch_id[-1])
            print('sum_log_ch    :', sum_log_ch[-1])
            print()

    return sum_rst, sum_log_ch, sum_log_ch_id, sum_error

