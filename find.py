from itertools import combinations

def find_core_combinations(cores, core_count, enumerate_mode, selected_perfect_cores):
    len_selected_perfect_cores = len(selected_perfect_cores)
    if len_selected_perfect_cores in [1,2,3]:
        hold_len = 2
    elif len_selected_perfect_cores in [4]:
        hold_len = 3
    elif len_selected_perfect_cores in [5,6]:
        hold_len = 4
    elif len_selected_perfect_cores in [7]:
        hold_len = 5
    elif len_selected_perfect_cores in [8,9]:
        hold_len = 6
    elif len_selected_perfect_cores in [10]:
        hold_len = 7
    elif len_selected_perfect_cores in [11,12]:
        hold_len = 8
    elif len_selected_perfect_cores in [13]:
        hold_len = 9
    elif len_selected_perfect_cores in [14,15]:
        hold_len = 10

    perfect_core_combination = []

    # Generate all possible combinations of 4 cores
    for hold in combinations(range(0,core_count), hold_len):
        selected = [0] * 15

        # Count the skills in the selected cores
        for core_index in hold:
            for skill_index in cores[core_index]:
                selected[skill_index-1] += 1

        # Check if each skill appears exactly twice
        if all(selected[skill_index-1] == 2 for skill_index in selected_perfect_cores):
            # Check for duplicates in the main skills
            if hold_len == 2:
                perfect_core_combination.append([cores[hold[0]], cores[hold[1]]])
            else:
                perfect_core_combination.append([cores[hold[0]], cores[hold[1]], cores[hold[2]]])
            if enumerate_mode == 2:
                return perfect_core_combination
            
    return perfect_core_combination


def main():
    enumerate_mode = 1  # 設 '1' 列出所有解, 設 '2' 列第一組合乎成本解
    selected_perfect_cores = [4,9,13] # 完美核心
    cores = [[4, 9, 13], [9,4,13]] # 請在陣列s1中輸入您持有的核心，用來找四核六技，以','分隔
    core_count = len(cores)  # 核心總數量

    # 搜尋核心組合
    a = find_core_combinations(cores, core_count, enumerate_mode, selected_perfect_cores)
    print(a)

if __name__ == "__main__":
    main()
