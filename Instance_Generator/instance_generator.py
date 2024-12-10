import random


def openFile(file):
    n = []
    N = None
    comp_range = []
    with open(file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("n ="):
            n = list(map(int, line.split('=')[1].strip('[ ]\n').split()))
        elif line.startswith("N ="):
            N = int(line.split('=')[1])
        elif line.startswith("compatibility range"):
            comp_range = list(map(float,(line.split('=')[1].split(","))))
    return n,N,comp_range


if __name__ == "__main__":
    n, N,comp_range = openFile("instance.conf")

    d = []
    m = []
    D = len(n)
    for i in range(D):
        for _ in range(N//D):
            if len(d)>=N:
                break
            d.append(i+1)


    for i in range(N):
        row = []
        for j in range(N):
            if i == j :
                row.append(1)
            elif i > j:
                row.append(m[j][i])
            else:
                row.append(random.uniform(comp_range[0],comp_range[1]))
        m.append(row)

    with open("output.dat", "w") as file:
        file.write(f"D = {D};\n")
        file.write(f"n = [ {' '.join(map(str, n))} ];\n")
        file.write(f"N = {N};\n")
        file.write(f"d = [ {' '.join(map(str, d))} ];\n")
        file.write("m = [\n")
        for row in m:
            file.write("    [ " + ' '.join(f"{val:.2f}" for val in row) + " ]\n")
        file.write("];\n")