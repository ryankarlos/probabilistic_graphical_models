from networkx.algorithms import tree
from pgmpy.estimators import (
    PC,
    BDeuScore,
    BicScore,
    ExhaustiveSearch,
    HillClimbSearch,
    K2Score,
    MmhcEstimator,
    TreeSearch,
)
from pgmpy.models import BayesianModel

from pgm.model.utils.logging_conf import get_logger

LOG = get_logger()


class StructureLearning:
    def __init__(self, data):
        self.data = data

    def score_based(self, algo="hc", scoring="bic", root_node=None):
        scoring = scoring_functions(self.data, scoring)
        if algo == "es":
            es = ExhaustiveSearch(self.data, scoring_method=scoring)
            model = es.estimate()
        elif algo == "hc":
            hc = HillClimbSearch(self.data)
            model = hc.estimate()
        elif algo == "tree":
            assert root_node is not None
            est = TreeSearch(self.data, root_node=root_node)
            model = est.estimate(estimator_type="chow-liu")

        return model

    def constraint_based(self):
        """
        Estimates a DAG from the given dataset using the
        PC algorithm. The independencies in the dataset are
        identified by doing statistical independence tests.
        Returns
        -------
        model
        """
        c = PC(self.data)
        model = c.estimate()
        return model

    def hybrid(self):
        """
        Uses the MMHC algorithm which combines the constraint-based and
        score-based method.
        It has two parts:
            Learn undirected graph skeleton using the constraint-based
            construction procedure MMPC.
            Orient edges using score-based optimization
            (BDeu score + modified hill-climbing)

        Returns
        -------
        model
        """

        est = MmhcEstimator(self.data)
        return est.estimate()


def scoring_functions(data, scoring_method="k2"):
    """
    Commonly used scores to measure the fit between model and data are
    Bayesian Dirichlet scores such as BDeu or K2 and the Bayesian Information
    Criterion (BIC). BDeu is dependent on an equivalent sample size.
    Returns
    -------

    """
    if scoring_method not in ("k2", "BDeu", "bic"):
        raise ValueError("Scoring method specified must be k2, BDeu or Bic")
    if scoring_method == "BDeu":
        return BDeuScore(data, equivalent_sample_size=5)
    elif scoring_method == "k2":
        return K2Score(data)
    else:
        return BicScore(data)


def true_structure(edge_list):
    """
    Specify list of edges and pass to the Bayesian Model
    constructor to create a DAG based on known/true relationships
    Parameters
    ----------
    edge_list

    Returns
    -------
    DAG
    """
    return BayesianModel(edge_list)


def max_spanning_tree(G, algorithm="kruskal"):
    mst = tree.maximum_spanning_edges(G, algorithm=algorithm, data=False)
    edgelist = list(mst)
    return edgelist
