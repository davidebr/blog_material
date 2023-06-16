"${SCHRODINGER}/utilities/multisim" -JOBNAME desmond_es \
                     -m desmond_es.msj -c desmond_es.cfg ../thermalized_sample.cms \
                     -o desmond_es-out.cms \
                     -mode umbrella \
                     -HOST md_gpu -maxjob 1 -cpu 1 \
                     -lic DESMOND_GPGPU:16
