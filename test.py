import math
import random
def read_data(file_path):
    transactions = []
    with open(file_path, 'r') as file:
        for line in file:
            items = [int(item) for item in line.strip().split()]
            transactions.append(items)
    return transactions



def lb(minsup, minpro):
    lower_bound = (2 * minsup - math.log(minpro) - math.sqrt(math.log(minpro) ** 2 - 8 * minpro * math.log(minpro))) / 2
    return lower_bound
def ub(minsup,minpro):
    upper_bound = minsup - math.log(1 - minpro) + math.sqrt(math.log(1-minpro)**2 - 2 * minpro * math.log(1 - minpro))
    return upper_bound

# def expectation(UD):
#     return sum(UD)
# def variance(UD):
#     return sum(j * (1 - j) for j in UD)
# expectation = expectation(transactions)  # expectation value
# var = variance(UD)
# def expectation(UD):
#     return sum(UD) / len(UD)

# def variance(values):
#     expectation = expectation(values)
#     return sum((x - expectation) ** 2 for x in values) / len(values)
file_path = "Kosarak.txt"
transactions = read_data(file_path)
UD = transactions

# def calculate_expectation(transactions):
#     return sum(transactions) / len(transactions)
# expectation = calculate_expectation(transactions)
# print("E :",expectation)
# def calculate_variance(transactions):
#     return sum((x - expectation) ** 2 for x in transactions) / len(transactions)
# var = calculate_variance(UD)
# print("Var :",var)

def generate_pj():
    pj = random.gauss(.5,.125)
    return pj

# def generate_pj(expectation, var):
#     # Generate a random number 'z' following a standard normal distribution
#     z = random.uniform(0, 1) # Using uniform distribution as a replacement for Gaussian distribution
#     # Calculate the number following a Gaussian distribution with expectation 'mu' and standard deviation 'sigma'
#     pj = expectation + z * var
#     return pj
p = []

def cgeb(UD, minsup, minpro):
    i = 1
    L = set()
    for transaction in UD:
        for item in transaction:
            L.add(item) # Populate L with single attributes from UD
    
    C = []  # List to store itemsets
    prob_table = {x:generate_pj() for x in L}

    while True:
        Ci = []
        for X in L:
            E = 0
            Var = 0
            count = 0

            for transaction in UD:
                if X in transaction:
                    pj = prob_table[X]
                    p.append(pj)  # Placeholder for generating pj for X
                    E += pj
                    Var += pj * (1 - pj)
                    count += 1

                if E >= lb(minsup, minpro) and count >= minsup:
                    Ci.append((X, E, Var, count))  # Add item to Ci
                    break  # Exit inner loop

            if Ci:  # Check if Ci is not empty
                break  # Exit outer loop

        C.append(Ci)  # Add Ci to C
        i += 1
        # Update L according to Ci-1 (update L logic needs to be implemented)
        for itemset in Ci:
            L.update(itemset)
        if not L:  # If L is null or empty
            return C  # Return the candidates

    # return C


file_path = "Kosarak.txt"
transactions = read_data(file_path)
UD = transactions
minsup = 5
minpro = 0.05


candidates = cgeb(UD, minsup, minpro)
print("Candidates:", candidates)
# print("UD",UD)
#FM algorithm
def fm(minsup, minpro, E, Var):
     
    if E >= ub(minsup,minpro):
        return True
    else:
        frequency = 1 - math.exp((minsup - E) / math.sqrt((Var)**2))
    # print(E)
        return frequency < lb(minsup,minpro)



#APFI_MAX algorithm
def apfi_max(UD, minsup, minpro):
    candidates = cgeb(UD, minsup, minpro)
    RES = set()
    # E = sum(UD)
    # Var = sum(j * (1 - j) for j in UD)
    
    for i in range(len(candidates) - 1, -1, -1):
        
        X, E, Var, count = candidates[i]
        # print(E)
        # print(Var)
        if fm(minsup, minpro, E, Var):
            RES.add(X)
            

    return RES


minsup = 5
minpro = 0.05

# print(lb(minsup,minpro))
candidates = cgeb(UD, minsup, minpro)
confirmed_pmfi = apfi_max(UD, minsup, minpro)
print("Confirmed PMFI",confirmed_pmfi)

# import matplotlib.pyplot as plt
# plt.plot(p)
# plt.show()
# expectation = 203.0
# var = 13804.0
# values = [random.gauss(expectation, var) for _ in range(1000)]
# plt.hist(values, bins=30, density=True)
# plt.xlabel('Values')
# plt.ylabel('Frequency')
# plt.title('Gaussian ')
# plt.show()