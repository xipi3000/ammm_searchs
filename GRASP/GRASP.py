import random
import time
participants = set()

# Open file and read input data
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
            matrix_lines = lines[lines.index(line) + 1:]
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

def calculate_compatibility(participants):
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

    is_full = sum(1 for person in participants if d[person] == d[candidates[0]]) == n[d[candidates[0]] - 1]
    if is_full:
        return True
    return isDepartmentCompleted(candidates[1:])

def addCandidates(candidates):
    if not isDepartmentCompleted(candidates):
        for candidate in candidates:
            participants.add(candidate)

def is_valid_committee(committee):
    department_counts = [0] * D
    for participant in committee:
        department_counts[d[participant] - 1] += 1
    return department_counts == n

def get_neighbors(current_committee):
    neighbors = []
    for participant_out in current_committee:
        for participant_in in range(N):
            if participant_in not in current_committee:
                new_committee = current_committee.copy()
                new_committee.remove(participant_out)
                new_committee.add(participant_in)
                if is_valid_committee(new_committee):
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
                break

    return current_committee, current_score

def grasp(D, n, N, d, m, max_iterations, alpha):

    best_committee = None
    best_score = -1
    iterations = 0

    while iterations < max_iterations:

        #print(iterations)

        participants.clear()

        RCL = build_RCL(alpha, N, m)
        committee = construct_solution(RCL)


        if not check_compatibility(m,committee):
            iterations += 1
            continue

        final_committee, final_score = local_search(committee)

        if final_score > best_score:
            best_committee = final_committee
            best_score = final_score

        iterations += 1

    if best_committee is None:
        return "Infeasible"

    return best_committee, best_score

def build_RCL(alpha, N, matrix):

    RCL = []
    candidate_pairs = []

    for i in range(N):
        for j in range(i + 1, N):
            if not mediator_constraint(i, j):
                continue
            candidate_pairs.append((i, j, matrix[i][j]))

    candidate_pairs.sort(key=lambda x: x[2])

    num_candidates = len(candidate_pairs)
    cutoff = int(alpha * num_candidates)


    RCL = [pair[:2] for pair in candidate_pairs[:cutoff]]


    remaining_pairs = candidate_pairs[cutoff:]
    random.shuffle(remaining_pairs)
    RCL += [pair[:2] for pair in remaining_pairs]

    random.shuffle(RCL)

    return RCL


def construct_solution(RCL):
    committee = set()
    for i, j in RCL:
        if i not in committee and j not in committee:

            committee.add(i)
            committee.add(j)
            if len(committee) >= sum(n):
                break
    return committee

# Check mediator constraint
def mediator_constraint(i, j):
    if m[i][j] >= 0.15:
        return True
    else:
        for k in range(N):
            if m[i][k] > 0.85 and m[j][k] > 0.85:
                return True
        return False


def check_compatibility(matrix, candidates):
    candidates_list = list(candidates)
    for i in range(len(candidates_list)):
        for j in range(i + 1, len(candidates_list)):
            person_i = candidates_list[i]
            person_j = candidates_list[j]

            compat_ij = matrix[person_i][person_j]

            if compat_ij == 0.0:
                return False

            if compat_ij < 0.15:
                found_compatible_k = False
                for k in range(len(matrix)):
                    if k != person_i and k != person_j:
                        compat_ik = matrix[person_i][k]
                        compat_jk = matrix[person_j][k]

                        if compat_ik > 0.85 and compat_jk > 0.85:
                            found_compatible_k = True
                            break

                if not found_compatible_k:
                    return False

    return True

if __name__ == "__main__":

    start_time = time.time()

    # Filename for data input
    filename = '../data/instance-16.dat'
    (D, n, N, d, m) = openFile(filename)

    # Max iterations for GRASP
    max_iterations = 100
    # Alpha value for RCL
    alpha = 0.9
    result = grasp(D, n, N, d, m, max_iterations, alpha)

    if result == "Infeasible":
        print("Infeasible")
    else:
        best_committee, best_score = result
        print("Best Committee:", best_committee)
        print("Best Compatibility Score:", best_score)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time: "+str(elapsed_time))

