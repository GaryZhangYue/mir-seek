## read the input
args <- commandArgs(trailingOnly = TRUE)
infilename = args[[1]]
infile = read.csv(infilename, sep = '\t')
#outfilename = paste0('mature-',infilename)
outfilename = args[[2]]
#infile = read.csv('miRNAs_expressed_all_samples_06_10_2022_t_16_14_0718_MiFo_12_1_2020_miRNA.tsv', sep = '\t')

#infile$miRNA = sub('_.*','',infile$miRNA)
infile$miRNA = sub('MIMA.*','',infile$miRNA)
infile.s = infile[,1:2]
infile.s.a = aggregate(.~miRNA,infile.s,mean)

write.table(infile.s.a,outfilename,sep='\t',row.names = F, quote=F)  

