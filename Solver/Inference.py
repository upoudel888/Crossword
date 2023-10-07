import os
from .Crossword_inf import Crossword
from .BPSolver_inf import BPSolver
from .Strict_json import json_CA_json_converter
from django.conf import settings


MODEL_PATH = os.path.join(settings.BASE_DIR,"Solver","Inference_components","dpr_biencoder_trained_500k.bin")
ANS_TSV_PATH = os.path.join(settings.BASE_DIR,"Solver","Inference_components","all_answer_list.tsv")
DENSE_EMBD_PATH = os.path.join(settings.BASE_DIR,"Solver","Inference_components","embeddings_all_answers_json_0*")

MODEL_PATH_DISTIL = os.path.join(settings.BASE_DIR,"Solver","Inference_components","distilbert_EPOCHs_7_COMPLETE.bin")
ANS_TSV_PATH_DISTIL = os.path.join(settings.BASE_DIR,"Solver","Inference_components","all_answer_list.tsv")
DENSE_EMBD_PATH_DISTIL = os.path.join(settings.BASE_DIR,"Solver","Inference_components","distilbert_7_epochs_embeddings.pkl")

def solvePuzzle(puzzle):
    puzzle = json_CA_json_converter(puzzle, False)
    crossword = Crossword(puzzle)
    solver = BPSolver(crossword, model_path = MODEL_PATH_DISTIL, ans_tsv_path = ANS_TSV_PATH_DISTIL, dense_embd_path = DENSE_EMBD_PATH_DISTIL, max_candidates = 40000, model_type = 'distilbert')
    solution = solver.solve(num_iters = 100, iterative_improvement_steps = 0)
    return solution, solver.evaluate(solution)
    