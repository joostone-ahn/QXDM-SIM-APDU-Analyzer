import command
import SELECT
import file_system
import short_file_id
debug_mode = 0

def rst(input):
    msg_all, prot_start, prot_type, prot_data = input
    sum_rst, sum_log_ch, sum_log_ch_id, sum_error = [], [], [], []
    log_ch = [['','']] # log_ch[n] = [current DF, current EF]

    last_file_id = ''
    for m in range(len(prot_start)):
        if debug_mode: print('prot_data      :', prot_data[m])

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
            if sw != '9000' and sw[:2] != '91':
                log_ch_prev_0 = log_ch[log_ch_id][0]
                log_ch_prev_1 = log_ch[log_ch_id][1]
            if debug_mode: print('status word    :', sw)

            # sum_log_ch_id
            cla = prot_data[m][0][:2]
            cla_bin = format(int(cla,16),'b').zfill(8)
            if cla_bin[0:2] == '01' or cla_bin[0:2] == '11': # '0100' ETSI ts102.221 Table 10.4a extended logical channels
                log_ch_id = 4 + int(cla_bin[4:],2)  # logical channel number from 4 to 19
            else:
                log_ch_id = int(cla_bin[6:],2) # logical channel number from 0 to 3
            if log_ch_id > len(log_ch) - 1:
                for n in range(log_ch_id - len(log_ch) + 1):
                    log_ch.append(['',''])
            sum_log_ch_id.append(log_ch_id)
            if debug_mode: print('class          :', cla)
            if debug_mode: print('log_ch_id      :', sum_log_ch_id[-1])

            # log_ch
            file_name, error = '',''
            ins = prot_data[m][0][2:4]
            if ins in command.cmd_name:
                cmd = command.cmd_name[ins]
                if sw == '6A82': cmd += '(X)'
                if ins == 'A4': # SELECT
                    if sw != '':
                        log_ch, file_name, error = SELECT.process(prot_data[m], log_ch, log_ch_id)
                        last_file_id = prot_data[m][2]
                    else:
                        file_name = '[N/A]'
                        error = '*Incomplete APDU'
                elif ins in short_file_id.cmd_SFI_list:
                    SFI_used, SFI = short_file_id.category(prot_data[m][0])
                    if SFI_used:
                        cmd += ' (SFI:0x%s)' % SFI
                        log_ch, file_name, error = short_file_id.process(log_ch, log_ch_id, SFI)
                    else:
                        file_name, error = file_system.process(log_ch[log_ch_id][0], log_ch[log_ch_id][1], last_file_id)
                elif ins == '88' or ins == '89': # AUTHENTICATE
                    file_name, error = file_system.process(log_ch[log_ch_id][0], '', last_file_id)
            else:
                cmd = 'Unknown INS(%s)'%ins
            if debug_mode: print('instruction    :', ins)
            if debug_mode: print('command name   :', cmd)
            if debug_mode: print('file name      :', file_name)
            if debug_mode: print('log_ch         :', log_ch)

            # sum_log_ch
            if sw != '9000' and sw[:2] != '91':
                log_ch[log_ch_id][0] = log_ch_prev_0
                log_ch[log_ch_id][1] = log_ch_prev_1
            sum_log_ch.append(log_ch[log_ch_id][0:2])

            # sum_rst
            cmd_len_max = len(command.cmd_name['AA'])+8  # TERMINAL CAPABILITY
            sum_rst.append(num + '  ' + time + '  ' + cmd + ' ' * (cmd_len_max - len(cmd)))
            if file_name: sum_rst[-1] += '  ' + file_name

            # sum_error
            sum_error.append(error)

        if debug_mode: print('sum_log_ch     :', sum_log_ch[-1])
        if debug_mode: print('sum_rst        :', '['+sum_rst[-1].split('[')[1])
        if debug_mode: print('error          :', sum_error[-1])
        if debug_mode: print()

    return sum_rst, sum_log_ch, sum_log_ch_id, sum_error

