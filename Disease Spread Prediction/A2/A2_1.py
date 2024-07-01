import math

def distribution(A, t0, t1, t2, alpha, gamma, rho, epsilon, T):
    state_vector = [1, 0, 0, 0, 0, 0, 0]

    L = 365
    beta = A[1][2] + A[1][3]

    for t in range(T):
        #Vaccination
        PSV = 0 if t < t0 else alpha * (t - t0)
        PSS = ((1-PSV)*A[0][0])/(A[0][1]+A[0][0]) #if t>=t0 else A[0][0]
        PSE = ((1-PSV)*A[0][1])/(A[0][1]+A[0][0]) #if t>=t0 else A[0][1]

        #Social Distancing
        PEI = beta if t < t1 or t > t2 else gamma * beta

        #Seasonal Variation
        PSE = PSE + epsilon * math.sin(2 * math.pi * t / L)
        PSS = PSS - epsilon * math.sin(2 * math.pi * t / L)

        A[0][0] = PSS
        A[0][1] = PSE

        next_state_vector = [
            state_vector[0] - PSE * state_vector[0] - PSV * state_vector[0] + A[5][0] * state_vector[5],
            state_vector[1] + PSE * state_vector[0] - PEI * state_vector[1],
            state_vector[2] + rho * PEI * state_vector[1] - A[2][4] * state_vector[2] - A[2][6] * state_vector[2],
            state_vector[3] + (1 - rho) * PEI * state_vector[1] - A[3][4] * state_vector[3] - A[3][6] * state_vector[3],
            state_vector[4] + A[2][4] * state_vector[2] + A[3][4] * state_vector[3],
            (1- A[5][0] ) * state_vector[5] + PSV * state_vector[0],
            state_vector[6] + A[3][6] * state_vector[3] + A[2][6] * state_vector[2]
        ]

        state_vector = next_state_vector

    return state_vector

#Input
A = []

for _ in range(7):
    row = input().split()
    row_float = [float(num) for num in row]
    A.append(row_float)

t_values = input().split()
t0, t1, t2 = int(t_values[0]), int(t_values[1]), int(t_values[2])

parameters = input().split()
alpha, gamma, rho, epsilon = float(parameters[0]), float(parameters[1]), float(parameters[2]), float(parameters[3])
T = int(input())


result = distribution(A, t0, t1, t2, alpha, gamma, rho, epsilon, T)

# Output
print(*result)