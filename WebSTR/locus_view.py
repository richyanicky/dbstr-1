from dbutils import *
import pyfaidx

seqbuf = 120
seqbreakline = 100
    
def GetSTRSeqHTML(lflank, strseq, rflank, charbreak=50):
    ret = '<font size="3" color="black">...'
    numchar = 0
    for i in range(len(lflank)):
        ret += lflank[i]
        numchar += 1
        if numchar%seqbreakline == 0: ret += "<br>"
    ret += "</font>"
    ret += '<font size="4" color="red"><b>'
    for i in range(len(strseq)):
        ret += strseq[i]
        numchar += 1
        if numchar%seqbreakline == 0: ret += "<br>"
    ret += "</font></b>"
    ret += '<font size="3" color="black">'
    for i in range(len(rflank)):
        ret += rflank[i]
        numchar += 1
        if numchar%seqbreakline == 0: ret += "<br>"
    ret += "</font>..."
    return ret

def GetSTRInfo(strid, DbSTRPath, reffa):
    ct = connect_db(DbSTRPath).cursor()
    squery = ("select str.chrom, str.start, str.end from strlocmotif str where str.strid = '{}'").format(strid)
    df = ct.execute(squery).fetchall()
    if len(df) == 0: return None, None, None, None
    chrom = df[0][0]
    start = int(df[0][1])
    end = int(df[0][2])
    lflank = str(reffa[chrom][start-seqbuf:start]).upper()
    strseq = str(reffa[chrom][start:end]).upper()
    rflank = str(reffa[chrom][end:end+seqbuf]).upper()
    seq = GetSTRSeqHTML(lflank,strseq,rflank)
    return chrom, start, end, seq

def GetGTExInfo(strid, DbSTRPath):
    ct = connect_db(DbSTRPath).cursor()
    gquery = ("select estr.gene_id, estr.gene_name, estr.tissue, estr.beta, estr.pval, estr.caviar "
              "from estr_gtex estr where estr.str_id = '{}' order by estr.gene_name, estr.beta").format(strid)
    df = ct.execute(gquery).fetchall()
    return df

def GetMutInfo(strid, DbSTRPath):
    ct = connect_db(DbSTRPath).cursor()
    gquery = ("select mut.est_logmu_ml, mut.est_beta_ml, mut.est_pgeom_ml, mut.up, mut.down, mut.p, mut.zscore_1, mut.zscore_2"
              " from mutrates mut where mut.str_id = '{}'").format(strid)
    df = ct.execute(gquery).fetchall()
    return df

def GetImputationInfo(strid, DbSTRPath):
    ct = connect_db(DbSTRPath).cursor()
    gquery = ("select imp.loo_concordance,imp.loo_r,imp.wgs_eur_concordance,imp.wgs_eur_r,imp.wgs_afr_concordance,imp.wgs_afr_r,"
              " imp.wgs_eas_concordance,imp.wgs_eas_r"
              " from locstat imp where imp.str_id = '{}'").format(strid)
    df = ct.execute(gquery).fetchall()
    return df

#elect * from *allelstat* limit 5;
# str_id|locus1|locus2|allele|freq_het|MAF|KL|r2|pval
def GetImputationAlleleInfo(strid, DbSTRPath):
    ct = connect_db(DbSTRPath).cursor()
    gquery = ("select al.allele, al.r2, al.pval"
              " from allelstat al where al.str_id = '{}'").format(strid)
    df = ct.execute(gquery).fetchall()
    return df
