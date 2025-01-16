const formatDateToISO = (timestamp) => {
    const date = new Date(timestamp);
    return date.toISOString().replace('T', ' ').slice(0, 19);
};
const formatDurationToMinutesHours = (durationSeconds) => {
    const hours = Math.floor(durationSeconds / 3600);
    durationSeconds = durationSeconds % 3600;
    const minutes = Math.floor(durationSeconds / 60);

    if (hours > 0) {
        return `${hours}h ${minutes}min`;
    }
    return `${minutes}min`;
}

function sumNonOverlappingDuration(intervals) {
    /**
     * intervals as collection of arrays [startTimestamp, endTimestamp]
     */
    if (intervals.length === 0) return 0;

    intervals.sort((a, b) => a[0] - b[0]);

    let mergedIntervals = [];
    let currentInterval = {...intervals[0]};

    for (let i = 1; i < intervals.length; i++) {
        let interval = intervals[i];

        // Check for overlap
        if (interval[0] <= currentInterval[1]) {
            // Overlapping, so extend the current interval's end time if needed
            currentInterval[1] = Math.max(currentInterval[1], interval[1]);
        } else {
            // No overlap, add the current interval to the merged list and move to the next
            mergedIntervals.push(currentInterval);
            currentInterval = {...interval};
        }
    }
    mergedIntervals.push(currentInterval);

    let totalDurationSeconds = 0;
    for (let interval of mergedIntervals) {
        totalDurationSeconds += (interval[1] - interval[0]) / 1000;
    }

    return totalDurationSeconds;
}

function daysBetweenDates(from, to) {
    /**
     * Simple helper function which gives estimated (ignoring edge-cases) days between dates.
     */
    const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
    return Math.round(Math.abs((from - to) / oneDay));
}