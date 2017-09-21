# sudoku-sat-solver

PYTHON=python3 make clean && PYTHON=python3 make && cp pycosat.cpython-36m-darwin.so /anaconda/envs/ml1labs/lib/python3.6/site-packages/

python3 processinput.py && python3 sat-solver.py > run.log && python3 processlog.py

