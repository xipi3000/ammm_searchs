
import time

participants =  set() #List of all participants

def open_file(file):
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

def is_department_completed(candidate):
    is_full = sum(1 for person in participants if d[person] == d[candidate]) >= n[d[candidate]-1]
    if is_full:
        return True

    return False


def are_compatible(candidate):
    bigger_than_85 = True
    if len(participants)==0:
        return True
    for participant in participants:
        if participant != m[candidate]:
            if m[candidate][participant] <= 0.15:
                bigger_than_85 = False
                for third_one in participants:
                    if m[candidate][third_one] > 0.85 and m[participant][third_one] > 0.85:
                        return  True
    return bigger_than_85
def add_candidates(candidate):
    if are_compatible(candidate) and (not is_department_completed(candidate)):
        participants.add(candidate)


if __name__ == "__main__":
    (D,n,N,d,m) = open_file("project.8.dat")

    start_time = time.time()

    older_searches = []
    max_itr = N
    itr = 0
    while len(participants)<sum(n) and not itr > max_itr:
        numb_of_searches = 0
        total_of_searches = ((N * N) / 2)
        while numb_of_searches <= total_of_searches and len(participants)<sum(n):
            best_value = 0
            best_participant = -1
            for i in range(N):
                if (i not in participants) and i not in older_searches:
                        eval_participants = set.copy(participants)
                        eval_participants.add(i)
                        if calculate_compatibility(eval_participants) >= best_value:
                            best_participant = i
                            best_value = calculate_compatibility(eval_participants)
            add_candidates(best_participant)
            numb_of_searches+=1
            older_searches.append(best_participant)

        itr+=1
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
        elapsed_time = end_time - start_time
        print("Time: " + str(elapsed_time))