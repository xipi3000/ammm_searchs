import time

participants =  set() #List of all participants in the solution

#Reeds file
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
    return (D,n,N,d,m)

#Calculates the compatibility score of all the persons in the given set
def calculate_compatibility(participants):
    total_score = 0
    count = 0
    for i in participants:
        for j in participants:
            if i != j:
                total_score += m[i][j]
                count += 1
    return total_score / count if count > 0 else 0

#Calculates if the department in the solution is full
def is_department_completed(candidate):
    is_full = sum(1 for person in participants if d[person] == d[candidate]) >= n[d[candidate]-1]
    if is_full:
        return True

    return False

#Calculates if the 0.85 mediator exists if it finds a pair with < 0.15 and also that the pair value isn't 0
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


#Adds the candidate if the constraints are correct
def add_candidates(candidate):
    if are_compatible(candidate) and (not is_department_completed(candidate)):
        participants.add(candidate)


if __name__ == "__main__":
    #Input file
    filename = "../data/instance-16.dat"

    (D,n,N,d,m) = open_file(filename)

    #Number of iterations
    max_itr = N

    older_searches = []
    start_time = time.time()
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
        print(participants)
        print(calculate_compatibility(participants))

        elapsed_time = end_time - start_time
        print("Time: "+str(elapsed_time))