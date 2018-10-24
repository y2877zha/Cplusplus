# -*- coding: utf-8 -*-# __author__ = 'yuzhe zhang'
import sys
import re

def intersect(p1, p2, p3, p4):
    temp_list = [p1, p2, p3, p4]
    temp_set = set(temp_list)
    if (len(temp_set) == 2):
        return "same"
    elif (len(temp_set) == 3):
        temp_crossing = 0
        for elem in temp_list:
            if (temp_list.count(elem) == 2):
                temp_crossing = elem
        temp_set.remove(temp_crossing)
        temp_V_list = list(temp_set)
        if (temp_V_list[0][0] <= temp_crossing[0] <= temp_V_list[1][0]
                or temp_V_list[1][0] <= temp_crossing[0] <= temp_V_list[0][0]
                or temp_V_list[0][1] <= temp_crossing[1] <= temp_V_list[1][1]
                or temp_V_list[1][1] <= temp_crossing[1] <= temp_V_list[0][1]):
            X = temp_crossing[0]
            Y = temp_crossing[1]
            return (X, Y)
        else:
            return "same"
    else:
        if (p1[0] == p2[0] != p3[0] == p4[0]):
            return 0
        elif (p1[0] == p2[0] == p3[0] == p4[0]):
            if (p1[1] < p3[1] < p2[1] or p2[1] < p3[1] < p1[1]
                    or p1[1] < p4[1] < p2[1] or p2[1] < p4[1] < p1[1]):
                return "same"
            else:
                return 0
        elif (p1[0] == p2[0]):
            X = p1[0]
            c = (p3[1] - p4[1]) / (p3[0] - p4[0])
            d = p3[1] - (p3[1] - p4[1]) / (p3[0] - p4[0]) * p3[0]
            Y = c * X + d
        elif (p3[0] == p4[0]):
            X = p3[0]
            a = (p1[1] - p2[1]) / (p1[0] - p2[0])
            b = p1[1] - (p1[1] - p2[1]) / (p1[0] - p2[0]) * p1[0]
            Y = a * X + b
        else:
            a = (p1[1] - p2[1]) / (p1[0] - p2[0])
            b = p1[1] - (p1[1] - p2[1]) / (p1[0] - p2[0]) * p1[0]
            c = (p3[1] - p4[1]) / (p3[0] - p4[0])
            d = p3[1] - (p3[1] - p4[1]) / (p3[0] - p4[0]) * p3[0]
            if (a - c == 0):
                if ((p3[1] == a * p3[0] + b and p1[1] < p3[1] < p2[1])
                        or (p3[1] == a * p3[0] + b and p2[1] < p3[1] < p1[1])
                        or (p3[1] == a * p3[0] + b and p1[1] < p4[1] < p2[1])
                        or (p3[1] == a * p3[0] + b and p2[1] < p4[1] < p1[1])):
                    return "same"
                else:
                    return 0
            else:
                X = (d - b) / (a - c)
                Y = (a * d - c * b) / (a - c)

        if ((X > p1[0] and X > p2[0])
                or (X < p1[0] and X < p2[0])
                or (X > p3[0] and X > p4[0])
                or (X < p3[0] and X < p4[0])
                or (Y > p1[1] and Y > p2[1])
                or (Y < p1[1] and Y < p2[1])
                or (Y > p3[1] and Y > p4[1])
                or (Y < p3[1] and Y < p4[1])):
            return 0
        else:
            return (X, Y)

def parse_street(output, street_name, street_seg):
    S = output['S']
    s_input = []
    for i in range(0, len(street_seg) - 1, 2):
        s_input.append((float(street_seg[i]), float(street_seg[i + 1])))

    for i in range(len(s_input) - 1):
        if (s_input[i] == s_input[i + 1]):
            return "same_next_point"

    for i in range(len(s_input) - 1):
        j = i + 1
        while (j < (len(s_input) - 1)):
            x = intersect(s_input[i], s_input[i + 1], s_input[j], s_input[j + 1])
            if (x == "same"):
                return "cover_itself"
            elif (x != 0 and x not in s_input):
                return "cover_itself"
            j = j + 1

    for i in range(len(s_input) - 1):
        for S_key in S:
            if (S_key != street_name):
                for j in range(len(S[S_key]) - 1):
                    x = intersect(s_input[i], s_input[i + 1], S[S_key][j], S[S_key][j + 1])
                    if (x == "same"):
                        return "cover_other"

def add(output, street_name, street_seg):
    s = output['S']
    V = output['V']
    E = output['E']
    s[street_name] = []
    for i in range(0, len(street_seg) - 1, 2):
        s[street_name].append((float(street_seg[i]), float(street_seg[i + 1])))

    E_crossing_set = set()
    for E_elem in E:
        E_crossing_set.add((V[E_elem[0]], V[E_elem[1]]))

    V_near_crossing_set = set()
    comp = []

    for k1 in s:
        for k2 in s:
            if (k1 != k2 and set([k1, k2]) not in comp):
                comp.append(set([k1, k2]))
                i = 0
                j = 0
                while (i < len(s[k1]) - 1):
                    while (j < len(s[k2]) - 1):
                        V_intersect = intersect(s[k1][i], s[k1][i + 1], s[k2][j], s[k2][j + 1])
                        if (V_intersect != 0 and V_intersect != "same"):
                            V_near_crossing_set.update([s[k1][i], s[k1][i + 1], s[k2][j], s[k2][j + 1], V_intersect])
                            if (V_intersect not in s[k1] and V_intersect not in s[k2]):
                                E_crossing_set.update(
                                    [(s[k1][i], V_intersect), (V_intersect, s[k1][i + 1]), (s[k2][j], V_intersect),
                                     (V_intersect, s[k2][j + 1])])
                                if ((s[k1][i], s[k1][i + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[k1][i], s[k1][i + 1]))
                                if ((s[k2][j], s[k2][j + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[k2][j], s[k2][j + 1]))
                                s[k1].insert(i + 1, V_intersect)
                                s[k2].insert(j + 1, V_intersect)
                                j = j + 1
                            elif (V_intersect in s[k1] and V_intersect not in s[k2]):
                                E_crossing_set.update([(s[k2][j], V_intersect), (V_intersect, s[k2][j + 1])])
                                if ((s[k2][j], s[k2][j + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[k2][j], s[k2][j + 1]))
                                s[k2].insert(j + 1, V_intersect)
                                j = j + 1
                            elif (V_intersect in s[k2] and V_intersect not in s[k1]):
                                E_crossing_set.update([(s[k1][i], V_intersect), (V_intersect, s[k1][i + 1])])
                                if ((s[k1][i], s[k1][i + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[k1][i], s[k1][i + 1]))
                                s[k1].insert(i + 1, V_intersect)
                                j = j + 1
                            elif (V_intersect in s[k1] and V_intersect in s[k2]):
                                E_crossing_set.update([(s[k1][i], s[k1][i + 1]), (s[k2][j], s[k2][j + 1])])
                        j = j + 1
                    j = 0
                    i = i + 1

    if (len(V) == 0):
        V_new_list = list(V_near_crossing_set)
        count = 0
    else:
        V_values_set = set(V.values())
        V_new_set = V_near_crossing_set - V_values_set
        V_new_list = list(V_new_set)
        k_list = V.keys()
        count = k_list[len(k_list) - 1]

    for V_elem in V_new_list:
        count = count + 1
        V[count] = V_elem

    E_list = list(E_crossing_set)
    E = []
    for E_elem in E_list:
        for k in V:
            if (E_elem[0] == V[k]):
                p1 = k
            if (E_elem[1] == V[k]):
                p2 = k
        E.append((p1, p2))

    output['S'] = s
    output['V'] = V
    output['E'] = E

    return output

def delete(output, street_name):
    S = output['S']
    V = output['V']
    E = output['E']
    s = S[street_name]

    V_id_du = {}
    V_id_1 = []
    V_id_3_4 = []
    V_id_2_m4 = []
    s_V_id = []
    V_del_set = set()

    for E_elem in E:
        if (E_elem[0] not in V_id_du.keys()):
            V_id_du[E_elem[0]] = 1
        else:
            V_id_du[E_elem[0]] = V_id_du[E_elem[0]] + 1
        if (E_elem[1] not in V_id_du.keys()):
            V_id_du[E_elem[1]] = 1
        else:
            V_id_du[E_elem[1]] = V_id_du[E_elem[1]] + 1

    for V_id_du_key in V_id_du:
        if (V_id_du[V_id_du_key] == 1):
            V_id_1.append(V_id_du_key)
        elif (3 <= V_id_du[V_id_du_key] <= 4):
            V_id_3_4.append(V_id_du_key)
        else:
            V_id_2_m4.append(V_id_du_key)

    for i in range(len(s)):
        for k in V:
            if (s[i] == V[k]):
                s_V_id.append(k)

    for i in range(len(s_V_id)):
        if (i != len(s_V_id) - 1):
            if ((s_V_id[i], s_V_id[i + 1]) in E):
                E.remove((s_V_id[i], s_V_id[i + 1]))
            elif ((s_V_id[i + 1], s_V_id[i]) in E):
                E.remove((s_V_id[i + 1], s_V_id[i]))
        if (s_V_id[i] in V_id_1):
            del V[s_V_id[i]]
        elif (s_V_id[i] in V_id_3_4):
            merge = {0: 0, 1: 0}
            E_output = E[:]
            for E_elem in E:
                if (s_V_id[i] == E_elem[0]):
                    merge[1] = E_elem[1]
                elif (s_V_id[i] == E_elem[1]):
                    merge[0] = E_elem[0]
                if ((s_V_id[i], merge[1]) in E_output):
                    E_output.remove((s_V_id[i], merge[1]))
                elif ((merge[0], s_V_id[i]) in E_output):
                    E_output.remove((merge[0], s_V_id[i]))
            E = E_output[:]
            E.append((merge[0], merge[1]))
            V_del_set.add(V[s_V_id[i]])
            del V[s_V_id[i]]

    E_output = E[:]
    for elem in E:
        if (elem[0] in V_id_1 and elem[1] in V_id_1):
            E_output.remove(elem);
            del V[elem[0]]
            del V[elem[1]]
    E = E_output[:]

    del S[street_name]

    for S_key in S:
        for elem in S[S_key]:
            if (elem in V_del_set):
                S[S_key].remove(elem)

    output['S'] = S
    output['V'] = V
    output['E'] = E

    return output

def generate_graph(output):
    V = output['V']
    E = output['E']
    print 'V={'
    for k in V:
        print "%s:(%.2f,%.2f)" % (k, V[k][0], V[k][1])
    print '}'
    print ' '
    print 'E={'
    for i in range(len(E)):
        if i < len(E):
            print "<" + str(E[i][0]) + "," + str(E[i][1]) + ">"
    print '}'

def main():
    output = {'V': {}, 'E': [], 'S': {}}
    while True:
        S = output['S']
        input_x = sys.stdin.readline()
        if input_x == '':
            break

        x = re.match(r'^\s*(\w)\s*"(.*)"(.*)$', input_x)
        x_g = re.match(r'^\s*(g)\s*$', input_x)

        if x:
            cmd = x.group(1)
            scmd = re.match(r'^[acrg]$', cmd)
            if not scmd:
                sys.stderr.write("Error: Your input command does not start with 'a','c','r','g' \n")
                continue

            if (cmd == 'a' or cmd == 'c' or cmd == 'r'):
                street_name = re.match(r'^\s*$', x.group(2).lower())
                k_str = str(S.keys())
                if street_name:
                    sys.stderr.write("Error: The street name you input is empty \n")
                    continue
                if (cmd == 'a' and (x.group(2).lower() in k_str.lower())):
                    sys.stderr.write("Error: 'a' specified for a street that already exist \n")
                    continue

                if ((cmd == 'c' or cmd == 'r') and (x.group(2).lower() not in k_str.lower())):
                    sys.stderr.write("Error: 'c' or ''r specified for a street that does not exist \n")
                    continue

            if (cmd == 'a' or cmd == 'c'):
                street_seg = re.match(r'(\s*\(\s*-?\d+\s*,\s*-?\d+\s*\)\s*)*$', x.group(3))
                if street_seg:
                    p = re.compile(r'-?\d+')
                    seg_list = p.findall(x.group(3))
                    if (len(seg_list) == 0 or len(seg_list) == 2):
                        sys.stderr.write("Error: The coordinates of is imcomplete \n")
                        continue

                    result = parse_street(output, x.group(2), seg_list)

                    if (result == "same_next_point"):
                        sys.stderr.write("Error: The two points are same \n")
                        continue
                    if (result == "cover_itself"):
                        sys.stderr.write("Error: The street covers itself \n")
                        continue
                    if (result == "cover_other"):
                        sys.stderr.write(
                            "Error: The street covers other street \n")
                        continue
                else:
                    sys.stderr.write("Error: Coordinates have format error \n")
                    continue

            if (cmd == 'r'):
                street_seg = re.match(r'^\s*$', x.group(3))
                if not street_seg:
                    sys.stderr.write("Error: 'r' specified for a street that does not exist \n")
                    continue

            if (cmd == 'a'):
                output = add(output, x.group(2).lower(), seg_list)
            elif (cmd == 'c'):
                output = delete(output, x.group(2).lower())
                output = add(output, x.group(2).lower(), seg_list)
            elif (cmd == 'r'):
                output = delete(output, x.group(2).lower())
        elif x_g:
            generate_graph(output)

        else:
            sys.stderr.write("Error: Your input command is invalid \n")

    print 'Finished reading input'
    sys.exit(0)

if __name__ == '__main__':
    main()

