import matplotlib.pyplot as plt

_file_name = "perfect_data"
_file_name_counter = 0


def set_file_name(file_name: str):
    """Define base file name to save snapshots to
    file_name = "figure" will result in figure0, figure1,... when calling snapshot
    """
    global _file_name, _file_name_counter
    _file_name = file_name
    _file_name_counter = 0


def snapshot():
    """Save a snapshot of the current matplotlib figure."""
    global _file_name, _file_name_counter
    file_name = f"{_file_name}{_file_name_counter}.png"
    plt.savefig(file_name, transparent=True, bbox_inches="tight", dpi=300)
    _file_name_counter += 1
