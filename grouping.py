import random
import os

APP_ENV = os.getenv("APP_ENV", "prod") 

def parse_names(input_str):
    return [name.strip() for name in input_str.split(",") if name.strip()]

def assign_balanced_groups(singles, doubles, n_groups):
    singles = singles[:]
    doubles = doubles[:]
    random.shuffle(singles)
    random.shuffle(doubles)
    people = [(name, 2) for name in doubles] + [(name, 1) for name in singles]
    groups = [{'members': [], 'weight': 0} for _ in range(n_groups)]
    for name, weight in people:
        idx = min(range(n_groups), key=lambda i: groups[i]['weight'])
        groups[idx]['members'].append((name, weight))
        groups[idx]['weight'] += weight
    return groups

def main():
    singles = parse_names(input("Unesi samce (comma-separated):\n"))
    doubles = parse_names(input("Unesi parove (comma-separated):\n"))
    overlapping = set(singles) & set(doubles)
    if overlapping:
        if APP_ENV == "dev":
            print(f"Warning: These names appear in both singles and doubles; treating them as doubles: {', '.join(overlapping)}")
    singles = [s for s in singles if s not in overlapping]
    n_groups = int(input("Unesi broj grupa:\n"))
    groups = assign_balanced_groups(singles, doubles, n_groups)
    if APP_ENV == "dev":
        print("\nGroups (showing members and group weight):")
    else:
        print("Grupe:")
    for i, group in enumerate(groups, 1):
        members_str = ", ".join(f"{name} (x2)" if weight == 2 else name for name, weight in group['members'])
        if APP_ENV == "dev":
            print(f"Group {i} (weight {group['weight']}): {members_str}")
        else:
            print(f"Grupa {i}: {members_str}")
        

if __name__ == "__main__":
    main()