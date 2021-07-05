class CFG:
    def __init__(self, non_terminal, string):
        self.non_terminal = non_terminal
        self.first = set()
        self.follow = set(("$"))
        self.instances = string.split('|')

def main():
    cfg = read_CFG("cfg.txt")
    
    # 2D array containg nonterminals and their statements
    cleaned_cfg = [[], []]
    for statement in cfg:
        temp = statement.split("->")
        cleaned_cfg[0].append(temp[0])
        cleaned_cfg[1].append(temp[1])
    
    cfg_objs = []
    for i in range(len(cfg)):
        cfg_objs.append(CFG(cleaned_cfg[0][i], cleaned_cfg[1][i]))
    
    find_first(cleaned_cfg[0], cfg_objs, 0)
    find_follow(cleaned_cfg[0], cfg_objs)
    
    print("FIRST:-")
    for i in cfg_objs:
        print(i.non_terminal, "->", i.first)
    
    print("")
    
    print("FOLLOW:-")
    for i in cfg_objs:
        print(i.non_terminal, "->", i.follow)

def find_first(nt_list, cfg_objs, nt_index):
    """
    nt_list is list of all non terminals in CFG
    cfg_objects is list of CFG objects
    nt_index index of non terminal
    """
    if len(cfg_objs[nt_index].first) != 0:
        return cfg_objs[nt_index].first.copy()
    
    for i in cfg_objs[nt_index].instances:
        for character in i:
            if character in nt_list:
                null_exists = False
                index = find_index(character, cfg_objs)
                le_first = find_first(nt_list, cfg_objs, index)
                if '#' in le_first and i.index(character) != len(i) - 1:
                    null_exists = True
                    le_first.remove('#')
                cfg_objs[nt_index].first = cfg_objs[nt_index].first.union(le_first)
                if null_exists:
                    continue
                else:
                    break
            elif character == '#': # null
                if i.index(character) == len(i) - 1:
                    cfg_objs[nt_index].first.add(character)
                else:
                    continue
            else:
                cfg_objs[nt_index].first.add(character)
                break
    
    return cfg_objs[nt_index].first.copy()

def find_follow(nt_list, cfg_objs):
    for i in cfg_objs:
        nt = i.non_terminal
        for j in cfg_objs:
            for k in j.instances:
                found = False
                x = 0
                while x < len(k):
                    if k[x] == nt or  found == True:
                        # if this character is last one
                        if x == len(k) - 1:
                            found = False
                            i.follow = i.follow.union(j.follow)
                            break
                        # if next is a non terminal
                        elif k[x+1] in nt_list:
                            index = find_index(k[x+1], cfg_objs)
                            ffirst = find_first(nt_list, cfg_objs, index)
                            if len(ffirst) == 1 and ffirst == '#':
                                found = True
                            else:
                                if '#' in ffirst:
                                    ffirst.remove('#')
                                    found = True
                                i.follow = i.follow.union(ffirst)
                                if found == False:
                                    break
                        # if the next character is null
                        elif k[x+1] == '#':
                            found = True
                        else:
                            i.follow.add(k[x+1])
                            found = False
                            break
                    
                    x = x + 1


def find_index(character, obj_list):
    index = -1
    i = 0
    while i < len(obj_list):
        if obj_list[i].non_terminal == character:
            index = i
            break
        i = i + 1
    return index

# read text file containg CFG
def read_CFG(file_name):
    cfg = [] # array containing CFG
    
    with open(file_name, 'r') as file:
        cfg = file.read().splitlines()
    
    return cfg

if __name__ == "__main__":
    main()