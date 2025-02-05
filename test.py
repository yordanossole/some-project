# x1 = [[1,2],[3,4],[5,6]]

# x2 = [[1,10],[10,20]]

# z = [[37,49],[5,17],[8,32]]
# for i in range(left, right+1):
    
# def check(ranges, left, right):
#     for arr in ranges:
#         if left in range(arr[0], arr[1]+1):
#             left = True
#         if right in range(arr[0], arr[1]+1):
#             right = True
#     if not isinstance(left, bool):
#         left = False
#     if not isinstance(right, bool):
#         right = False
#     return left and right

# print('return', check(z, 29, 49))
# # print(check(x2, 21, 21))



s = "leetcode"
t = "practice"
# s = "anagram"
# t = "mangaar"
# s = "bab"
# t = "aba"

def anagram(s, t):
    dic_s = dict()
    dic_t = dict()

    for char in s:
        if not char in dic_s.keys():
            dic_s[char] = 1
        else:
            dic_s[char] += 1

    for char in t:
        if not char in dic_t.keys():
            dic_t[char] = 1
        else:
            dic_t[char] += 1

    # print('s',dic_s)
    # print('t',dic_t)

    result = 0

    for char in list(dic_t.keys()):
        if char in list(dic_s.keys()):
            dic_t[char] -= dic_s[char]
            result += max(0, dic_t[char])
            # print('a',result)
        else:
            result += dic_t[char]
            # print('b',result)

    return result
# print(anagram(s, t))

nums = [1,1,1,2,2,3]
k = 2

def fun(nums, k):
    mod = dict()
    for num in nums:
        if not num in mod:
            mod[num] = 1
        else:
            mod[num] += 1
    sorted_dic = dict(sorted(mod.items(), key= lambda num: num[1]))
    return list(sorted_dic.keys())[-k:]

# print(fun(nums, k))

def areAlmostEqual(s1: str, s2: str):
    print(set(s1), set(s2))
    if set(s1) != set(s2):
        return False
    my_list = [pair for pair in zip(s1,s2)]
    print(my_list)
    counter = 0
    for pair in my_list:
        if pair[0] != pair[1]:
            counter+=1
            print('current counter: ', counter)
    print('final counter: ', counter)
    if counter == 0 or counter == 2:
        return True
    else:
        return False

s1 = "caa"
s2 = "aaz"
#
print(areAlmostEqual(s1,s2))