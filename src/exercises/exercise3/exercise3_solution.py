'''
Give input string s, check if the open and close parenthesis match up, see examples with output below:

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Example 4:
Input: s = "(((({}))))"
Output: true

Example 5:
Input: s = "))(("
Output: false

'''

brackets_map = {'(':')', '{':'}', '[':']'}

def check_paren_match(input_value):
    status:bool = True
    list_parens_read = []

    for item in input_value:
        # if no items in the read_list, just append and continue
        if len(list_parens_read) == 0:
            list_parens_read.append(item)
            continue
        # on paren match found pop, otherwise append to read_list
        if item == brackets_map.get(list_parens_read[-1], 'NotFound'):
            list_parens_read.pop()
        else:
            list_parens_read.append(item)

    # at the end if the item still exists in parens read into  list, then
    # match incomplete or error
    if  len(list_parens_read) > 0:
         status = False

    return status


s1 = "()"
s2 = "()[]{}"
s3 = "(]"
s4 = "(((({}))))"
s5 = "))(("

if __name__ == '__main__':
    print(f' {s1} : {check_paren_match(s1)}')
    print(f' {s2}: {check_paren_match(s2)}')
    print(f' {s3}: {check_paren_match(s3)}')
    print(f' {s4}: {check_paren_match(s4)}')
    print(f' {s5}: {check_paren_match(s5)}')
