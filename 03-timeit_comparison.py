import timeit

def read_file(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        return file.read()

def boyer_moore(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0:
        return -1
    skip = {c: m for c in set(text)}
    for i in range(m - 1):
        skip[pattern[i]] = m - i - 1
    i = m - 1
    comparisons = 0
    while i < n:
        j = m - 1
        while j >= 0 and text[i] == pattern[j]:
            comparisons += 1
            i -= 1
            j -= 1
        comparisons += 1  
        if j == -1:
            return i + 1, comparisons
        else:
            i += skip.get(text[i], m)
    return -1, comparisons

def kmp(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0:
        return -1
    lps = [0] * m
    j = 0
    i = 1
    comparisons = 0
    while i < m:
        if pattern[i] == pattern[j]:
            comparisons += 1
            j += 1
            lps[i] = j
            i += 1
        else:
            comparisons += 1
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    i = 0
    j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j, comparisons
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1, comparisons

def rabin_karp(text, pattern):
    m, n = len(pattern), len(text)
    if m == 0:
        return -1
    hash_pattern = hash(pattern)
    comparisons = 0
    for i in range(n - m + 1):
        comparisons += 1
        if hash(text[i:i + m]) == hash_pattern and text[i:i + m] == pattern:
            return i, comparisons
    return -1, comparisons

def test_algorithm(algorithm, text, pattern):
    start_time = timeit.default_timer()
    result, comparisons = algorithm(text, pattern)
    elapsed_time = timeit.default_timer() - start_time
    if result == -1:
        return f"Підрядок не знайдений, Час: {elapsed_time:.6f} сек, Порівняння: {comparisons}"
    else:
        return f"Підрядок знайдений на позиції {result}, Час: {elapsed_time:.6f} сек, Порівняння: {comparisons}"


text1 = read_file("article-1.txt")
text2 = read_file("article-2.txt")

patterns = [
    "Distance Learning",
    "RDF Database Systems: Triples Storage and SPARQL Query Processing",
    "неіснуючийпідрядок"
]


for i, text in enumerate([text1, text2]):
    for pattern in patterns:
        print(f"Тестування для статті {i+1} (Підрядок: {pattern}):")
        print(test_algorithm(boyer_moore, text, pattern))
        print(test_algorithm(kmp, text, pattern))
        print(test_algorithm(rabin_karp, text, pattern))
        print()
