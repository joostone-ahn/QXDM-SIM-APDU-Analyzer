import file_system
debug_mode = 1

def rst(input, read, error, item_num):
    prot_type, sum_cmd, sum_log_ch, sum_log_ch_id = input

    log_ch = sum_log_ch[item_num]
    log_ch_id = sum_log_ch_id[item_num]
    cmd = sum_cmd[item_num]

    if debug_mode: print(log_ch_id, log_ch)
    current_DF = log_ch[0]
    current_EF = log_ch[1]
    if current_DF[:16] in file_system.DF_name: current_DF = current_DF[:16]

    app_rst = []
    if prot_type[item_num][0] == 'TX':
        rst_ind = '[%s]'%str(item_num+1)
        void = ' '*len(rst_ind)
        app_rst.append(rst_ind + ' Logical Channel : %s' % str(log_ch_id))
        if log_ch_id >= 4: app_rst[-1] += ' [Extended]'
        if debug_mode: print(app_rst[-1])

        app_rst.append(void+' Current DF File : %s'%log_ch[0])
        if current_DF:
            if current_DF in file_system.DF_name:
                app_rst[-1] += ' [%s]'%file_system.DF_name[current_DF]
        if debug_mode: print(app_rst[-1])

        app_rst.append(void+' Current EF File : %s'%log_ch[1])
        if current_DF and current_EF:
            if current_DF in file_system.DF_name:
                if current_DF in file_system.EF_name:
                    if current_EF in file_system.EF_name[current_DF]:
                        app_rst[-1] += ' [%s]'%file_system.EF_name[current_DF][current_EF]
        if debug_mode: print(app_rst[-1])

        app_rst.append(void+' Current Command : %s' % cmd.replace('(X)',''))
        if debug_mode: print(app_rst[-1])

        if read[item_num][0]:
            app_rst.append(void + ' ' + '-' *(80-len(void)-1))
            if len(read[item_num]) == 3: # READ RECORD
                app_rst.append(void+' Record Number   : 0x%s'%read[item_num][1])
                app_rst.append(void+' Record Length   : 0x%s'%read[item_num][2])
                app_rst[-1] +=' (%d Bytes)'%int(read[item_num][2],16)
                app_rst.append(void+' Record Contents : ')
                app_rst = split_contents(read[item_num][0][0], app_rst)
                if len(read[item_num][0])>1:
                    app_rst.append(void + ' Record Parsing  : ')
                    app_rst = split_parsing(read[item_num][0][1], app_rst)
            elif len(read[item_num]) == 2: # READ BINARY
                app_rst.append(void+' Read Offset     : 0x%s'%read[item_num][1][0])
                app_rst.append(void+' Read Length     : 0x%s'%read[item_num][1][1])
                app_rst[-1] += ' (%d Bytes)'%int(read[item_num][1][1],16)
                app_rst.append(void+' Read Contents   : ')
                app_rst = split_contents(read[item_num][0][0], app_rst)
                if len(read[item_num][0])>1:
                    app_rst.append(void + ' Read Parsing    : ')
                    app_rst = split_parsing(read[item_num][0][1], app_rst)
            elif len(read[item_num]) == 1: # ETC (AUTHENTICATE, ...)
                for n in read[item_num][0]: app_rst.append(void+n)
        if debug_mode: print()

        if error[item_num]:
            app_rst.append(void + ' ' + '-' *(80-len(void)-1))
            app_rst.append(void+' Error Message   : %s'%error[item_num])


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

def split_contents(input, app_rst):
    void = ' '*len(app_rst[-1])
    cnt = 0
    for m in range(len(list(input))):
        if m//32 > 0 and m % 32 == 0:
            app_rst.append(void)
        if m % 2 == 0:
            app_rst[-1] += list(input)[m]
            cnt += 1
        else:
            app_rst[-1] += list(input)[m] + ' '
            cnt += 2
    return app_rst

def split_parsing(input, app_rst):
    void = ' '*len(app_rst[-1])
    if '\n' in input:
        input_list = input.split('\n')
        for n in range(len(input_list)):
            if n>0: app_rst.append(void)
            app_rst[-1] += input_list[n]
    else:
        app_rst[-1] += input
    return app_rst
