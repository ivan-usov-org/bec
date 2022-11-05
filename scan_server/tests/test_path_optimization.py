import numpy as np
import pytest
from scan_server.path_optimization import PathOptimizerMixin
from scan_server.scans import get_fermat_spiral_pos, get_round_roi_scan_positions


def test_shell_optimization():
    optim = PathOptimizerMixin()
    positions_orig = get_fermat_spiral_pos(-5, 5, -5, 5, 0.5)
    step = 2
    drs = np.linspace(step - step / 2, step + step / 2, 100)
    min_length = len(positions_orig)
    for dr in drs:
        optim_positions = optim.optimize_shell(positions_orig, 1, dr)
        assert optim.get_path_length(optim_positions) < optim.get_path_length(positions_orig)
        assert len(positions_orig) == len(optim_positions)
        if min_length > len(optim_positions):
            min_length = len(optim_positions)


@pytest.mark.parametrize(
    "positions_orig",
    [
        (get_fermat_spiral_pos(-5, 5, -5, 5, 0.5)),
        (get_round_roi_scan_positions(10, 10, 1, 3)),
        (get_fermat_spiral_pos(5, 15, -5, 5, 1.5)),
    ],
)
def test_corridor_optimization(positions_orig):
    optim = PathOptimizerMixin()
    optim_positions = optim.optimize_corridor(positions_orig)
    assert optim.get_path_length(optim_positions) < optim.get_path_length(positions_orig)
    assert len(positions_orig) == len(optim_positions)

    # from matplotlib import pyplot as plt

    # plt.figure()
    # plt.plot(positions_orig[:, 0], positions_orig[:, 1], "r-x")
    # plt.plot(optim_positions[:, 0], optim_positions[:, 1], "g-")
    # plt.show()
