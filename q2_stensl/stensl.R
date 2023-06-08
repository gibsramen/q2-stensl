#!/usr/bin/env Rscript
library(biomformat)
library(FEAST)

args <- commandArgs(trailingOnly=T)

tbl_file <- args[1]
md_file <- args[2]
em_iterations <- as.numeric(args[3])
output <- args[4]

tbl <- biomformat::read_biom(tbl_file)
tbl <- t(as.matrix(biomformat::biom_data(tbl)))

md <- read.table(md_file, sep="\t", header=T, na.strings="")
row.names(md) <- md$SampleID

print(head(md))
print(dim(md))

result <- FEAST::STENSL(
    C=tbl,
    metadata=md,
    EM_iterations=em_iterations,
    COVERAGE=NULL,
    l.range=c(0.01)
)
mix_props <- result$proportions_mat

write.table(mix_props, file=output, sep="\t", row.names=T,
            quote=F, col.names=NA)
