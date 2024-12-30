def single_policy2boolean_expr(binary_str):
    expression = []
    for i in range(len(binary_str)):
        if int(binary_str[i]) == 0:
            expression.append("1")
        else:
            expression.append("0")
    
    return "( " + " OR ".join(expression) + " )"

def policy2booean_expr(policies, max_length):
    policies = [format(policy, f'0{max_length}b') for policy in policies]

    expressions = []
    for policy in policies:
        expressions.append(single_policy2boolean_expr(policy))
    
    return " AND ".join(expressions)

if __name__ == "__main__":
    policy = [7, 12, 3]
    print(policy2booean_expr(policy, 4))