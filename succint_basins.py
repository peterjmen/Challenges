def read_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(x) for x in line.strip()]
            matrix.append(row)
    return matrix

def pad_matrix(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    padded_matrix = [[9 for _ in range(columns + 2)] for _ in range(rows + 2)]
    for i in range(rows):
        for j in range(columns):
            padded_matrix[i + 1][j + 1] = matrix[i][j]
    return padded_matrix

def find_low_points(matrix):
    rows = len(matrix) - 2
    columns = len(matrix[0]) - 2
    risk_level = 0
    low_point_counter = 0
    low_point_locations = []

    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            if (matrix[i][j] < matrix[i - 1][j] and
                matrix[i][j] < matrix[i + 1][j] and
                matrix[i][j] < matrix[i][j - 1] and
                matrix[i][j] < matrix[i][j + 1]):
                
                risk_level += matrix[i][j] + 1
                low_point_counter += 1
                low_point_locations.append((i, j))

    return risk_level, low_point_counter, low_point_locations

def calculate_basin_sizes(matrix, low_point_locations):
    rows = len(matrix)
    columns = len(matrix[0])
    basin_sizes = []
    unique_identifier = 10
    
    for (i, j) in low_point_locations:
        matrix[i][j] = unique_identifier
        unique_identifier += 1
    
    changes_made = True
    while changes_made:  # Continue until no changes are made in the matrix
        changes_made = False
        for i in range(1, rows-1):
            for j in range(1, columns-1):
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if matrix[i + dx][j + dy] >= 10 and matrix[i][j] < 9:
                        matrix[i][j] = matrix[i + dx][j + dy]
                        changes_made = True
    
    for id in range(10, unique_identifier):
        basin_sizes.append(sum(row.count(id) for row in matrix))
    
    return basin_sizes


def print_matrix(matrix, low_points):
    low_points_set = set(low_points)
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if (i, j) in low_points_set:
                print('\033[91m' + str(val) + '\033[0m', end=' ')
            else:
                print(val, end=' ')
        print()

matrix_original = read_matrix('dev_task/input.txt')
matrix_padded = pad_matrix(matrix_original)
risk_level, low_point_count, low_point_locations = find_low_points(matrix_padded)
print_matrix(matrix_padded, low_point_locations)

print(f"\nThere are {low_point_count} low points total.")
print(f"The risk level is {risk_level}.")
# for idx, (x, y) in enumerate(low_point_locations, start=1):
#     print(f"Low point {idx} at Location x: {x-1}, y: {y-1} (0 indexed)")  # Subtracting 1 for 0 indexing

basin_sizes = calculate_basin_sizes(matrix_padded, low_point_locations)
basin_sizes.sort()
print("\nBasins ordered smallest to largest:")
print(basin_sizes)

largest_basins = basin_sizes[-3:]
print("\nThe three largest basins from largest to smallest are:")
print(largest_basins)

three_largest_basins_multiplied = largest_basins[0] * largest_basins[1] * largest_basins[2]
print(f"\nthree_largest_basins_multiplied is: {three_largest_basins_multiplied}")
