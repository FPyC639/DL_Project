MAX_NEW_DATA=1000000
python ./star_align/self_ossinstruct.py \
 --seed_data_files "an778/cppHeaderFiles/data/" \ 
 --use_vllm_server True \
 --instruct_mode "S->C" \
 --max_new_data $MAX_NEW_DATA \
 --tag concept_gen \
 --temperature 0.7 \
 --seed_code_start_index 0 \
 --model "/project/phan/codellama/StarCoder" \
 --num_fewshots 8 \
 --num_batched_requests 2000 \
 --num_sample_per_request 1