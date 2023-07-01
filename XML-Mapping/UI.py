#Libraries - all required except plt (just for checking and visualization) and mp (for viewing final model)
import matplotlib.pyplot as plt
import numpy as np
import triangle as tr

def form_tri_mesh(file_name:str):
    pts0 = [[0, 0], [0, 0], [0, 0], [0, 0]]
    pts = [pts0]
    seg1 = [[0, 1], [1, 2], [2, 3], [3, 0]]
    seg0 = [seg1]
    pts_index = 1
    seg_index = 1
    seg_num = 4
    lCols0 = [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
    lCols = [lCols0]
    lCols_index = 1
    rCols0 = [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
    rCols = [rCols0]
    rCols_index = 1
    xml_image = open(file_name, 'r')
    for line in xml_image:
        line = line.strip()
        if line == '<control_points_set>':
            pts.append([])
            seg0.append([])
            point_line = xml_image.readline().strip()
            while point_line != '</control_points_set>':
                point = []
                num_str = ''
                char = 18
                while char < len(point_line):
                    while point_line[char].isdigit() or point_line[char] == '.':
                        num_str += point_line[char]
                        char += 1
                    if len(num_str) > 0:
                        num = float(num_str)
                        point.insert(0, num)
                        num_str = ''
                    char += 1
                pts[pts_index].append(point)
                seg0[seg_index].append((seg_num, seg_num + 1))
                seg_num += 1
                point_line = xml_image.readline().strip()
            seg0[seg_index] = seg0[seg_index][:len(seg0[seg_index]) - 1]
            pts_index += 1
            seg_index += 1
        elif line == '<left_colors_set>':
            lCols.append([])
            col_line = xml_image.readline().strip()
            while col_line != '</left_colors_set>':
                col = []
                num_str = ''
                char = 0
                while char < len(col_line):
                    while col_line[char].isdigit() or col_line[char] == '.':
                        num_str += col_line[char]
                        char += 1
                    if len(num_str) > 0:
                        num = float(num_str)
                        col.insert(0, num/255)
                        num_str = ''
                    char += 1
                lCols[lCols_index].append(col)
                col_line = xml_image.readline().strip()
            lCols_index += 1
        elif line == '<right_colors_set>':
            rCols.append([])
            col_line = xml_image.readline().strip()
            while col_line != '</right_colors_set>':
                col = []
                num_str = ''
                char = 0
                while char < len(col_line):
                    while col_line[char].isdigit() or col_line[char] == '.':
                        num_str += col_line[char]
                        char += 1
                    if len(num_str) > 0:
                        num = float(num_str)
                        col.insert(0, num/255)
                        num_str = ''
                    char += 1
                rCols[rCols_index].append(col)
                col_line = xml_image.readline().strip()
            rCols_index += 1

    xml_image.close()
    
    for c_s in range(len(lCols)):
        for c in range(len(lCols[c_s])):
            lCols[c_s][c] = [lCols[c_s][c][0], lCols[c_s][c][1], lCols[c_s][c][3]]
    
    for c_s in range(len(rCols)):
        for c in range(len(rCols[c_s])):
            rCols[c_s][c] = [rCols[c_s][c][0], rCols[c_s][c][1], rCols[c_s][c][3]]
    
    for seg in pts:
        for point in seg:
            point[1] *= -1
    seg0T = np.vstack(seg0).tolist()
    ptsT = np.vstack(pts).tolist()
    
    x = []
    y = []
    for dot in ptsT:
        x.append(dot[0])
        y.append(dot[1])

    fig = plt.figure()
    plt.plot(x, y, '.', c=(0,0,0))
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    pts[0][0][0] = ax.get_xlim()[0]
    pts[0][3][0] = ax.get_xlim()[0]
    pts[0][1][0] = ax.get_xlim()[1]
    pts[0][2][0] = ax.get_xlim()[1]
    pts[0][0][1] = ax.get_ylim()[0]
    pts[0][1][1] = ax.get_ylim()[0]
    pts[0][2][1] = ax.get_ylim()[1]
    pts[0][3][1] = ax.get_ylim()[1]
    ptsT[0][0] = ax.get_xlim()[0]
    ptsT[3][0] = ax.get_xlim()[0]
    ptsT[1][0] = ax.get_xlim()[1]
    ptsT[2][0] = ax.get_xlim()[1]
    ptsT[0][1] = ax.get_ylim()[0]
    ptsT[1][1] = ax.get_ylim()[0]
    ptsT[2][1] = ax.get_ylim()[1]
    ptsT[3][1] = ax.get_ylim()[1]

    A = dict(vertices=ptsT, segments=seg0T)
    meshObj = tr.triangulate(A)
    plt.close(fig)
    
    return (pts, seg0, meshObj, lCols, rCols)
    
    

tri_obj = form_tri_mesh('xmls/snake/lady_bug.xml')
