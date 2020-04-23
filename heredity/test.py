PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

one_gene = {"Harry"}
two_genes = {"James"}
have_trait = {"James"}
names = list(people.keys())
people_data = dict()

for name in names:
    people_data[name] = [0, False]

# update data info for people in each group
for person in one_gene:
    people_data[person][0] = 1

for person in two_genes:
    people_data[person][0] = 2

for person in have_trait:
    people_data[person][1] = True

joint_output = 1
    
print(people_data)

for person, data in people.items():
    num_genes = people_data[person][0]
    trait = people_data[person][1]
    p_trait_given_genes = PROBS["trait"][num_genes][trait]
    # people without parents data
    if not people[person]["mother"] and not people[person]["father"]:    
        p_genes = PROBS["gene"][num_genes]    
    # person has parents data
    else:
        mother_num_genes = people_data[data["mother"]][0]
        father_num_genes = people_data[data["father"]][0]

        # gene origin probabilities
        from_mother_probs = {
            True: 0,
            False: 0
        }
        from_father_probs = {
            True: 0,
            False: 0
        }

        if mother_num_genes == 2:
            from_mother_probs[True] = 1 - PROBS["mutation"]
        elif mother_num_genes == 1:
            from_mother_probs[True] = 0.5
        elif mother_num_genes == 0:
            from_mother_probs[True] = PROBS["mutation"]
        from_mother_probs[False] = 1 - from_mother_probs[True]

        if father_num_genes == 2:
            from_father_probs[True] = 1 - PROBS["mutation"]
        elif father_num_genes == 1:
            from_father_probs[True] = 0.5
        elif father_num_genes == 0:
            from_father_probs[True] = PROBS["mutation"]
        from_father_probs[False] = 1 - from_father_probs[True]
 
        if num_genes == 1:
            p_genes = from_mother_probs[True] * from_father_probs[False] + from_mother_probs[False] * from_father_probs[True]
        elif num_genes == 2:
            p_genes = from_mother_probs[True] * from_father_probs[True] 
        elif num_genes == 0:
            p_genes = from_mother_probs[False] * from_father_probs[False]

    p_person = p_genes * p_trait_given_genes
    print(person)
    print(p_genes)
    print(p_trait_given_genes)
    print(p_person)
    joint_output *= p_person
print("Joint Probability:")
print(joint_output)
