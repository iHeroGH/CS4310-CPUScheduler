from scheduler import Scheduler
from matplotlib import pyplot as plt

def plot(
            to_plot: list[tuple[int, float, float, float, float]],
            file_name: str
        ) -> None:
    """
    Plots a given list of scheduling algorithm comparison data

    Parameters
    ----------
    to_plot: list[tuple[int, float, float, float, float]]
        A list of tuples containing the number of jobs scheduled, and average
        turnaround times for FCFS, SJF, RR2, and RR5
    file_name: str
        The file name to save the created plot image to. Will be concatenated
        with ".png"
    """
    # Split up to_plot list
    input_size = [i[0] for i in to_plot]
    fcfs_time = [i[1] for i in to_plot]
    sjf_time = [i[2] for i in to_plot]
    rr2_time = [i[3] for i in to_plot]
    rr5_time = [i[4] for i in to_plot]

    # Titles and labels
    plt.title("Scheduling Algorithm Comparison")
    plt.xlabel("Input Size")
    plt.xticks(input_size)
    plt.ylabel("Average Turnaround Time (ms)")

    # Plots for each algorithm
    plt.plot(
        input_size, fcfs_time, color="red",
        label="First-Come-First-Serve"
    )
    plt.plot(
        input_size, sjf_time, color="green",
        label="Shortest-Job-First"
    )
    plt.plot(
        input_size, rr2_time, color="blue",
        label="Round-Robin (w/2ms time-slice)"
    )
    plt.plot(
        input_size, rr5_time, color="gray",
        label="Round-Robin (w/5ms time-slice)"
    )
    plt.legend()

    # Save and display
    plt.savefig(f"{file_name}.png")
    plt.show()

def execute(
            to_plot: list[tuple[int, float, float, float, float]] = []
        ) -> None:
    """
    Drives execution of the comparison of the algorithms.

    Parameters
    ----------
    to_plot: list[tuple[int, float, float, float, float]]
        A list of tuples containing the number of jobs scheduled, and average
        turnaround times for FCFS, SJF, RR2, and RR5. If provided, no
        comparisons will be made. Instead, the input list will be plotted using
        the `plot` function.
    """


    # "Constants" - dimensions actually changes every iteration... but whatever
    FILE_NAME = "comparison/comparison"
    DIMENSIONS = 5
    NUM_TRIALS = 20
    log = True

    # If given a list of items to plot, just plot it. No need to re-compare
    if to_plot:
        plot(to_plot, FILE_NAME)
        return

    # Gameplay loop
    while DIMENSIONS <= 15:
        try:
            print(f"Scheduler with {DIMENSIONS:_} Jobs is being tested!")

            # Call each function NUM_TRIAL times for an average
            fcfs_average: float = 0
            sjf_average: float = 0
            rr2_average: float = 0
            rr5_average: float = 0
            for _ in range(NUM_TRIALS):

                # Create a random scheduler for every dimension and every trial
                scheduler = Scheduler.create_random(DIMENSIONS)

                # FCFS
                fcfs_time = scheduler.order_first_serve().process(log)
                fcfs_average += fcfs_time

                # SJF
                sjf_time = scheduler.order_shortest().process(log)
                sjf_average += sjf_time

                # RR2
                rr2_time = scheduler.order_round_robin(2).process(log)
                rr2_average += rr2_time

                # RR5
                rr5_time = scheduler.order_round_robin(5).process(log)
                rr5_average += rr5_time

        # If something goes wrong, let's plot what we had
        except:
            break

        # Store the plotting data
        to_plot.append(
            (
                DIMENSIONS,
                fcfs_average/NUM_TRIALS,
                sjf_average/NUM_TRIALS,
                rr2_average/NUM_TRIALS,
                rr5_average/NUM_TRIALS
            )
        )
        print(
            to_plot,
            file=open(f"{FILE_NAME}.txt", "w", encoding="utf-8")
        )

        # So many dimensions
        DIMENSIONS += 5

    # Plotting time
    plot(to_plot, FILE_NAME)

if __name__ == "__main__":
    execute(
        [(5, 56.75, 48.21000000000001, 75.75999999999999, 74.85), (10, 110.905, 85.485, 148.465, 147.775), (15, 155.45999999999998, 118.27333333333331, 213.8433333333333, 212.0033333333334)]
    )