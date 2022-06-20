def rst(input):
    msg_all, prot_start, prot_end, item_num = input
    start = prot_start[item_num]
    end = prot_end[item_num]

    app_rst = []
    app_rst.append('='*100)
    for m in range(len(start)):
        for n in range(start[m], end[m]+1):
            if msg_all[n].replace(' ','') != '':
                app_rst.append(msg_all[n])
        app_rst.append('='*100)

    return app_rst

