import time

participants =  set() #List of all participants

def openFile(file):
    D = None
    n = []
    N = None
    d = []
    m = []
    with open(file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith("m ="):
            matrix_lines = lines[lines.index(line) + 1:]  # Get subsequent lines for the matrix
            for matrix_line in matrix_lines:
                if matrix_line.strip().startswith("["):
                    row = list(map(float, matrix_line.strip('[ ]\n').split()))
                    m.append(row)
        else:
            line = line.strip()
            if line.startswith("D ="):
                D = int(line.split('=')[1].strip(';'))
            elif line.startswith("n ="):
                n = list(map(int, line.split('=')[1].strip('[ ];\n').split()))
            elif line.startswith("N ="):
                N = int(line.split('=')[1].strip(';'))
            elif line.startswith("d ="):
                d = list(map(int, line.split('=')[1].strip('[ ];\n').split()))
    return (D,n,N,d,m)

def calculate_compatibility(participants):
    # Calculate the average compatibility score for the current participants
    total_score = 0
    count = 0
    for i in participants:
        for j in participants:
            if i != j:
                total_score += m[i][j]
                count += 1
    return total_score / count if count > 0 else 0

def isDepartmentCompleted(candidates):
    if len(candidates) == 0:
        return False


    is_full = sum(1 for person in participants if d[person] == d[candidates[0]]) == n[d[candidates[0]]-1]
    if is_full:
        return True
    return isDepartmentCompleted(candidates[1:])

def addCandidates(candidates):
    if not isDepartmentCompleted(candidates):
        for candidate in candidates:
            participants.add(candidate)


if __name__ == "__main__":
    (D,n,N,d,m) = openFile("project.2.dat")
    last_best_pair = (0,0)
    start_time = time.time()
    while len(participants)<sum(n):
        #Getting pair with the best value
        best_value = 0
        best_pair = (0,0)
        for i, row in enumerate(m):
            for j, pair_value in enumerate(row):
                if i < j and (i not in participants or j not in participants) and not isDepartmentCompleted([i,j]):
                    if pair_value > best_value:
                        best_pair = (i,j)
                        best_value = pair_value
        i = best_pair[0]
        j = best_pair[1]
        #Check for constraints
        if best_value > 0.15:
            addCandidates(best_pair)
        else:
            for k in range(N):
                if k != i and k != j:
                    if m[i][k] > 0.85 and m[j][k] > 0.85:
                        addCandidates([i, j, k])
        if last_best_pair==best_pair:
            break
        last_best_pair = best_pair
    end_time = time.time()
    if len(participants) != sum(n):
        print("Infeasible")
    else:
        print(participants)
        print(calculate_compatibility(participants))
        elapsed_time = end_time - start_time
        print("Time: "+str(elapsed_time))