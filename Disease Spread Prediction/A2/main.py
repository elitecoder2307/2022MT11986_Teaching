import numpy as np

def simulate(prob, t0, t1, t2, alpha, gamma, rho, epsilon, T):
    state_vector = [1, 0, 0, 0, 0, 0, 0]

    L = 365
    beta = prob[1][2] + prob[1][3]

    for t in range(T):
        #Vaccination
        PSV = 0 if t < t0 else alpha * (t - t0)
        PSS = ((1-PSV)*prob[0][0])/(prob[0][1]+prob[0][0]) #if t>=t0 else prob[0][0]
        PSE = ((1-PSV)*prob[0][1])/(prob[0][1]+prob[0][0]) #if t>=t0 else prob[0][1]

        #Social Distancing
        PEI = beta if t < t1 or t > t2 else gamma * beta

        #Seasonal Variation
        PSE = PSE + epsilon * np.sin(2 * np.pi * t / L)
        PSS = PSS - epsilon * np.sin(2 * np.pi * t / L)

        prob[0][0] = PSS
        prob[0][1] = PSE

        next_state_vector = [
            state_vector[0] - PSE * state_vector[0] - PSV * state_vector[0] + prob[5][0] * state_vector[5],
            state_vector[1] + PSE * state_vector[0] - PEI * state_vector[1],
            state_vector[2] + rho * PEI * state_vector[1] - prob[2][4] * state_vector[2] - prob[2][6] * state_vector[2],
            state_vector[3] + (1 - rho) * PEI * state_vector[1] - prob[3][4] * state_vector[3] - prob[3][6] * state_vector[3],
            state_vector[4] + prob[2][4] * state_vector[2] + prob[3][4] * state_vector[3],
            (1- prob[5][0] ) * state_vector[5] + PSV * state_vector[0],
            state_vector[6] + prob[3][6] * state_vector[3] + prob[2][6] * state_vector[2]
        ]

        state_vector = next_state_vector

    return state_vector


