from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    ans = defaultdict(list)

    for s in strs:
        key = [0] * 26
        for c in s:
            key[ord(c) - ord('a')] += 1
        
        key = tuple(key)

        ans[key].append(s)

    return list(ans.values())


if __name__ == "__main__":
    input_data = [
        ["eat", "tea", "tan", "ate", "nat", "bat"],
        [""],
        ["a"]
        ]
    for strs in input_data:
        print(group_anagrams(strs))