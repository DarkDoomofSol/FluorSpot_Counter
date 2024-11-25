# FluoroSpot_Counter
 GUI using opencvs simpleblobdetector to detect spots from fluorospot

These are the parameters that can be modified to tune spot detection:

Thresholding Parameters

    minThreshold:
        Minimum intensity value to consider for blob detection.
        Pixels below this threshold are ignored.
    maxThreshold:
        Maximum intensity value to consider for blob detection.
        Pixels above this threshold are ignored.
    thresholdStep:
        Step size for the range [minThreshold, maxThreshold].
        Determines how many thresholds are applied in the multi-level thresholding process.

Blob Size Parameters

    minArea:
        Minimum area (in pixels) for a blob to be detected.
        Filters out blobs smaller than this value.
    maxArea:
        Maximum area (in pixels) for a blob to be detected.
        Filters out blobs larger than this value.

Shape Parameters

    filterByCircularity:
        Enable/disable filtering by the circularity of blobs.
        Set to True to detect blobs based on how circular they are.

    minCircularity:
        Minimum circularity value (0 to 1) for a blob to be considered.
        Perfect circles have a circularity of 1.

    maxCircularity:
        Maximum circularity value (0 to 1) for a blob to be considered.

    filterByInertia:
        Enable/disable filtering by the elongation (or "thinness") of blobs.
        Set to True to detect blobs based on their shape's elongation.

    minInertiaRatio:
        Minimum ratio of the blob's principal axis to the secondary axis (0 to 1).
        Higher values detect more elongated shapes.

    maxInertiaRatio:
        Maximum ratio of the blob's principal axis to the secondary axis (0 to 1).

    filterByConvexity:
        Enable/disable filtering by the convexity of blobs.
        Convexity measures how closely a shape resembles its convex hull.

    minConvexity:
        Minimum convexity value (0 to 1) for a blob to be detected.

    maxConvexity:
        Maximum convexity value (0 to 1) for a blob to be detected.

Blob Placement Parameters

    minDistBetweenBlobs:
        Minimum allowed distance (in pixels) between the centers of detected blobs.
        Prevents detecting multiple blobs too close together.

Blob Stability Parameter

    minRepeatability:
        Minimum number of times a blob must be detected across multiple thresholding steps to be considered valid.
        Helps eliminate blobs that appear inconsistently across thresholds.