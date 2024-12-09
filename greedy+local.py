import time

participants = set()  # List of all participants

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
    return (D, n, N, d, m)

def is_valid_compatibility(committee):
    department_counts = [0] * D
    compatible = True
    for i in committee:
        for j in committee:
            if i != j:
                if m[i][j]<=0:
                    return False
                elif m[i][j]<=0.15:
                    compatible = False
                    for k in committee:
                        if k != i and k != j:
                            if m[i][k] > 0.85 and m[j][k] > 0.85:
                                compatible = True

        if compatible:
            department_counts[d[i] - 1] += 1
    return department_counts == n

def get_neighbors(current_committee):
    neighbors = []
    for participant_out in current_committee:
        for participant_in in range(N):
            if participant_in not in current_committee:
                # Create a new committee by swapping
                new_committee = current_committee.copy()
                new_committee.remove(participant_out)
                new_committee.add(participant_in)
                if is_valid_compatibility(new_committee):  # Ensure the new committee is valid
                    neighbors.append(new_committee)
    return neighbors

def local_search(initial_committee):
    current_committee = set(initial_committee)
    current_score = calculate_compatibility(current_committee)
    improved = True
    while improved:
        improved = False
        neighbors = get_neighbors(current_committee)

        for neighbor in neighbors:
            neighbor_score = calculate_compatibility(neighbor)
            if neighbor_score > current_score:
                current_committee = neighbor
                current_score = neighbor_score
                improved = True
                break  # Move to the better neighbor immediately

    return current_committee, current_score
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

def isDepartmentCompleted(candidates,participants_future=set()):
    if len(candidates) == 0 or len(participants_future)==0:
        return False
    is_full = sum(1 for person in participants_future if d[person] == d[candidates[0]]) >= n[d[candidates[0]]-1]
    if is_full:
        return True
    participants_future.add(candidates[0])
    return isDepartmentCompleted(candidates[1:],participants_future)


def areCompatible(candidates):

    bigger_than_85 = True
    if len(participants)==0:
        return True
    for participant in participants:
        if participant != m[candidates[0]] and participant != m[candidates[0]]:
            if m[candidates[0]][participant] <= 0.15:
                bigger_than_85 = False
                for third_one in participants:
                    if m[candidates[0]][third_one] > 0.85 and m[candidates[1]][third_one] > 0.85:
                        return  True
            elif m[candidates[1]][participant] <= 0.15:
                bigger_than_85 = False
                for third_one in participants:
                    if m[candidates[0]][third_one] > 0.85 and m[candidates[1]][third_one] > 0.85:
                        return  True
    return bigger_than_85
def addCandidates(candidates):
    #print(participants)
    if areCompatible(candidates) and (not isDepartmentCompleted(candidates,participants)):
            for candidate in candidates:
                participants.add(candidate)
    print(participants)

if __name__ == "__main__":
    (D,n,N,d,m) = openFile("project.5.dat")
    older_searches = []
    start_time = time.time()
    max_itr = N
    itr = 0
    while len(participants)<sum(n) and not itr > max_itr:
        #Getting pair with the best value
        best_value = 0
        best_pair = (0,0)
        for i, row in enumerate(m):
            for j, pair_value in enumerate(row):
                if i < j and (i not in participants or j not in participants) and (i,j) not in older_searches: #and (i,j)!=last_best_pair: #and not isDepartmentCompleted([i,j],set.copy(participants)):
                    if pair_value >= best_value:
                        best_pair = (i,j)
                        best_value = pair_value
                        #print(i,j)

        i = best_pair[0]
        j = best_pair[1]
        if best_value > 0.15:
            addCandidates(best_pair)
        itr+=1
        older_searches.append(best_pair)
    end_time = time.time()
    if len(participants) != sum(n):
        print("Infeasible")
    else:
        print("Greedy Committee:", participants)
        print("Initial Compatibility Score:", calculate_compatibility(participants))

        # Local Search
        final_committee, final_score = local_search(participants)
        print("Final Committee after Local Search:", final_committee)
        print("Final Compatibility Score:", final_score)
