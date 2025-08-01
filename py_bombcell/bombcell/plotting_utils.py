import numpy as np
from collections import namedtuple

# Define MATLAB-style color matrices
red_colors = np.array([
    [0.8627, 0.0784, 0.2353],  # Crimson
    [1.0000, 0.1412, 0.0000],  # Scarlet
    [0.7255, 0.0000, 0.0000],  # Cherry
    [0.5020, 0.0000, 0.1255],  # Burgundy
    [0.5020, 0.0000, 0.0000],  # Maroon
    [0.8039, 0.3608, 0.3608],  # Indian Red
])

blue_colors = np.array([
    [0.2549, 0.4118, 0.8824],  # Royal Blue
    [0.0000, 0.0000, 0.5020],  # Navy Blue
])

darker_yellow_orange_colors = np.array([
    [0.7843, 0.7843, 0.0000],  # Dark Yellow
    [0.8235, 0.6863, 0.0000],  # Dark Golden Yellow
    [0.8235, 0.5294, 0.0000],  # Dark Orange
    [0.8039, 0.4118, 0.3647],  # Dark Coral
    [0.8235, 0.3176, 0.2275],  # Dark Tangerine
    [0.8235, 0.6157, 0.6510],  # Dark Salmon
    [0.7882, 0.7137, 0.5765],  # Dark Goldenrod
    [0.8235, 0.5137, 0.3922],  # Dark Light Coral
    [0.7569, 0.6196, 0.0000],  # Darker Goldenrod
    [0.8235, 0.4510, 0.0000],  # Darker Orange
])

COLOR_MATRIX = np.vstack([red_colors, blue_colors, darker_yellow_orange_colors])

def get_color_from_matrix(idx: int):
    """
    Returns a color from a predefined color matrix based on the given index.

    The function cycles through the COLOR_MATRIX using modulo indexing, ensuring 
    a valid color is always returned regardless of the input index.

    Parameters
    ----------
    idx : int
        The index used to select a color from the color matrix.

    Returns
    -------
    np.ndarray
        A NumPy array representing the RGB color corresponding to the given index.
    """
    return COLOR_MATRIX[idx % len(COLOR_MATRIX)]

def get_metric_info_list(param, quality_metrics):
    """
    Constructs a list of metric information objects for spike sorting quality metrics.

    Each entry in the returned list is a namedtuple containing:
    - the metric's full name,
    - a human-readable short name,
    - one or two threshold values used for visualization or filtering,
    - a condition that determines whether the metric should be plotted,
    - and a predefined line color array for use in plots.

    The list of metrics is hard-coded and includes waveform, amplitude, noise, 
    and clustering quality measures. Plot conditions are dynamically determined
    based on `param` flags and availability of data in `quality_metrics`.

    Parameters
    ----------
    param : dict
        Dictionary containing configuration parameters and thresholds
        used to determine which metrics to compute and display.

    quality_metrics : dict
        Dictionary of extracted quality metric values for all units.
        May include NaNs for metrics that are not computed.

    Returns
    -------
    list of namedtuple
        Each namedtuple (MetricInfo) contains:
        - name (str): full metric name,
        - short_name (str): label for plotting
        - threshold_1 (float or None): lower or upper threshold,
        - threshold_2 (float or None): secondary threshold if applicable,
        - plot_condition (bool): flag to determine if the metric should be plotted,
        - line_colors (np.ndarray): RBA(A) line color vectors for visualization.

    """
    # Define line colors for thresholds (MATLAB style)
    metric_line_cols = np.array([
        [0.2, 0.2, 0.2, 1, 0, 0, 0, 0, 0],  # nPeaks
        [0.2, 0.2, 0.2, 1, 0, 0, 0, 0, 0],  # nTroughs
        [0.2, 0.2, 0.2, 1, 0, 0, 1, 0, 0],  # baseline flatness
        [1, 0, 0, 0.2, 0.2, 0.2, 1, 0, 0],  # waveform duration
        [0.2, 0.2, 0.2, 1, 0, 0, 1, 0, 0],  # peak2/trough
        [1, 0, 0, 0.2, 0.2, 0.2, 1, 0, 0],  # spatial decay
        [0.2, 0.2, 0.2, 0.25, 0.41, 0.88, 0, 0, 0],  # peak1/peak2
        [0.2, 0.2, 0.2, 0.25, 0.41, 0.88, 0, 0, 0],  # peak_main/trough
        [1.0, 0.5469, 0, 0, 0.5, 0, 0, 0, 0],  # amplitude
        [1.0, 0.5469, 0, 0, 0.5, 0, 0, 0, 0],  # SNR
        [0, 0.5, 0, 1.0, 0.5469, 0, 0, 0, 0],  # frac RPVs
        [1.0, 0.5469, 0, 0, 0.5, 0, 0, 0, 0],  # nSpikes
        [1.0, 0.5469, 0, 0, 0.5, 0, 0, 0, 0],  # presence ratio
        [0, 0.5, 0, 1.0, 0.5469, 0, 0, 0, 0],  # % spikes missing
        [0, 0.5, 0, 1.0, 0.5469, 0, 0, 0, 0],  # max drift
        [1.0, 0.5469, 0, 0, 0.5, 0, 0, 0, 0],  # isolation dist
        [0, 0.5, 0, 1.0, 0.5469, 0, 0, 0, 0],  # L-ratio
    ])

    MetricInfo = namedtuple("MetricInfo", "name, short_name, threshold_1, threshold_2, plot_condition, line_colors")
    return [
        MetricInfo(
            name="nPeaks", 
            short_name="# peaks", 
            threshold_1=param.get('maxNPeaks'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[0]
        ),
        
        MetricInfo(
            name="nTroughs", 
            short_name="# troughs", 
            threshold_1=param.get('maxNTroughs'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[1]
        ),
        
        MetricInfo(
            name="waveformBaselineFlatness", 
            short_name="baseline flatness", 
            threshold_1=param.get('maxWvBaselineFraction'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[2]
        ),
        
        MetricInfo(
            name="waveformDuration_peakTrough", 
            short_name="waveform duration", 
            threshold_1=param.get('minWvDuration'), 
            threshold_2=param.get('maxWvDuration'), 
            plot_condition=True, 
            line_colors=metric_line_cols[3]
        ),
        
        MetricInfo(
            name="scndPeakToTroughRatio", 
            short_name="peak_2/trough", 
            threshold_1=param.get('maxScndPeakToTroughRatio_noise'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[4]
        ),
        
        MetricInfo(
            name="spatialDecaySlope", 
            short_name="spatial decay", 
            threshold_1=param.get('minSpatialDecaySlope') if param.get('spDecayLinFit') else param.get('minSpatialDecaySlopeExp'),
            threshold_2=None if param.get('spDecayLinFit') else param.get('maxSpatialDecaySlopeExp'), 
            plot_condition=param.get("computeSpatialDecay", False), 
            line_colors=metric_line_cols[5]
        ),
        
        MetricInfo(
            name="peak1ToPeak2Ratio", 
            short_name="peak_1/peak_2", 
            threshold_1=param.get('maxPeak1ToPeak2Ratio_nonSomatic'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[6]
        ),
        
        MetricInfo(
            name="mainPeakToTroughRatio", 
            short_name="peak_{main}/trough", 
            threshold_1=param.get('maxMainPeakToTroughRatio_nonSomatic'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[7]
        ),
        
        MetricInfo(
            name="rawAmplitude", 
            short_name="amplitude", 
            threshold_1=param.get('minAmplitude'), 
            threshold_2=None, 
            plot_condition=param.get('extractRaw', False) and 'rawAmplitude' in quality_metrics and np.any(~np.isnan(quality_metrics.get('rawAmplitude', [np.nan]))), 
            line_colors=metric_line_cols[8]
        ),
        
        MetricInfo(
            name="signalToNoiseRatio", 
            short_name="signal/noise (SNR)", 
            threshold_1=None, 
            threshold_2=param.get('minSNR'), 
            plot_condition=param.get('extractRaw', False) and 'signalToNoiseRatio' in quality_metrics and np.any(~np.isnan(quality_metrics.get('signalToNoiseRatio', [np.nan]))), 
            line_colors=metric_line_cols[9]
        ),
        
        MetricInfo(
            name="fractionRPVs_estimatedTauR", 
            short_name="refractory period viol. (RPV)", 
            threshold_1=param.get('maxRPVviolations'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[10]
        ),
        
        MetricInfo(
            name="nSpikes", 
            short_name="# spikes", 
            threshold_1=None, 
            threshold_2=param.get('minNumSpikes'), 
            plot_condition=True,
            line_colors=metric_line_cols[11]
        ),
        
        MetricInfo(
            name="presenceRatio", 
            short_name="presence ratio", 
            threshold_1=None, 
            threshold_2=param.get('minPresenceRatio'), 
            plot_condition=True, 
            line_colors=metric_line_cols[12]
        ),
        
        MetricInfo(
            name="percentageSpikesMissing_gaussian", 
            short_name="% spikes missing", 
            threshold_1=param.get('maxPercSpikesMissing'), 
            threshold_2=None, 
            plot_condition=True, 
            line_colors=metric_line_cols[13]
        ),
        
        MetricInfo(
            name="maxDriftEstimate", 
            short_name="maximum drift", 
            threshold_1=param.get('maxDrift'), 
            threshold_2=None, 
            plot_condition=param.get("computeDrift", False), 
            line_colors=metric_line_cols[14]
        ),
        
        MetricInfo(
            name="isolationDistance", 
            short_name="isolation dist.", 
            threshold_1=param.get('isoDmin'), 
            threshold_2=None, 
            plot_condition=param.get("computeDistanceMetrics", False), 
            line_colors=metric_line_cols[15]
        ),
        
        MetricInfo(
            name="Lratio", 
            short_name="L-ratio", 
            threshold_1=None, 
            threshold_2=param.get('lratioMax'), 
            plot_condition=param.get("computeDistanceMetrics", False), 
            line_colors=metric_line_cols[16]
        ),
    ]