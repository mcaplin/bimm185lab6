import re
import MySQLdb

#genes = open('genes.txt', 'r')
#gene_synonyms = open('gene_synonyms.txt', 'r')
operon_set = open('OperonSet.txt', 'r')
tu_set = open('TUSet.txt', 'r')
gene_product_set = open('GeneProductSet.txt', 'r')
operon_distances = open('OperonDistances.txt', 'w')


db = MySQLdb.connect(host='bm185s-mysql.ucsd.edu', user='mcaplin',
        passwd='', db='mcaplin_db') 

def query(retrieve, table, column, item):
    cur = db.cursor()
    cur.execute("select %s from %s where %s = \'%s\'" % (retrieve, table, column, item))
    result = cur.fetchone()
    #if result != None:
    return result
    cur.close()

#gene_names = {}
i = 0
op_pos = []
for line in operon_set:
#gene_pos = []
    if line[0] == '#':
        continue

    row = line.strip('\n').split('\t')
    if len(row) != 8:
        continue
    if row[7] == 'Weak':
        continue
    i += 1
    if i == 20:
        break
    operon = row[5].split(',')
    strand = row[3]
    gene_pos = []
   # print names
    #if '<' in names:
        #continue
    for gene_name in operon:
        if '<' in gene_name:
            i-=1
            continue
        gene_id = query('gene_id', 'genes', 'name', gene_name)
        #if gene_id != None: print gene_id[0]
        if gene_id != None:
            gene_pos.append(query('left_pos, right_pos', 'exons', 'gene_id', gene_id[0]))
            gene_pos.sort()
    if len(gene_pos) < 1:
        continue
    if len(gene_pos) == 1:
        op_pos.append(gene_pos)
        op_pos.sort()
    if(strand == 'forward'):
        print gene_pos
        for i in range(0, len(gene_pos)-1):
            operon_distances.write(str(gene_pos[i+1][0] - gene_pos[i][1]) + '\n')
        op_pos.append(gene_pos[0])
        op_pos.append(gene_pos[len(gene_pos)-1])

    #print gene_pos
    #if len(gene_pos) > 1: print gene_pos[0][1]

#gene_names[name] = 'name': None, 'left': None
    




"""
promoters = []
i = 0
for line in tu_set:
    if i == 5: break
    if line[0] == '': continue
    #l = []
    #print line
    l = line.strip().split('\t')
    print l[6]
    length = len(l)

    if l[length-1] == 'Strong' or l[length-1] == 'Confirmed':
        if l[length-3] == '': continue
        i+=1
        l[length-3].split(', ')
        promoters.append(l[length-3])
    
print promoter
"""

