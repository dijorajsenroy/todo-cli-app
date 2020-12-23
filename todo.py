import argparse
import datetime
dt = datetime.datetime.now()

def save_todo(item):
    with open('todo.txt', 'a+') as f:
        f.write("%s\n" % item)

def get_todo():
    todo_txt = open('todo.txt', 'r')
    todolist = [line.split('\n')[0] for line in todo_txt.readlines()][::-1]
    return todolist

def get_stats():
    stat_txt = open('statistics.txt', 'r')
    statistics = [int(line.split('\n')[0]) for line in stat_txt.readlines()]
    return statistics

def save_stats(pending, completed):
    statistics = [0, 0]
    statistics[0] = pending
    statistics[1] = completed
    with open('statistics.txt', 'w') as f: f.write("")
    with open('statistics.txt', 'a+') as f:
        for s in statistics:
            f.write("{0}\n".format(s))


parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

parser_add = subparser.add_parser('add')
parser_add.add_argument('todo_item', type = str)

parser_del = subparser.add_parser('del')
parser_del.add_argument('del_item', type=int)

parser_done = subparser.add_parser('done')
parser_done.add_argument('done_item', type=int)

parser_ls= subparser.add_parser('ls')
parser_ls.add_argument('ls_flag', action = "store_const", const= True)

parser_h = subparser.add_parser('help')
parser_h.add_argument('h_flag', action="store_const", const=True)

parser_rep = subparser.add_parser('report')
parser_rep.add_argument('rep_flag', action="store_const", const=True)

p = parser.parse_args()

try:
    todo_item = p.todo_item
except AttributeError:
    todo_item = "null"

try:
    done_item = p.done_item
except AttributeError:
    done_item = -1

try:
    del_item = p.del_item
except AttributeError:
    del_item = -1

try:
    ls_flag = p.ls_flag
except AttributeError:
    ls_flag = False

try:
    h_flag = p.h_flag
except AttributeError:
    h_flag = False

try:
    rep_flag = p.rep_flag
except AttributeError:
    rep_flag = False


if h_flag:
    print("""Usage :-\n
        $ ./todo add \"todo item\"        # Add a new todo\n
        $ ./todo ls                     # Show remaining todos\n
        $ ./todo del NUMBER             # Delete a todo\n
        $ ./todo done NUMBER            # Complete a todo\n
        $ ./todo help                   # Show usage\n
        $ ./todo report                 # Statistics""")

if h_flag==False and ls_flag==False and rep_flag==False and todo_item=="null" and del_item==-1 and done_item==-1:
    print("""Usage :-\n
        $ ./todo add \"todo item\"        # Add a new todo\n
        $ ./todo ls                     # Show remaining todos\n
        $ ./todo del NUMBER             # Delete a todo\n
        $ ./todo done NUMBER            # Complete a todo\n
        $ ./todo help                   # Show usage\n
        $ ./todo report                 # Statistics""")

if todo_item != "null":
    save_todo(todo_item)
    print("Added todo: \"%s\"" % todo_item)
    save_stats(len(get_todo()), 0)


if ls_flag:
    todolist = get_todo()
    n = len(todolist)
    for i, j in enumerate(todolist):
        print("[{0}]".format(n-i), j)

if del_item != -1:
    todolist = get_todo()
    if len(todolist) == 0:
        print("Error: todo  # {0} does not exist. Nothing deleted.".format(del_item))
    else:
        with open('todo.txt', 'w+') as f:
            f.write("")
    
        n = len(todolist)
        for i in todolist[::-1]:
            if i != todolist[n - del_item]:
                save_todo(i)
        print("Deleted todo #",del_item)
        statistics = get_stats()
        save_stats(pending = statistics[0] - 1, completed = statistics[1])


if done_item != -1:
    todolist = get_todo()
    if len(todolist) == 0:
        print("error: todo list empty")
    else:
        with open('todo.txt', 'w+') as f:
            f.write("")
    
        n = len(todolist)
        D = todolist[n - done_item]
        for i in todolist[::-1]:
            if i != D:
                save_todo(i)
        print("Completed todo #", done_item)
        statistics = get_stats()
        save_stats(pending=statistics[0]-1, completed=statistics[1]+1)
        with open('done.txt', 'a+') as f:
            f.write("x {0}-{1}-{2} {3}\n".format(dt.year, dt.month, dt.day, D))


if rep_flag:
    statistics = get_stats()
    print("{0}/{1}/{2}".format(dt.day, dt.month, dt.year), "Pending: ", statistics[0], " Completed: ", statistics[1])
