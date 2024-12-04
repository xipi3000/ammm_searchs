# Example
D = 2  # Number of groups
n = [3, 3]  # Group sizes

N = 8  # Total number of participants
d = [1, 1, 1, 1, 2, 2, 2, 2]  # Group assignments for participants

m = [  # Compatibility matrix (NxN)
    [1.00, 0.50, 0.75, 0.90, 0.15, 0.40, 1.00, 0.90],
    [0.50, 1.00, 0.00, 0.00, 0.60, 0.80, 1.00, 0.00],
    [0.75, 0.00, 1.00, 0.25, 0.55, 0.75, 1.00, 0.60],
    [0.90, 0.00, 0.25, 1.00, 0.40, 0.20, 1.00, 0.10],
    [0.15, 0.60, 0.55, 0.40, 1.00, 0.15, 1.00, 0.15],
    [0.40, 0.80, 0.75, 0.20, 0.15, 1.00, 1.00, 0.20],
    [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
    [0.90, 0.00, 0.60, 0.10, 0.15, 0.20, 1.00, 1.00]
]


participants =  set() #List of all participants

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


while len(participants)!=sum(n):
    best_value = 0
    best_pair = (0,0)
    for i, row in enumerate(m):
        for j, pair_value in enumerate(row):
            if i != j and (i not in participants or j not in participants) and not isDepartmentCompleted([i,j]):
                if pair_value > best_value:
                    best_pair = (i,j)
                    best_value = pair_value
    i = best_pair[0]
    j = best_pair[1]
    print(best_value)
    if best_value > 0.15:
        print(best_pair)
        addCandidates([i, j])
    else:
        for k in range(N):
            if k != i and k != j:
                if m[i][k] > 0.85 and m[j][k] > 0.85:
                    addCandidates([i, j, k])
    print(participants)