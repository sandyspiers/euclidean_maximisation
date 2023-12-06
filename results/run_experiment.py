import copy
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from multiprocessing import Pool

from data.instance_handler import (
    capacitated_diversity_problem_from_file,
    generalized_diversity_problem_from_file,
    random_capacitated_diversity_problem,
    random_generalized_diversity_problem,
)

from emsca.model import EmsModel

LOG_FILE = "results/results_test.log"
TIME_LIMIT = 0.1

RUN_CDP = False
RUN_GDP = False
RUN_RCDP = True
RUN_RGDP = True

ALL_SOLVERS = EmsModel.ALL_SOLVER_OPTIONS
DC_SOLVERS = [(s, rc) for s in ["repoa", "fcard"] for rc in [True, "rootonly", False]]
OA_SOLVERS = [(s, False) for s in ["repoa", "concave_oa"]]


def record_results(mdl: EmsModel):
    with open(LOG_FILE, "a") as f:
        f.write(
            f"{mdl.name},{mdl._original_timelimit},{mdl.solver},{mdl.add_lp_tangents},"
        )
        f.write(
            f"{mdl.solve_details.time},{mdl.objective_value},{mdl.solve_details.best_bound},"
        )
        f.write(f"{mdl.iterations},{mdl.lp_cut_counter},{mdl.ip_cut_counter}\n")


def standard_solve(solver, lp_tangents, instance):
    mdl = copy.deepcopy(instance)
    mdl.name = instance.name
    mdl.verbose = 0
    mdl.solver = solver
    mdl.add_lp_tangents = lp_tangents
    mdl.name = f"{mdl.name}_{solver}_{lp_tangents}"
    mdl.parameters.timelimit = TIME_LIMIT
    mdl.solve()
    record_results(mdl)


def run_para_tests(solver_setups, generator, parameters):
    pool = Pool()
    for solver, lp_tangents in solver_setups:
        for paras in parameters:
            args = (solver, lp_tangents, generator(*paras))
            pool.apply_async(standard_solve, args)
    pool.close()
    pool.join()


def get_file_names(directory, keyword):
    files = []
    for file in os.listdir(directory):
        if file.__contains__(keyword):
            files.append(f"{directory}/{file}")
    return files


def get_RCDP_parameters():
    parameters = []
    seed = 0
    for num in [1000, 1500, 2000, 2500, 3000]:
        for coords in [2, 10, 20]:
            for capacity_ratio in [0.2, 0.3]:
                for k in range(5):
                    seed += 1
                    parameters.append((num, coords, capacity_ratio, seed))
    return parameters


def get_RGDP_parameters():
    parameters = []
    seed = 0
    for num in [1000, 1500, 2000, 2500, 3000]:
        for coords in [2, 10, 20]:
            for capacity_ratio in [0.2, 0.3]:
                for cost_ratio in [0.5, 0.6]:
                    for k in range(5):
                        seed += 1
                        parameters.append(
                            (num, coords, capacity_ratio, cost_ratio, seed)
                        )
    return parameters


if __name__ == "__main__":
    # CDP tests
    if RUN_CDP:
        run_para_tests(
            ALL_SOLVERS,
            capacitated_diversity_problem_from_file,
            get_file_names("results/data/CDP", "CDP"),
        )

    # GDP tests
    if RUN_GDP:
        run_para_tests(
            ALL_SOLVERS,
            generalized_diversity_problem_from_file,
            get_file_names("results/data/GDP", "GDP"),
        )

    # RCDP tests
    if RUN_RCDP:
        run_para_tests(
            DC, random_capacitated_diversity_problem, get_RCDP_parameters()
        )

    # RGDP tests
    if RUN_RGDP:
        run_para_tests(
            DC, random_generalized_diversity_problem, get_RGDP_parameters()
        )
