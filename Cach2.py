import math
import random

"""
   Function : read_data(file_path)
   Input : file_path
   Output : transactions
"""
def read_data(file_path):
    with open(file_path, 'r') as file:
        transactions = {}
        for i, line in enumerate(file):
            items = [int(item) for item in line.strip().split(' ')]
            transactions[i] = items
    return transactions

file_path = "Kosarak.txt"
transactions = read_data(file_path)
UD = transactions
minsup = 2
minpro = 0.5

# Algorithm 1

"""
 Function : lb(minsup,minpro)
    Input :
        minsup : Integer - Minimum threshold T for desired support .
        minpro: Float - Minimum threshold τ for desired probability .
    Output: lower_bound : Float - Represents the calculated lower bound.
"""
def lb(minsup, minpro):
    # Calculate the lower bound
    lower_bound = (2 * minsup - math.log(minpro) - math.sqrt(math.log(minpro) ** 2 - 8 * minpro * math.log(minpro))) / 2
    return lower_bound
"""
 Function : ub(minsup,minpro)
    Input :
        minsup : Integer - Minimum threshold T for desired support .
        minpro: Float - Minimum threshold τ for desired probability .
    Output: upper_bound : Float - Represents the calculated upper bound.
"""
def ub(minsup,minpro):
    # Calculate the upper bound
    upper_bound = minsup - math.log(1 - minpro) + math.sqrt(math.log(1-minpro)**2 - 2 * minpro * math.log(1 - minpro))
    return upper_bound

"""
 Function : generate_pj()
    Input :
    Output: pj (Random Probability): Float - Represents the generated random probability.
"""
def generate_pj():
    # Generate a random probability using Gaussian distribution with mean 0.5 and std deviation 0.125
    return random.gauss(0.5, 0.125)
"""
Algorithm 1: CGEB
    Function : cgeb(UD,minsup,minpro)
    Input:
    UD: Uncertain database(dictionary type).
        Key : Transaction ID
        Value : List of item within the transaction
        UD = {
              0: [item_1, item_2, ...],
              1: [item_2, item_3, ...],
              ...}
    minsup : Integer - Minimum threshold T for desired support .
    minpro: Float - Minimum threshold τ for desired probability .

    Output:
    C: List - Contains the generated candidate itemsets for frequent itemsets.
    Each itemset is represented as a tuple containing:
        X: itemset.
        E: Float - Expected support.
        Var: Float - Variance.
        count: Integer - Count of transactions containing the item or itemset.
"""
def cgeb(UD, minsup, minpro):
    C = []  # List to store all candidate itemsets
    L = set()
    # p=[]
    previous_Ci = set()  # To store candidates from the previous iteration

    for transaction in UD.values():
      L.update(transaction)

    # Create a probability table for each item in L
    prob_table = {x:generate_pj() for x in L}

    while L:
      Ci = []

      for X in L:
          E = 0  # Expected support
          Var = 0  # Variance
          count = 0  # Count of transactions containing the item

          for transaction in UD.values():
              if X in transaction:
                  # Assuming each occurrence of an item has a uniform probability
                  pj = prob_table[X]# Set a fixed probability for each item
                  # p.append(pj)
                  E += pj
                  Var += pj * (1 - pj)
                  count += 1

          if E >= lb(minsup, minpro) and count >= minsup:
              Ci.append((X, E, Var, count))  # Add item to candidates

      C.append(Ci)  # Add Ci to C

      # Update L for the next iteration based on the previous Ci
      if previous_Ci:
          L = set([X for X, _, _, _ in previous_Ci])
      else:
          L = set()

      previous_Ci = set(Ci)  # Set previous_Ci as Ci for the next iteration

      # If L is empty, return C
      if not L:
          return C
    return C

candidates = cgeb(UD, minsup, minpro)
print("Candidates: ",candidates)

# Algorithm 3

"""
  Function : fm(minsup,minpro,E,Var)
    Input:
        minsup (Minimum Support): Integer - Represents the minimum threshold for expected support.
        minpro (Minimum Probability): Float - Represents the minimum threshold for probability of an item.
        E (Expected Support): Float - Represents the expected support of an item.
        Var (Variance): Float - Represents the variance associated with the item.
    Output:
        A Boolean value (True or False):
            True: If the evaluated itemset has expected support (E) greater than or equal to the minimum support threshold (minsup), or the predicted probability is significantly lower than the minimum probability threshold (minpro).
            False: If it fails to meet both of the above conditions.
"""
def fm(minsup, minpro, E, Var):

    if E >= ub(minsup,minpro):
        return True
    else:
        frequency = 1 - math.exp((minsup - E) / math.sqrt((Var)**2))
        return frequency < lb(minsup,minpro)

#Algorithm 2

import itertools

"""
Function apfi_max(UD,minsup,minpro)
  Input:
      UD (Uncertain Database): A dataset containing uncertain information, usually represented as a dictionary.
      minsup: Integer, the minimum threshold for the desired support.
      minpro: Float, the minimum threshold for the desired probability.
  Output:
      A list of tuples representing pairs of frequent itemsets:
        Each tuple contains two itemsets that are frequent based on the given thresholds.
"""

def apfi_max(UD, minsup, minpro):
    candidates = cgeb(UD, minsup, minpro)
    RES = set()
    Fre_Pre = set()
    Fre_Cur = set()

    for i in range(len(candidates) - 1, -1, -1):
        Ci = candidates[i]
        for itemset in Ci:
            X, E, Var, count = itemset

            if Fre_Pre and any(all(item in X for item in Fre_X) for Fre_X in Fre_Pre):
                Fre_Cur.add(X)
                continue

            if fm(minsup, minpro, E, Var):
                RES.add(X)
                Fre_Cur.add(X)

        Fre_Pre = Fre_Cur
        Fre_Cur = set()

        pairs = list(itertools.combinations(RES, 2))
    return pairs
print("UD",UD)
print("Confirmed PMFI" ,apfi_max(UD,minsup,minpro))