# dataprov: Automatic provenance metadata generation
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Ffbartusch%2Fdataprov.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Ffbartusch%2Fdataprov?ref=badge_shield)


Dataprov is a wrapper that produces provenance metadata at the same time the data processing happens.

## Install

It's the best to install dataprov in a new conda environment:
[Howto install conda](https://conda.io/miniconda.html)

```
conda create -n dataprov python=3.6
source activate dataprov
```

Install dataprov

```
git clone https://github.com/fbartusch/dataprov.git
cd dataprov
pip install .
```

### Install additonal packages.

You need to enable the [bioconda](https://bioconda.github.io/) channel for the examples in this README:

```
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
```

To try the 'First steps' examples without an the Docker container:

```
conda install bwa
```

To try the 'First steps' examples with the Docker container. This is just the Docker Python-API, you have to install Docker on your system, too.
You can also use Singularity to try the 'First steps' example.

```
pip install docker
```

For the snakemake example workflow:

```
pip install snakemake
pip install docutils

# Install samtools and bcftools
conda install samtools
conda install bcftools
```

To support CWL command line tools and workflows:

```
pip install cwltool==1.0.20180302231433
```


# First steps

A important part of the recorded metadata is **who** computed something.
This information is stored at `~/.dataprov/executor.conf`. If you start dataprov for the first time, the file will be created for you. You hjust have to fill in the information. 

```
$ dataprov
No personal information found at ~/.dataprov/executor.conf
An empy personal information file will be created at ~/.dataprov/executor.conf
Please fill this file with your personal information and try again.
```

## First Computation

The repository contains a very small reference genome. First we compute an index with bwa. 

```
# bwa is installed already
dataprov -i examples/bwa/genome.fa -o examples/bwa/genome.fa.bwt run bwa index examples/bwa/genome.fa

# bwa is not installed already
# Using Docker
docker pull biocontainers/bwa
dataprov -i examples/bwa/genome.fa -o examples/bwa/genome.fa.bwt run docker run -v $PWD/examples/:/tmp/:z -it docker.io/biocontainers/bwa:latest bwa index /tmp/bwa/genome.fa

# Using Singularity
dataprov -i examples/bwa/genome.fa -o examples/bwa/genome.fa.bwt run singularity exec bwa.simg bwa index examples/bwa/genome.fa
```

Everything after the keyword `run` is the command wrapped by dataprov. The `-i/--input` and `-o/--output` options tell dataprov the input/output files of the wrapped command.
You can take a look at the created metadata file at `data/index/genome.bwt.prov`.

```
ls -go examples/bwa/
total 629
-rw-r--r-- 1 234112 Feb 15 15:37 genome.fa
-rw-r--r-- 1   2598 Feb 15 15:40 genome.fa.amb
-rw-r--r-- 1     83 Feb 15 15:40 genome.fa.ann
-rw-r--r-- 1 230320 Feb 15 15:40 genome.fa.bwt
-rw-r--r-- 1   1658 Feb 15 15:40 genome.fa.bwt.prov
-rw-r--r-- 1  57556 Feb 15 15:40 genome.fa.pac
-rw-r--r-- 1 115160 Feb 15 15:40 genome.fa.sa
```

It's an xml-file answering the following questions:

  * **Who** computed the result?
  * **When** was the result computed?
  * **How** was the result computed?
  * **What Input** files were used?
  * **How** were the **input files** computed?
  * On which machine were the computation executed?
  * Was the input/output data changed? 

## Second computation: Inherit metadata

We can also incorporate existing metadata into the metadata of new computations. We map now a small set of reads against the previously computed index.

```
mkdir data/mapped_reads

# bwa installed
dataprov -i examples/bwa/genome.fa.bwt -i examples/bwa/samples/A.fastq -o examples/bwa/mapped_reads/A.bam run 'bwa mem examples/bwa/genome.fa examples/bwa/samples/A.fastq > examples/bwa/mapped_reads/A.bam'

# bwa not installed
# Using Docker
dataprov -i examples/bwa/genome.fa.bwt -i examples/bwa/samples/A.fastq -o examples/bwa/mapped_reads/A.bam \
    run 'docker run -v $PWD/examples/:/tmp/:z  docker.io/biocontainers/bwa:latest bwa mem /tmp/bwa/genome.fa /tmp/bwa/samples/A.fastq > examples/bwa/mapped_reads/A.bam'

# Using Singularity
dataprov -i examples/bwa/genome.fa.bwt -i examples/bwa/samples/A.fastq -o examples/bwa/mapped_reads/A.bam \
    run 'singularity exec bwa.simg bwa mem examples/bwa/genome.fa examples/bwa/samples/A.fastq > examples/bwa/mapped_reads/A.bam'
```

This command produces a mapping result file and the corresponding provenance file:

```
ls -go examples/bwa/mapped_reads/
total 6112
-rw-r--r-- 1 6254845 Feb 15 15:46 A.bam
-rw-r--r-- 1    3253 Feb 15 15:46 A.bam.prov
```

If you look into this file you will see that the history of `A.bam.prov` contains now two operations. The first operation describes how the index from the first step was computed. This operation element was inherited from the metadata file of the specified input. The second operation describes the mapping we just computed.


## Running Snakemake workflows

The directory `examples/snakemake` contains the snakemake tutorial workflow and example data.

```
cd examples/snakemake
dataprov run snakemake all
```

This will run the workflow and creates a provenance file for each of the eight output files:

```
ls -go . calls/ mapped_reads/ sorted_reads/
.:
total 104
drwxrwxr-x. 2    41 Mar 27 16:00 calls
drwxrwxr-x. 2    68 Mar 27 16:00 mapped_reads
-rw-rw-r--. 1 92876 Mar 15 16:11 report.html
-rw-rw-r--. 1 11974 Mar 27 16:00 report.html.prov
drwxrwxr-x. 2   146 Mar 27 16:00 sorted_reads

calls/:
total 80
-rw-rw-r--. 1 66927 Mar 15 16:11 all.vcf
-rw-rw-r--. 1 11977 Mar 27 16:00 all.vcf.prov

mapped_reads/:
total 4436
-rw-rw-r--. 1 2256008 Mar 15 16:11 A.bam
-rw-rw-r--. 1   11980 Mar 27 16:00 A.bam.prov
-rw-rw-r--. 1 2259659 Mar 15 16:11 B.bam
-rw-rw-r--. 1   11980 Mar 27 16:00 B.bam.prov

sorted_reads/:
total 4444
-rw-rw-r--. 1 2242429 Mar 15 16:11 A.bam
-rw-rw-r--. 1     344 Mar 15 16:11 A.bam.bai
-rw-rw-r--. 1   11988 Mar 27 16:00 A.bam.bai.prov
-rw-rw-r--. 1   11980 Mar 27 16:00 A.bam.prov
-rw-rw-r--. 1 2245385 Mar 15 16:11 B.bam
-rw-rw-r--. 1     344 Mar 15 16:11 B.bam.bai
-rw-rw-r--. 1   11988 Mar 27 16:00 B.bam.bai.prov
-rw-rw-r--. 1   11980 Mar 27 16:00 B.bam.prov
```

## Running CWL CommandLineTools

This is one example from the CWL user guide. It just untars a tar archive that contains just one file.

```
cd examples/cwl_command_line
dataprov -i hello.tar -o hello.txt run cwltool tar.cwl tar-job.yml
```

This example used Java installed in a Docker container to create a class file from Java source code.
The example shows that dataprov can infer the name of the resulting class file from the information provided by the .cwl and .yml file.
It could be the case that you have to disable SELinux to run the Docker container (more precise: allow writing in mounted volumes).

```
cd examples/cwl_command_line
dataprov run cwltool arguments.cwl arguments-job.yml
```

# Documentation

## XML Schema

The generated provenance files follow the XML schema provided with this repository. The schema documentation can be found under `xml/schema_doc`.
The documentation was built with `xsltproc` using the [xs3p XSLT stylesheet](https://xml.fiforms.org/xs3p/) and can be viewed in a browser.


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Ffbartusch%2Fdataprov.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Ffbartusch%2Fdataprov?ref=badge_large)