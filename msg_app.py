import file_system
debug_mode = 0

def rst(input1, input2, read, error, item_num, load_type):
    msg_all, prot_start, prot_end = input1
    prot_type, log_ch, log_ch_id = input2

    start = prot_start[item_num]
    end = prot_end[item_num]
    if debug_mode: print(log_ch)

    app_rst = []
    if prot_type[item_num][0] == 'TX':
        app_rst = ['=' * 150]
        app_rst.append(' Logical Channel : %s' % str(log_ch_id[item_num]))
        if log_ch_id[item_num] >= 4: app_rst[-1] += ' [Extended]'
        if debug_mode: print(app_rst[-1])

        app_rst.append(' Current DF File : %s' % log_ch[item_num][0])
        if log_ch[item_num][0]:
            if log_ch[item_num][0] in file_system.DF_name:
                app_rst[-1] += ' [' + file_system.DF_name[log_ch[item_num][0]] + ']'
        if debug_mode: print(app_rst[-1])

        app_rst.append(' Current EF File : %s' % log_ch[item_num][1])
        if log_ch[item_num][0] and log_ch[item_num][1]:
            if log_ch[item_num][0] in file_system.DF_name:
                if log_ch[item_num][1] in file_system.EF_name[log_ch[item_num][0]]:
                    app_rst[-1] += ' [' + file_system.EF_name[log_ch[item_num][0]][log_ch[item_num][1]] + ']'
        if debug_mode: print(app_rst[-1])
        app_rst.append('=' * 150)

        if read[item_num][0]:
            if len(read[item_num]) == 3:
                app_rst.append(' Record Number   : 0x%s'%read[item_num][1])
                app_rst.append(' Record Length   : 0x%s'%read[item_num][2]+' (%d Bytes)'%int(read[item_num][2],16))
                app_rst.append(' Record Contents : %s'%read[item_num][0][0])
                if len(read[item_num][0])>1: app_rst.append(' Record Parsing  : %s'%read[item_num][0][1])
            elif len(read[item_num]) == 2:
                app_rst.append(' Read Offset     : 0x%s'%read[item_num][1][0])
                app_rst.append(' Read Length     : 0x%s'%read[item_num][1][1]+' (%d Bytes)'%int(read[item_num][1][1],16))
                app_rst.append(' Read Contents   : %s'%read[item_num][0][0])
                if len(read[item_num][0])>1: app_rst.append(' Read Parsing    : %s'%read[item_num][0][1])
            app_rst.append('=' * 150)
        if debug_mode: print(app_rst[-1])

        if error[item_num]:
            app_rst.append(' ERROR Contents  : %s'%error[item_num])
            app_rst.append('=' * 150)

        app_rst.append('')

    if load_type == 'File':
        for m in range(len(start)):
            for n in range(start[m], end[m] + 1):
                if 'APDU Parsing' in msg_all[n] or 'RESET' in msg_all[n] or 'DATA' in msg_all[n]:
                    app_rst.append('-' * 150)
                    app_rst += msg_all[start[m]:end[m]]
                    if app_rst[-1] == '' or app_rst[-1] == '  ':
                        del app_rst[-1]
                    app_rst.append('-' * 150)

    return app_rst

