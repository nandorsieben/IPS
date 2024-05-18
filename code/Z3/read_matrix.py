def read_matrix(filename):
    Mat=[]
    with open(filename, "r") as f:
        for line in f:
            integer_tuple = tuple(int(x) for x in line.strip().split())
            Mat.append(integer_tuple)
    return Mat
