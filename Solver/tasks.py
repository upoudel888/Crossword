from celery import shared_task
from celery_progress.backend import ProgressRecorder

import os
from .Crossword_inf import Crossword
from .BPSolver_inf import BPSolver
from .Strict_json import json_CA_json_converter
from django.conf import settings


MODEL_PATH = os.path.join(settings.BASE_DIR,"Solver","Inference_components","dpr_biencoder_trained_500k.bin")
ANS_TSV_PATH = os.path.join(settings.BASE_DIR,"Solver","Inference_components","all_answer_list.tsv")
DENSE_EMBD_PATH = os.path.join(settings.BASE_DIR,"Solver","Inference_components","embeddings_all_answers_json_0*")

@shared_task(bind=True)
def solvePuzzle69(self,puzzle):
    puzzle = json_CA_json_converter(puzzle, False)
    crossword = Crossword(puzzle)
    solver = BPSolver(crossword, model_path = MODEL_PATH, ans_tsv_path = ANS_TSV_PATH, dense_embd_path = DENSE_EMBD_PATH, max_candidates = 10000)
    solution = solver.solve(num_iters = 100, iterative_improvement_steps = 0)
    return solution, solver.evaluate(solution)
    



@shared_task(bind=True)
def go_to_sleep(self, duration):
    progress_recorder = ProgressRecorder(self)
    for i in range(100):
        sleep(duration)
        progress_recorder.set_progress(i + 1, 100, f'On iteration {i}')
    return 'Done'