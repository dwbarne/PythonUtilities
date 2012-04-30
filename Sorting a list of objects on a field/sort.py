# sorting (ordering) a list of python objects on a field

def sort(list, field):
    res = []
    for x in list:
        i = 0
        for y in res:
            if x[field] <= y[field]: break
            i += 1
        res[i:i] = [x]
    return res
        
if __name__ == '__main__':
    table = [{'name':'john', 'age':25},{'name':'doe', 'age':32}]
    print sort(table, 'name')
    print sort(table, 'age')
    table = [('john', 25), ('doe', 32)]
    print sort(table,0)
    print sort(table,1)