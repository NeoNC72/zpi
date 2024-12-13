MAX_LEN = 20

def data_to_lines(data):
    split_data = data.split()
    lines = []
    temp_line = ""
    temp_temp_line = ""
    if len(data) < MAX_LEN:
        return [data]
    i = 0
    while True:
        if i == len(split_data):
            break
        
        temp_temp_line += split_data[i] + " "
        if len(temp_line) > MAX_LEN:
            lines.append(temp_line)
            temp_line = ""
            temp_temp_line = "" 
            i -= 1
        else:
            temp_line = temp_temp_line
        i += 1
    lines.append(temp_line)
    return lines
        


data = "is this q so long that it wraps or ses some other funky stuff lol"

print(data_to_lines(data))  # ['This is a test of th', 'e emergency broadcas', 't system. This is on', 'ly a test.']