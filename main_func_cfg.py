def out_fuse(dicts, spice=True):
    threshold = 0.7
    output = {}
    classes = {}
    for dict in dicts:
        for object in dict:
            try:
                classes[object] += dict[object]
            except KeyError:
                classes[object] = dict[object]
    dicts_len = len(dicts)
    if not spice:
        dicts_len = 1
    for object in classes:
        classes[object] = classes[object]/dicts_len
        if classes[object]-int(classes[object]) >= threshold:
            output[object] = int(classes[object])+1
        elif int(classes[object]) != 0:
            output[object] = int(classes[object])
    return output


def write_output(dict, f):
    text = open(f, 'w')
    i=0
    for object in dict:
        if i == 0:
            i=1
        else:
            text.write('\n')
        text.write(object)
        text.write(' ')
        text.write(str(dict[object]))
    text.close()


def record_fuse(dicts, record, start_time, time, total):
    if time-start_time > 50 and record == 0:
        output = out_fuse(dicts)
        record += 1
        print("XXXXXXXXXXXXX=1\n")
        print(output)
        total.append(output)
        dicts = []
        return record, total, dicts
    elif time-start_time > 120 and record == 1:
        output = out_fuse(dicts)
        record += 1
        print("XXXXXXXXXXXXX=2\n")
        print(output)
        dicts = []
        total.append(output)
        return record, total, dicts
    # elif time - start_time > 230 and record == 2:
    #     output = out_fuse(dicts)
    #     total.append(output)
    #     end = out_fuse(total, spice=False)
    #     record += 1
    #     print("XXXXXXXXXXXXX=3\n")
    #     print(output)
    #     dicts = []
    #     return record, end, dicts
    return record, total, dicts


def record_fuse2(total, dict):
    scene3={}
    for object in dict:
        if dict[object]!=0:
            scene3[object] = dict[object]
    total.append(scene3)
    end = out_fuse(total, spice=False)
    return end


def record_if(start_time, time):
    t = time-start_time
    if (t>5 and t<50)or(t>75 and t<120)or(t>145 and t<230):
        return True
    return False


def alarmer(start_time, time):
    t = time - start_time
    if t<60:
        print("Scene:First    Time left:", 60-t)
    elif t>70 and t<130:
        print("Scene:Second    Time left:", 130-t)
    elif t>140 and t<240:
        print("Scene:Third    Time left:", 240-t)
    elif t>240 :
        print("end")

# a = {"CA001":1, "CA002":1}
# b = {"CA001":1, "CA002":1}
# c = {"CA001":0, "CA002":1}
# d = {"CA001":0, "CA002":0}
# list = [a, b, c, d]
# write_output(out_fuse(list))
