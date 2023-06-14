#!/usr/bin/env Rscript
library(biomformat)
library(FEAST)

args <- commandArgs(trailingOnly=T)

tbl_file <- args[1]
md_file <- args[2]
em_iterations <- as.numeric(args[3])
lambda_vals <- args[4]
output <- args[5]

lambda_vals <- as.numeric(strsplit(lambda_vals, ",")[[1]])

tbl <- biomformat::read_biom(tbl_file)
tbl <- t(as.matrix(biomformat::biom_data(tbl)))

md <- read.table(md_file, sep="\t", header=T, na.strings="")
colnames(md)[colnames(md) == "stensl_id"] = "id"
row.names(md) <- md$SampleID

result <- FEAST::STENSL(
    C=tbl,
    metadata=md,
    EM_iterations=em_iterations,
    COVERAGE=NULL,
    l.range=lambda_vals
)
mix_props <- result$proportions_mat

write.table(mix_props, file=output, sep="\t", row.names=T,
            quote=F, col.names=NA)
