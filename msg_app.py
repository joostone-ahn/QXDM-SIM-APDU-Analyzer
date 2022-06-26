import file_system

def rst(input, item_num):
    msg_all, prot_start, prot_end, prot_type, log_ch = input
    start = prot_start[item_num]
    end = prot_end[item_num]

    app_rst = []
    for m in range(len(start)):
        for n in range(start[m], end[m]+1):
            if 'APDU Parsing' in msg_all[n] or 'RESET' in msg_all[n] or 'DATA' in msg_all[n] :
                app_rst.append('-' * 150)
                app_rst += msg_all[start[m]:end[m]]
                if app_rst[-1] == '' or app_rst[-1] == '  ' : del app_rst[-1]
    if app_rst: app_rst.append('-' * 150)

    if prot_type[item_num][0] == 'TX':
        current_dir = []
        current_dir.append('=' * 150)
        current_dir.append('Current DF : %s'%log_ch[item_num][0])
        if log_ch[item_num][0]:
            if log_ch[item_num][0] in file_system.DF_name:
                current_dir[-1] += ' (' + file_system.DF_name[log_ch[item_num][0]] + ')'
        current_dir.append('Current EF : %s'%log_ch[item_num][1])
        if log_ch[item_num][0] and log_ch[item_num][1]:
            if log_ch[item_num][0] in file_system.DF_name:
                if log_ch[item_num][1] in file_system.EF_name[log_ch[item_num][0]]:
                    current_dir[-1] += ' (' + file_system.EF_name[log_ch[item_num][0]][log_ch[item_num][1]] + ')'
        current_dir.append('=' * 150)
        app_rst = current_dir + app_rst

    return app_rst

