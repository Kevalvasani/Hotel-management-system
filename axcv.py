# def analyze_names(names):
#     name_lengths = {}
#     for name in names:
#         length = len(name)
#         if length in name_lengths:
#             name_lengths[length].append(name)
#         else:
#             name_lengths[length] = [name]

#     sorted_lengths = sorted(name_lengths.items(), key=lambda x: len(x[1]), reverse=True)

#     print("Names:", names)
#     print("Name lengths:", [len(name) for name in names])

#     print("\nThe three most frequent name lengths are:")
#     for length, names_list in sorted_lengths[:3]:
#         print(f"{len(names_list)} names of length {length}: {names_list}")

#     print("\nThe three least frequent name lengths are:")
#     for length, names_list in sorted_lengths[-3:]:
#         print(f"{len(names_list)} names of length {length}: {names_list}")

# # Example input
# names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson',
#          'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White']

# analyze_names(names)
# ##############################################################################################

# def tokenize_sentences(sentences):
#     word_trees = [sentence.split() for sentence in sentences]
#     word_counts = {}
#     for sentence in word_trees:
#         for word in sentence:
#             if word in word_counts:
#                 word_counts[word] += 1
#             else:
#                 word_counts[word] = 1
#     return word_trees, word_counts

# # Example input
# sentences = ["My name is Ram", "He is a good person", "You should be careful while coding",
#              "He can do better", "The person is mysterious", "Jay Shree Ram", "It is my pen."]

# word_trees, word_counts = tokenize_sentences(sentences)

# print("Word trees:", word_trees)

# print("\nNumber of times each word appears:")
# print(word_counts)
# ############################################################################################

# def fibonacci(n, memo={}):
#     if n in memo:
#         return memo[n]
#     if n <= 1:
#         return n
#     else:
#         memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
#         return memo[n]

# # Example input
# N = 8
# result = fibonacci(N)
# print("Output:", result)

# # Check if the recursive function can handle larger values like 60 or 90
# try:
#     fib_60 = fibonacci(60)
#     print("60th Fibonacci term:", fib_60)
# except RecursionError:
#     print("Unable to calculate the 60th Fibonacci term with the recursive function.")

# try:
#     fib_90 = fibonacci(90)
#     print("90th Fibonacci term:", fib_90)
# except RecursionError:
#     print("Unable to calculate the 90th Fibonacci term with the recursive function.")
##############################################################################################

# import re

# def validate_emails(emails):
#     valid_emails = []
#     for email in emails:
#         if re.match(r'^[\w.-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$', email):
#             valid_emails.append(email)
#     return valid_emails

# # Example input
# emails = ['abc@gmail.com', '123$tt*@xyz.com', 'good@bad@uk.in', 'nasa@usa12.space',
#           'no-reply@domain.in', 'ramhanuman@saketa.lok', 'ruhi.mohan@exter123.123',
#           'fake@fake123.fakercom']

# # Filter valid emails
# valid_emails = validate_emails(emails)

# # Output
# print("Valid emails:", valid_emails)
###########################################################################################
def find_replace_AP(arithmetic_progression):
    common_difference = arithmetic_progression[1] - arithmetic_progression[0]
    for i in range(1, len(arithmetic_progression) - 1):
        if arithmetic_progression[i + 1] - arithmetic_progression[i] != common_difference:
            wrong_index = i
            break
    correct_value = arithmetic_progression[i] + common_difference
    arithmetic_progression[wrong_index] = correct_value
    return arithmetic_progression

def find_replace_GP(geometric_progression):
    common_ratio = geometric_progression[1] / geometric_progression[0]
    for i in range(1, len(geometric_progression) - 1):
        if geometric_progression[i + 1] / geometric_progression[i] != common_ratio:
            wrong_index = i
            break
    correct_value = geometric_progression[i] * common_ratio
    geometric_progression[wrong_index] = correct_value
    return geometric_progression

# Example input
wrong_AP = [2, 5, 8, 11, 15, 17]
wrong_GP = [3, 6, 9, 12, 16, 18]

# Find and replace wrong term in AP and GP
correct_AP = find_replace_AP(wrong_AP)
correct_GP = find_replace_GP(wrong_GP)

# Output
print("Correct A.P.:", correct_AP)
print("Correct G.P.:", correct_GP)
