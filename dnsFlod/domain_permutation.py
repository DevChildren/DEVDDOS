# domain_permutation.py

import random

def generate_domain_permutations(domain, count=10):
    permutations = set()
    domain_parts = domain.split('.')
    base = domain_parts[0]
    
    while len(permutations) < count:
        # Acak panjang substring dari base dan tambahkan karakter acak untuk membuat variasi domain
        permutation = base[:random.randint(1, len(base))] + ''.join(random.choices('09876543210zxcvbnmasdfghjklqwertyuiop', k=random.randint(5, 8)))
        permutations.add(f"{permutation}.{domain_parts[1]}")
        
    return list(permutations)
