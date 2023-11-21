
import copy
q_name = ["q1", "q2", "q3"]
# n1 = [3]*3
# all_q_proj = []
def rec( q_name:list, q_proj=[], all_q_proj=[] ):

    q_current = q_name[-1]
    # print(q_current, q_proj)

    for proj in ["x","y","z"]:
        # print(len(q_name), "layer", q_current, proj)
        q_proj_next = q_proj +[(q_current,proj)]
        # q_proj += [(q_current,proj)]
        if len(q_name) > 1:
            q_next = q_name[:-1]
            rec( q_next, q_proj_next, all_q_proj )
        else:
            # print( q_proj_next, "deepest" )
            all_q_proj.append(q_proj_next)
            # print(all_q_proj)
        # q_proj.pop()
    return all_q_proj

# for _ in range(2):
#     n1.append(["a" for _ in range(3)])

print(len(rec( q_name )))
# print(tuple(n1) )
# print(n1[1][0])