MAX_LEN = 20

def data_to_lines(data):
    split_data = data.split()
    lines = []
    temp_line = ""
    temp_temp_line = ""
    if len(data) < MAX_LEN:
        return [data]

    for i in range(len(split_data)):
        temp_temp_line += split_data[i] + " "
        if len(temp_line) > MAX_LEN:
            lines.append(temp_line)
            temp_line = ""
            temp_temp_line = "" 

        else:
            temp_line = temp_temp_line
    lines.append(temp_line)
    return lines
        


data = "This is a test of the emergency broadcast system. This is only a test."

print(data_to_lines(data))  # ['This is a test of th', 'e emergency broadcas', 't system. This is on', 'ly a test.']