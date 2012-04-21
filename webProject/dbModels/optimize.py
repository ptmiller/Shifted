# what up haters?

# draconian algorithm
def optimize(employees, shifts):
    # populate the number of shifts that remain to be filled
    shift_to_fill = {}
    emp_to_assign = {}

    # a matrix that details shift/employee preference
    matrix_haters = [[0]*len(shifts) for i in range(len(employees))]
    for i in range(len(shifts)):
        for j in range(len(employees)):
            rating = 0
            for k in range(len(employees[j].choices)):
                if (employees[j].choices[k] == shifts[i].idNum):
                    rating = k
            matrix_haters[i][j] = rating

    for i in shifts:
        shift_to_fill[i] = i.staffNum
    for i in employees:
        emp_to_assign[i] = len(i.choices)

    # repeating steps until all of the shifts have been allocated
    while True:
        worst = 0
        # find the appropriate shift to allocate next
        for key in shift_to_fill:
            best = []
            for key2 in emp_to_assign:
                best.append(key2.choices[]
        # allocate the shift, decrement the appropriate counters

        # if we have not found a shift to allocate, quit
