环境配置

``````
conda create environment.yaml
conda activate mapping_vertvirus
``````

用法

```
usage: run.py [-h] [-c CORES] -i INPUT -o OUTPUT [-d] [-r READNUM]

VHDB Vertebrate Virus Mapper

options:
  -h, --help            show this help message and exit
  -c CORES, --cores CORES
                        Max threads for executing workflow [default: 8] 执行流程最大线程数
  -i INPUT, --input INPUT
                        Input table 输入表格：3列 SampleIndex FASTQ1 FASTQ2
  -o OUTPUT, --output OUTPUT
                        Output path 输出路径
  -d, --dry-run         Dry-run 
  -r READNUM, --readnum READNUM 
                        Minimum readnum threshold [default: 2] 最小报告Reads数目
```

