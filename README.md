# DL_Project

## self_ossinstruct execution steps
1. set HF_HOME env var (where HF cache will be stored)
2. start an vLLM server with docker
3. set the OPENAI_API_KEY and OPENAI_BASE_URL environment variables
4. execution command `python3 ./star_align/self_ossinstruct.py --seed_data_files=an778/cppHeaderFiles --max_new_data=5 --instruct_mode='S->C' --model=bigcode/starcoderbase-3b --use_vllm_server True`
