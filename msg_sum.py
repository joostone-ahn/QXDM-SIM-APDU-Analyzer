import command
import SELECT
import READ
import Proactive
import file_system
import short_file_id
debug_mode = 0

def rst(input, load_type):
    msg_all, prot_start, prot_type, prot_data = input
    sum_rst, sum_log_ch, sum_log_ch_id, sum_read, sum_error = [], [], [], [], []
    sum_remote, sum_remote_list = READ.init()
    log_ch = [['','']] # log_ch[n] = [current DF, current EF]

    last_file_id = ''
    for m in range(len(prot_start)):
        if debug_mode: print('prot_data      :', prot_data[m])

        num_max = len(str(len(prot_start)))+1 # including '['
        num = ' '*(num_max-len(str(m+1))) + '[' + str(m+1) + ']'
        type = prot_type[m][0]
        if load_type == 'File':
            time = msg_all[prot_start[m][0]].split('  ')[1].split('  [')[0]
            if ':' not in time: time = 'TIME ERROR'
            time = '%-12s'%time
        elif load_type == 'Paste':
            time = msg_all[prot_start[m][0]].split('                 ')[1].split(' ')[0]
            time = '%-12s'%time

        if type != 'TX' and type != 'RX': # RESET, ATR
            sum_rst.append(num + '  ' + time + '  ' + type)
            sum_log_ch.append(['','']) # sum_log_ch[n] = [current DF, current EF]
            sum_log_ch_id.append('')
            sum_read.append(['','']) # sum_read[n] = [file_name, file_data]
            sum_error.append('')
        else: # sum_type == 'TX'
            if len(prot_data[m][-1]) >= 4:
                sw = prot_data[m][-1][-4:]
            else:  # Incomplete APDU
                sw = ''
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
            if debug_mode: print('CLA byte       :', cla)
            if debug_mode: print('log_ch_id      :', sum_log_ch_id[-1])

            if sum_rst:
                if 'SELECT (X)' in sum_rst[-1]:
                    log_ch[log_ch_id][1] = ''

            # log_ch
            file_name, error = '',''
            ins = prot_data[m][0][2:4]
            if debug_mode: print('INS byte       :', ins)
            if ins in command.cmd_name:
                cmd = command.cmd_name[ins]
                if ins == 'A4': # SELECT
                    if sw != '':
                        log_ch, file_name, error = SELECT.process(prot_data[m], log_ch, log_ch_id)
                        last_file_id = prot_data[m][2]
                    else:
                        file_name = '[N/A]'
                        error = 'Incomplete APDU'
                elif ins in short_file_id.cmd_SFI_list:
                    SFI_used, SFI = short_file_id.category(prot_data[m][0])
                    if SFI_used:
                        cmd += ' (SFI: 0x%s)'%SFI
                        log_ch, file_name, error = short_file_id.process(log_ch, log_ch_id, SFI)
                    # else:
                    #     file_name, error = file_system.process(log_ch[log_ch_id][0], log_ch[log_ch_id][1], last_file_id)
                elif ins == '88' or ins == '89': # AUTHENTICATE
                    file_name, error = file_system.process(log_ch[log_ch_id][0], '', last_file_id)
                    cmd += ' (%s)'%file_name.split(' ')[1].replace(']','')
                    file_name = ''
                elif ins == '70': # MANAGE CHANNEL
                    if prot_data[m][0][4:6] == '80': cmd += ' (CLOSE: %d)'%int(prot_data[m][0][6:8],16)
                    elif prot_data[m][0][4:6] == '00':
                        if len(prot_data[m][1]) == 8 and prot_data[m][1][-4:] == '9000':
                            if prot_data[m][0][6:8] == '00': cmd += ' (OPEN: %d)'%int(prot_data[m][1][2:4],16)
                            else: cmd += ' (OPEN: %d)'%int(prot_data[m][0][6:8],16)
                elif ins == '12': # FETCH
                    if debug_mode: print('FETCH check    :',prot_data[m])
                    FETCH_data = prot_data[m][1].split('810301')[1][:4]
                    if FETCH_data[:2] in Proactive.Proactive_type:
                        FETCH_type = Proactive.Proactive_type[FETCH_data[:2]]
                        cmd += ' (%s)' % FETCH_type
                        if FETCH_type == 'REFRESH':
                            if FETCH_data[2:] in Proactive.REFRESH_type:
                                cmd = cmd[:-1] + ': %s)'% Proactive.REFRESH_type[FETCH_data[2:]]
                elif ins == '14': # TERMINAL RESPONSE
                    if debug_mode: print('T/R check      :', prot_data[m])
                    TR_data = prot_data[m][2].split('810301')[1][:4]
                    if TR_data[:2] in Proactive.Proactive_type:
                        TR_type = Proactive.Proactive_type[TR_data[:2]]
                        TR_rst = prot_data[m][2].split('8281')[1][4]
                        cmd += ' (%s: '%TR_type
                        cmd += '%sX)'%TR_rst
                elif ins == 'C2': # ENVELOPE
                    if debug_mode: print('ENVELOPE check :', prot_data[m])
                    ENV_type = prot_data[m][2][:2]
                    if ENV_type == 'D1': cmd += ' (SMS-PP DOWNLOAD)'
                    elif ENV_type == 'D6': cmd += ' (EVENT DOWNLOAD)'

            else:
                cmd = "Unknown (INS:%s)"%ins
            if debug_mode: print('command name   :', cmd)
            if debug_mode: print('file name      :', file_name)
            if debug_mode: print('log_ch         :', log_ch)

            # sum_log_ch
            sum_log_ch.append(log_ch[log_ch_id][0:2])
            if debug_mode: print('sum_log_ch     :', sum_log_ch[-1])

            # sum_rst
            if sw != '9000' and sw[:2] != '91' and ins[0] != '2': cmd += ' (X)'
            sum_rst.append(num + '  ' + time + '  ' +'%-42s'%cmd)
            if file_name: sum_rst[-1] += file_name
            if debug_mode: print('sum_rst        :', sum_rst[-1])

            # sum_read, sum_remote
            if ins == 'B0' or ins == 'B2':
                if sw == '9000' or sw[:2] == '91':
                    if SFI_used == False : file_name, error \
                        = file_system.process(log_ch[log_ch_id][0], log_ch[log_ch_id][1], last_file_id)
                    sum_read, sum_remote \
                        = READ.process(ins, file_name, prot_data[m], sum_read, sum_remote, sum_remote_list)
                else:
                    sum_read.append(['', ''])
            else:
                sum_read.append(['', ''])
            if debug_mode: print('sum_remote     :', sum_remote)
            if debug_mode: print('sum_read       :', sum_read[-1])

            # sum_error (R-APDU TBD)
            if sw == '6A82': # ETSI ts102.221 Table 10.14
                if error: error = 'File not found (SW:6A82) ' + error
                else: error = 'File not found (SW:6A82)'
            elif sw == '6282': # ETSI ts102.221 Table 10.9
                if error: error = 'unsuccessful search (SW:6282)' + error
                else: error = 'unsuccessful search (SW:6282)'
            sum_error.append(error)
            if debug_mode: print('error          :', sum_error[-1])

        if debug_mode: print()

    return sum_rst, sum_log_ch, sum_log_ch_id, sum_read, sum_error, sum_remote

