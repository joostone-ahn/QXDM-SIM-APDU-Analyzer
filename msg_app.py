def rst(input):
    msg_all, prot_start, prot_end, item_num = input
    start = prot_start[item_num]
    end = prot_end[item_num]

    app_rst = []
    for m in range(len(start)):
        for n in range(start[m], end[m]+1):
            if 'APDU Parsing' in msg_all[n] or 'RESET' in msg_all[n] or 'DATA' in msg_all[n] :
                app_rst.append('-' * 150)
                app_rst += msg_all[start[m]:end[m]]
                if app_rst[-1] == '' or app_rst[-1] == '  ' : del app_rst[-1]
    if app_rst : app_rst.append('-' * 150)

    return app_rst

