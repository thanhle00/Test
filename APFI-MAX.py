import math
import itertools
def read_data(file_path):
    with open(file_path, 'r') as file:
        transactions = {}
        for i, line in enumerate(file):
            items = [int(item) for item in line.strip().split(' ')]
            transactions[i] = items
    return transactions


def lb(minsup, minpro):
    lower_bound = (2 * minsup - math.log(minpro) - math.sqrt(math.log(minpro) ** 2 - 8 * minpro * math.log(minpro))) / 2
    return lower_bound
def ub(minsup,minpro):
    upper_bound = minsup - math.log(1 - minpro) + math.sqrt(math.log(1-minpro)**2 - 2 * minpro * math.log(1 - minpro))
    return upper_bound


def cgeb(UD, minsup, minpro):
    C = []  # List to store all candidate itemsets
    L = set()
    for transaction in UD.values():
        L.update(transaction)

    for X in L:
        E = 0  # Expected support
        Var = 0  # Variance
        count = 0  # Count of transactions containing the item

        for transaction in UD.values():
            if X in transaction:
                # Assuming each occurrence of an item has a uniform probability
                pj = 1# Set a fixed probability for each item
                E += pj
                Var += pj * (1 - pj)
                count += 1

        if E >= lb(minsup, minpro) and count >= minsup:
            C.append((X, E, Var, count))  # Add item to candidates

    return C


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
    frequency = 1 - math.exp((minsup - E) / math.sqrt(Var))
    # print(E)
    return frequency > lb(minsup,minpro)



#APFI_MAX algorithm
def apfi_max(UD, minsup, minpro):
    candidates = cgeb(UD, minsup, minpro)
    RES = set()
    E = sum(UD)
    Var = sum(j * (1 - j) for j in UD)
    
    for i in range(len(candidates) - 1, -1, -1):
        X, E, Var, count = candidates[2]
        print(E)
        # print(Var)
        if fm(minsup, minpro, E, Var):
            RES.add(X)

    return RES

# Generate all non-empty subsets of a set
# def generate_subsets(s):
#     result = []
#     for i in range(1, len(s)):
#         result.extend(itertools.combinations(s, i))
#     return result
minsup = 5
minpro = 0.05

print(lb(minsup,minpro))
candidates = cgeb(UD, minsup, minpro)
confirmed_pmfi = apfi_max(UD, minsup, minpro)
print(confirmed_pmfi)