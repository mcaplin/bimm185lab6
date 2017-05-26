import MySQLdb
from scipy.stats import gaussian_kde
import numpy
import matplotlib.pyplot as plt

operon_set = open('OperonSet.txt', 'r')
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

def sql(statement):
    cur = db.cursor()
    cur.execute(statement)
    result = cur.fetchall()
    if result == None:
        print 'none'
    cur.close()
    return result

def sql2(statement1, statement2):
    cur = db.cursor()
    cur.execute(statement1)
    cur.execute(statement2)
    result = cur.fetchall()
    if result == None:
        print 'none'
    cur.close()
    return result


asdf = 0

gp = {}
intergenic_distances = []
h1 = []
h0 = []
border_distances = []
borders = []
op_borders = []
operons = {}
prev = 0
op = 1

def border(prev, curr):
    #print str(prev) + " " + str(curr)
    if prev == 0:
        return
    if prev[3] == curr[3]:
        ##print str(prev) + " " + str(curr)
        border_distances.append(curr[1] - prev[2] + 1)

for line in gene_product_set: # get b numbers 
    if line[0] == '#':
        continue
    line = line.strip('\n').split('\t')
    if len(line) != 10:
        continue
    gp[line[1]] = line[2]

for line in operon_set:
    if line[0] == '#': # skip header
        continue

    row = line.strip('\n').split('\t')
    if len(row) != 8: 
        continue
    if row[7] == 'Weak': # only get strong or confirmed
        continue
    asdf += 1
    #if asdf == 200:
        #break
    genes = row[5].split(',') # separate genes
    strand = row[3] # get strand
    operon = row[0]
    b_nums = []
    for gene in genes:
        if '<' in gene:
            continue
        b_num = query('locus_tag', 'genes', 'name', gene) # get b number for each gene
        if b_num is None:
            b_num = gp[gene]
            #if len(b_num) < 1:
                #continue
        if b_num is None:
            b_num = query('locus_tag', 'genes', 'synonym', gene)
        if len(b_num) == 0:
            #print 'bnum 0'
            continue
        b_nums.append(b_num[0])
    #if len(genes) > 0: operons.append(genes)

    if len(b_nums) == 1:
        position = sql('SELECT g.gene_id,e.left_pos,e.right_pos,g.strand FROM genes g JOIN exons e USING(gene_id) WHERE g.locus_tag in (\'%s\') ORDER BY e.left_pos asc' % str(b_nums[0]))
        #print len(position)
        if len(position) == 0:
            continue
        #print exons[0]
        #e = []
        for exon in position:
            operons[exon[0]] = op
        op+=1
            #e.append(exon)
        #if len(exons) == 1
            #operons[exons[0][0]] = op
            #op+=1
        #if len(exons > 1):
            #exons[0][2] = exons[len(exons-1)][2]
            #operons[exons[0][0]]
        ##op_borders.append(operon,q[0])
        #border(prev, q[0])
        #prev = q[0]

    if len(b_nums) > 1:
        s = ''
        for b in b_nums:
            s += '\'' + str(b) + '\','
        s = s[:-1]
        positions = sql('SELECT g.gene_id,e.left_pos,e.right_pos,g.strand FROM genes g JOIN exons e USING(gene_id) WHERE g.locus_tag in (%s) ORDER BY e.left_pos asc' % s)
        if len(positions) == 0:
            continue
        #e = []
        for exon in positions:
            #e.append(exon)
            operons[exon[0]]=op
        op+=1
        #if len(positions) > 1:
        #print positions
        #print b_nums
        #border(prev, positions[0])
        #prev = positions[len(positions)-1]
        ##op_borders.append(operon,line[positions[0]])
        ##op_borders.append(operon,positions[len(positions)-1])
        for i in range(0,len(positions)-1):
            #op[positions[i]]
            h1.append(positions[i+1][1] - positions[i][2] + 1)
    
#print asdf
#print intergenic_distances
#q = sql('SELECT g.gene_id,e.left_pos,e.right_pos,g.strand FROM genes g JOIN exons e USING(gene_id)  WHERE g.genome_id=1 ORDER BY e.left_pos ASC;')
idx = sql2('SET @a:=0;', 'SELECT @a:=@a+1 as idx, g.gene_id,e.left_pos,e.right_pos,g.strand  FROM genes g JOIN exons e USING(gene_id)  WHERE g.genome_id=1 ORDER BY e.left_pos ASC;')
#for i in range(0, len(q)-1):
    #if q[i][ in op_borders:
        #if gene[0]
#####print operons 
#print 'ok'
#print idx[0][1]
#print operons[0]
#prevIdx = None
prevOp = None
for i in range(1, len(idx)):
    #print i
    if idx[i][1] in operons:
        if prevOp is not 'asdfasdf':
            o = operons[idx[i][1]]
            #print "ops: " + str(prevOp) + " " + str(o)
            #print "dir: " + str(idx[i-1][4]) + " " + str(idx[i][4])
                #if not in same operon and in same directon
            if prevOp != o and idx[i-1][4] == idx[i][4]: 
                #print "good" + '\n'
                h0.append(idx[i][2]-idx[i-1][3])
            prevOp = o
    #else:
        #print idx[i][1]
print h1
print h0

kde = gaussian_kde(h1)

