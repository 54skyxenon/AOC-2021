from typing import List, Dict, Set
from collections import defaultdict

def build_graph(edges : List[str]) -> Dict[str, Set[str]]:
    ''' Build the graph data structure's vertices and edges, represented as a Dict. '''
    graph = defaultdict(set)
    for edge in edges:
        u, v = edge.split('-')
        graph[u].add(v)
        graph[v].add(u)

    return graph

def part1(edges : List[str]) -> int:
    ''' Solve part 1 '''
    graph = build_graph(edges)
    seen = {'start'}

    def DFS(curr):
        ''' Count number of paths visiting no small cave more than once. '''
        if curr == 'end':
            return 1
        
        ans = 0
        for nei in graph[curr]:
            if nei == nei.upper() or nei not in seen:
                seen.add(nei)
                ans += DFS(nei)
                seen.discard(nei)

        return ans
    
    return DFS('start')

def part2(edges : List[str]) -> int:
    ''' Solve part 2 '''
    graph = build_graph(edges)
    seen = {'start'}

    def DFS(curr, seen_twice):
        ''' Count number of paths visiting no one small cave more than twice,
            and no other small cave more than once. '''
        if curr == 'end':
            return 1
        
        ans = 0
        for nei in graph[curr]:
            if nei == nei.upper() or nei not in seen:
                seen.add(nei)
                ans += DFS(nei, seen_twice)
                seen.discard(nei)
            elif nei != 'start' and not seen_twice:
                ans += DFS(nei, True)
        
        return ans

    return DFS('start', False)

with open('day12.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]
    print(part1(lines))
    print(part2(lines))