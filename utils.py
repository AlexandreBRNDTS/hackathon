import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime


def generate_seismic_chart(stream, phase_data):
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(f"Seismic Waveforms and Detected Phases for {stream[0].stats.station}")

    colors = {'Z': 'black', 'N': 'red', 'E': 'green'}
    phase_colors = {'P': 'blue', 'S': 'orange'}

    start_time = stream[0].stats.starttime
    for i, tr in enumerate(stream):
        times = np.arange(tr.stats.npts) / tr.stats.sampling_rate
        axes[i].plot(times, tr.data, color=colors[tr.stats.channel[-1]], label=tr.stats.channel)
        axes[i].set_ylabel("Amplitude")
        axes[i].legend(loc='upper right')

        if i == len(stream) - 1:
            axes[i].set_xlabel("Time (seconds)")

    for phase in phase_data:
        phase_time = UTCDateTime(phase['phase_time'])
        relative_time = phase_time - start_time
        for ax in axes:
            ax.axvline(x=relative_time, color=phase_colors[phase['phase_type']], 
                       linestyle='--', label=f"{phase['phase_type']} Phase")
            ax.text(relative_time, ax.get_ylim()[1], f"{phase['phase_type']}",
                    color=phase_colors[phase['phase_type']], verticalalignment='top')

    handles, labels = axes[0].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), loc='upper right')

    plt.tight_layout()
    return fig