import re
import MySQLdb

#genes = open('genes.txt', 'r')
#gene_synonyms = open('gene_synonyms.txt', 'r')
operon_set = open('OperonSet.txt', 'r')
#tu_set = open('TUSet.txt', 'r')
gene_product_set = open('GeneProductSet.txt', 'r')
operon_distances = open('1OperonDistances.txt', 'w')
adjacent_operons = open('AdjacentOperons.txt', 'w')


db = MySQLdb.connect(host='bm185s-mysql.ucsd.edu', user='mcaplin',
        passwd='', db='mcaplin_db') 

def query(retrieve, table, column, item):
    cur = db.cursor()
    cur.execute("select %s from %s where %s = \'%s\'" % (retrieve, table, column, item))
    result = cur.fetchone()
    if result != None:
        return result
    cur.close()

forward = []
reverse = []
asdf = 0
for line in operon_set:
#gene_pos = []
    if line[0] == '#':
        continue

    row = line.strip('\n').split('\t')
    if len(row) != 8:
        continue
    if row[7] == 'Weak':
        continue
    asdf += 1
   # if asdf == 10:
      #  break
    names = row[5].split(',')
    strand = row[3]
    gene_pos = []
    for name in names:
        if '<' in name:
            continue
        gene_id = query('gene_id', 'genes', 'name', name)
        if gene_id == None:
            continue
        if gene_id != None:
           # print str(gene_id[0]) 
            q = query('left_pos, right_pos', 'exons', 'gene_id', gene_id[0])
            gene_pos.append(q)
            gene_pos.sort()
    if len(gene_pos) == 0:
        continue
    if len(gene_pos) == 1:
        if strand == 'forward':
            forward.append(gene_pos[0])
            forward.sort()
        else:
            reverse.append(gene_pos[0])
            reverse.sort()
    if len(gene_pos) > 1:
        for i in range(0, len(gene_pos)-1):
            operon_distances.write(str(gene_pos[i+1][0] - gene_pos[i][1]) + '\n')
        if strand == 'forward':
            forward.append(gene_pos[0])
            forward.append(gene_pos[len(gene_pos)-1])
            forward.sort()
            #print forward
            #break
        else:
            reverse.append(gene_pos[0])
            reverse.append(gene_pos[len(gene_pos)-1])
            reverse.sort()
#print forward
for i in range(0, len(forward)-1):
    adjacent_operons.write(str(forward[i+1][0] - forward[i][1])+'\n')
for i in range(0, len(reverse)-1):
    adjacent_operons.write(str(reverse[i+1][0] - reverse[i][1]) + '\n')
    #print gene_pos

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

