from itertools import combinations

def find_core_combinations(cores, core_count, enumerate_mode, mode):
    if mode == 1: #4核6技
        selected_len = 6
        hold_len = 4
    elif mode == 2:
        selected_len = 9
        hold_len = 6

    selected = [0] * selected_len
    hold = [0] * hold_len
    check_dup = True
    ans = 1

    print("start")

    # Generate all possible combinations of 4 cores
    for hold in combinations(range(0,core_count), hold_len):
        selected = [0] * selected_len

        # Count the skills in the selected cores
        for core_index in hold:
            for skill_index in cores[core_index]:
                selected[skill_index-1] += 1

        # Check if each skill appears exactly twice
        if all(selected[skill_index] == 2 for skill_index in range(0, selected_len - 1)):
            check_dup = False
            # Check for duplicates in the main skills
            print(f'-----------------------------第{ans}組解-----------------------------')
            ans += 1
            for core_index in hold:
                print(f"核心編號:{core_index + 1}, {cores[core_index]}")
            if enumerate_mode == 2:
                return
                
    if check_dup:
        print(f"未找到完美的{hold_len}核{selected_len}技")


def main():
    # 參數設定區
    mode = 1  # 設定'1'找4核6技 ,'2'找6核9技
    enumerate_mode = 2  # 設 '1' 列出所有解, 設 '2' 列第一組合乎成本解

    # 請在陣列s1中輸入您持有的核心，用來找四核六技，以','分隔
    cores = [[1,2,3],[3,2,1],[4,5,6],[6,5,4],[2,3,1]]

    # 解析輸入數據
    core_count = len(cores) #核心總數量

    # 搜尋核心組合
    find_core_combinations(cores, core_count, enumerate_mode, mode)

if __name__ == "__main__":
    main()
