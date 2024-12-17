# eval to activate conda env
srun -p gpu -n 1 --ntasks-per-node=2  --qos=low --account=phan --mem-per-cpu=64G --gres=gpu:1 --time=72:00:00 --pty bash
module load foss/2022b Python/3.10.8
cd /project/phan/jms266
vllm serve /project/phan/codellama/StarCoder --dtype auto