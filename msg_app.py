import file_system
debug_mode = 0

def rst(input, read, error, item_num):
    prot_type, sum_cmd, sum_log_ch, sum_log_ch_id = input

    log_ch = sum_log_ch[item_num]
    log_ch_id = sum_log_ch_id[item_num]
    cmd = sum_cmd[item_num]

    if debug_mode: print(log_ch_id, log_ch)

    app_rst = []
    if prot_type[item_num][0] == 'TX':
        rst_ind = '[%s]'%str(item_num+1)
        app_rst.append(rst_ind + ' Logical Channel : %s' % str(log_ch_id))
        if log_ch_id >= 4: app_rst[-1] += ' [Extended]'
        if debug_mode: print(app_rst[-1])

        app_rst.append(' '*len(rst_ind)+' Current DF File : %s' % log_ch[0])
        if log_ch[0]:
            if log_ch[0] in file_system.DF_name:
                app_rst[-1] += ' [' + file_system.DF_name[log_ch[0]] + ']'
        if debug_mode: print(app_rst[-1])

        app_rst.append(' '*len(rst_ind)+' Current EF File : %s' % log_ch[1])
        if log_ch[0] and log_ch[1]:
            if log_ch[0] in file_system.DF_name:
                if log_ch[0] in file_system.EF_name:
                    if log_ch[1] in file_system.EF_name[log_ch[0]]:
                        app_rst[-1] += ' [' + file_system.EF_name[log_ch[0]][log_ch[1]] + ']'
        if debug_mode: print(app_rst[-1])

        app_rst.append(' '*len(rst_ind)+' Current Command : %s' % cmd.replace('(X)',''))
        if debug_mode: print(app_rst[-1])

        if read[item_num][0]:
            app_rst.append(' '*(len(rst_ind)+1) + '-' *(80-len(rst_ind)-1))
            if len(read[item_num]) == 3: # READ RECORD
                app_rst.append(' '*len(rst_ind)+' Record Number   : 0x%s'%read[item_num][1])
                app_rst.append(' '*len(rst_ind)+' Record Length   : 0x%s'%read[item_num][2])
                app_rst[-1] +=' (%d Bytes)'%int(read[item_num][2],16)
                split_rst = split_func(read[item_num][0][0], len(rst_ind))
                app_rst.append(' '*len(rst_ind)+' Record Contents : %s'%split_rst)
                if len(read[item_num][0])>1:
                    if '\n' in read[item_num][0][1]:
                        app_rst.append(' ' * len(rst_ind)+' Read Parsing    : '+read[item_num][0][1].split('\n')[0])
                        for n in read[item_num][0][1].split('\n')[1:]:
                            app_rst.append(' ' * len(rst_ind) + ' '*len(' Read Parsing    : ')+n)
                    else: app_rst.append(' '*len(rst_ind)+' Record Parsing  : %s'%read[item_num][0][1])
            elif len(read[item_num]) == 2: # READ BINARY
                app_rst.append(' '*len(rst_ind)+' Read Offset     : 0x%s'%read[item_num][1][0])
                app_rst.append(' '*len(rst_ind)+' Read Length     : 0x%s'%read[item_num][1][1])
                app_rst[-1] += ' (%d Bytes)'%int(read[item_num][1][1],16)
                split_rst = split_func(read[item_num][0][0], len(rst_ind))
                app_rst.append(' '*len(rst_ind)+' Read Contents   : %s'%split_rst)
                if len(read[item_num][0])>1:
                    if '\n' in read[item_num][0][1]:
                        app_rst.append(' ' * len(rst_ind)+' Read Parsing    : '+read[item_num][0][1].split('\n')[0])
                        for n in read[item_num][0][1].split('\n')[1:]:
                            app_rst.append(' ' * len(rst_ind) + ' '*len(' Read Parsing    : ')+n)
                    else: app_rst.append(' '*len(rst_ind)+' Read Parsing    : %s'%read[item_num][0][1])
            elif len(read[item_num]) == 1: # ETC (AUTHENTICATE, ...)
                for n in read[item_num][0]:
                    app_rst.append(' '*len(rst_ind)+n)
        if debug_mode: print()

        if error[item_num]:
            app_rst.append(' '*(len(rst_ind)+1) + '-' *(80-len(rst_ind)-1))
            app_rst.append(' '*len(rst_ind)+' Error Message   : %s'%error[item_num])


    # QXDM/QCAT Parsing
    # if load_type == 'File':
    #     for m in range(len(start)):
    #         for n in range(start[m], end[m] + 1):
    #             if 'APDU Parsing' in msg_all[n] or 'RESET' in msg_all[n] or 'DATA' in msg_all[n]:
    #                 app_rst.append('-' * 80)
    #                 app_rst += msg_all[start[m]:end[m]]
    #                 if app_rst[-1] == '' or app_rst[-1] == '  ':
    #                     del app_rst[-1]
    #                 app_rst.append('-' * 80)

    return app_rst

def split_func(input, weight):
    split_rst = ''
    cnt = 0
    for m in range(len(list(input))):
        if m//32 > 0 and m % 32 == 0:
            split_rst += '\n' + ' ' * (len(' Read Contents   : ')+weight)
        if m % 2 == 0:
            split_rst += list(input)[m]
            cnt += 1
        else:
            split_rst += list(input)[m] + ' '
            cnt += 2
    return split_rst
