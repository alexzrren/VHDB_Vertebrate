with open(config['input_table'], 'r') as fd:
        SAMPLE_INDEX = { x[0]:x[1:] for x in list(map(lambda x: x.split(), fd.read().splitlines()))}

from pathlib import Path

SNAKEFILE_DIR = Path(__file__).parent
print(SNAKEFILE_DIR)

rule all:
    input:
        expand(os.path.join(config['outdir'], "2.coverage", "{sample_index}_coverage.txt"), sample_index=SAMPLE_INDEX.keys()),
        expand(os.path.join(config['outdir'], "0.stats", "{sample_index}.seqkit.stats.txt"), sample_index=SAMPLE_INDEX.keys()),
        expand(os.path.join(config['outdir'], "3.summary", "{sample_index}_summary.csv"), sample_index=SAMPLE_INDEX.keys())

rule seqkit_stats:
    input:
        fq1 = lambda wildcards: SAMPLE_INDEX[wildcards.sample_index][0],
        fq2 = lambda wildcards: SAMPLE_INDEX[wildcards.sample_index][1]
    output:
        os.path.join(config['outdir'], "0.stats", "{sample_index}.seqkit.stats.txt")
    threads: 2
    shell:
        """
        seqkit stats -j{threads} -a {input.fq1} {input.fq2} > {output}
        """    

rule bowtie2_mapping:
    input:
        fq1 = lambda wildcards: SAMPLE_INDEX[wildcards.sample_index][0],
        fq2 = lambda wildcards: SAMPLE_INDEX[wildcards.sample_index][1],
    output:
        os.path.join(config['outdir'], "1.sortedbam", "{sample_index}_sorted.bam")
    threads: 4
    log:
        "logs/bowtie2_{sample_index}.log"
    params:
        db = config['index']
    shell:
        """
        bowtie2 -x {params.db} -1 {input.fq1} -2 {input.fq2} --very-sensitive-local -p 4 | samtools view -bS -F 4 | samtools sort -o {output} 2> {log}
        """

rule samtools_coverage:
    input:
        rules.bowtie2_mapping.output
    output:
        os.path.join(config['outdir'], "2.coverage", "{sample_index}_coverage.txt")
    threads: 1
    shell:
        """
        samtools coverage --ff UNMAP,SECONDARY,QCFAIL,DUP -H -q 0 {input} | awk '$6>0' | sed 's/^/{wildcards.sample_index}\\t/g' > {output}
        """
    
rule summarize:
    input:
        coverage = rules.samtools_coverage.output,
        stats = rules.seqkit_stats.output
    output:
        os.path.join(config['outdir'], "3.summary", "{sample_index}_summary.csv")
    params:
        summarize_script = config['summarize_script'],
        readnum_cutoff = config['readnum_cutoff'],
        infotable = config['infotable']
    threads: 1
    shell:
        """
        python {params.summarize_script} {input.coverage} {input.stats} {params.infotable} {output} {params.readnum_cutoff} 
        """