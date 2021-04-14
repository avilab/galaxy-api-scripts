# galaxy-api-scripts

Tired of clicking through Galaxy? Here are some _ad hoc_ scripts to run ARTIC COVID19 Galaxy workflow.

# run_articv3_pe

Runs [ARTICv3 COVID-19 variation workflow](workflows/Galaxy-Workflow-Copy_of_COVID-19__variation_analysis_on_ARTIC_PE_data___collapse_collection_shared_by_user_ulvit.ga). Takes shared data library name as argument. Parses automatically data library subfolders and runs workflow separately on each subfolder.

[ARTICv3 primer bed file](resources/nCoV-2019_v3.bed) and NC_045512 reference genome fasta are imported from separate history (update their ids respectively).

```bash
python scripts/run_articv3_pe.py covid210407 > covid210407.log
```

