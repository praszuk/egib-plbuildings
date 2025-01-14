const tooltip = document.getElementById('tooltip');
const reportVisualizationSelectElem = document.getElementById('report-visualization');
const reportTypeSelectElem = document.getElementById('report-type');

class AreaImport {
    static ResultStatus = {
        SUCCESS: 'success',
        DOWNLOADING_ERROR: 'downloading_error',
        PARSING_ERROR: 'parsing_error',
        EMPTY_DATA_ERROR: 'empty_data_error',
        DATA_CHECK_ERROR: 'data_check_error',
    }
    static translationResultStatusPl = {
        success: 'Sukces',
        downloading_error: 'Błąd pobierania',
        parsing_error: 'Błąd przetwarzania',
        empty_data_error: 'Brak danych',
        data_check_error: 'Błąd sprawdzania danych',
    }

    constructor({
                    id,
                    name,
                    teryt,
                    start_at,
                    end_at,
                    building_count,
                    result_status,
                    has_building_type,
                    has_building_levels,
                    has_building_levels_undg: has_building_levels_underground,
                    data_check_has_expected_tags,
                    data_check_expected_tags,
                    data_check_result_tags
                }) {
        this.id = id;
        this.name = name;
        this.teryt = teryt;
        this.startTs = Date.parse(start_at);
        this.endTs = Date.parse(end_at);
        this.buildingCount = building_count;
        this.hasBuildingType = has_building_type;
        this.hasBuildingLevels = has_building_levels;
        this.hasBuildingLevelsUnderground = has_building_levels_underground;
        this.dcHasExpectedtags = data_check_has_expected_tags;
        this.dcExpectedTags = data_check_expected_tags;
        this.dcResultTags = data_check_result_tags;

        if (Object.values(AreaImport.ResultStatus).includes(result_status)) {
            this.resultStatus = result_status;
        } else {
            throw new Error(`Invalid result status: ${result_status}`);
        }
    }

    isCounty() {
        return this.teryt.length === 4;
    }

    /**
     * @returns {number} score 0-10 (incl.) which describes quality of imported data from the area
     */
    getScore() {
        if (this.buildingCount === 0) {
            return 0;
        }

        let score = 4; // if import data has any building it receives at least 4 points – building=yes
        if (this.hasBuildingType) {
            score += 3;
        }
        if (this.hasBuildingLevels) {
            score += 2;
        }
        if (this.hasBuildingLevelsUnderground) {
            score += 1;
        }
        return score;
    }

    getResultStatusDisplay() {
        return AreaImport.translationResultStatusPl[this.resultStatus];
    }

    static maxScore() {
        return 10;
    }
}

const ReportType = {
    LATEST: 'latest',
    STABLE: 'stable',
}

const VisualizationType = {
    STATUS: 'status',
    LAST_UPDATED_DT: 'last_updated_dt',
    SCORE: 'score',
}

function getVisualizationType() {
    const option = reportVisualizationSelectElem.options[reportVisualizationSelectElem.selectedIndex];
    return VisualizationType[Object.keys(VisualizationType).find(key => VisualizationType[key] === option.value)]
}

function getReportType() {
    const option = reportTypeSelectElem.options[reportTypeSelectElem.selectedIndex];
    return ReportType[Object.keys(ReportType).find(key => ReportType[key] === option.value)]
}

function tagsObjectToString(tags) {
    if (tags === null) {
        return '<brak danych>';
    }
    return Object.entries(tags).map(([k, v]) => `${k}=${v}`).join(',');
}

const areaImportCache = {};

async function getAreaImportData(type) {
    if (type in areaImportCache) {
        return areaImportCache[type];
    }
    try {
        const endpoint = type === ReportType.LATEST ? 'latest' : 'stable';
        const response = await fetch(`/api/v1/area_imports/${endpoint}`);
        const data = await response.json();
        areaImportCache[type] = data.map(areaImportData => new AreaImport(areaImportData));
        return areaImportCache[type];
    } catch (e) {
        console.error(`Failed to fetch ${type} area import objects:`, e);
        return [];
    }
}

function updateSummarySection(areaImportData) {
    let minStartTs = areaImportData[0].startTs;
    let maxEndTs = areaImportData[0].endTs;
    let totalCountiesNumber = 0;
    let successCountiesNumber = 0;
    let totalCommunesNumber = 0;
    let successCommunesNumber = 0;

    areaImportData.forEach(areaImport => {
        minStartTs = Math.min(minStartTs, areaImport.startTs);
        maxEndTs = Math.max(maxEndTs, areaImport.endTs);

        if (areaImport.isCounty()) {
            totalCountiesNumber++;
        } else {
            totalCommunesNumber++;
        }

        if (areaImport.resultStatus === AreaImport.ResultStatus.SUCCESS) {
            if (areaImport.isCounty()) {
                successCountiesNumber++;
            } else {
                successCommunesNumber++;
            }
        }
    })
    const intervals = areaImportData.map(a => [a.startTs, a.endTs]);
    const durationSeconds = sumNonOverlappingDuration(intervals);

    document.getElementById('summary-start-dt').innerText = formatDateToISO(minStartTs);
    document.getElementById('summary-end-dt').innerText = formatDateToISO(maxEndTs);
    document.getElementById('summary-duration').innerText = formatDurationToMinutesHours(durationSeconds);

    document.getElementById('summary-counties-info').innerText = `${successCountiesNumber}/${totalCountiesNumber} (max 380)`;
    document.getElementById('summary-communes-info').innerText = `${successCommunesNumber}/${totalCommunesNumber}`;
}


function getBackgroundColorByStatus(areaImport) {
    switch (areaImport.resultStatus) {
        case AreaImport.ResultStatus.SUCCESS:
            return '#00FF00';
        case AreaImport.ResultStatus.DATA_CHECK_ERROR:
            return '#FFD700';
        case AreaImport.ResultStatus.DOWNLOADING_ERROR:
        case AreaImport.ResultStatus.PARSING_ERROR:
            return '#FF0000';
        case AreaImport.ResultStatus.EMPTY_DATA_ERROR:
            return '#89978A';
    }
}

function getBackgroundColorBy(visualization, areaImportData) {
    if (visualization === VisualizationType.STATUS) {
        return areaImportData.map(function (areaImport) {
            return {area: areaImport, color: getBackgroundColorByStatus(areaImport)}
        })
    } else if (visualization === VisualizationType.LAST_UPDATED_DT) {
        return areaImportData.map(function (areaImport) {
            const days = daysBetweenDates(new Date(areaImport.endTs), new Date());
            let color;
            if (areaImport.resultStatus !== AreaImport.ResultStatus.SUCCESS || days > 28) {
                color = '#FF0000';
            } else if (days > 14) {
                color = '#FFA500';
            } else if (days > 7) {
                color = '#FFD700';
            } else {
                color = '#00FF00';
            }
            return {area: areaImport, color: color}
        })
    } else if (visualization === VisualizationType.SCORE) {
        return areaImportData.map(function (areaImport) {
            const score = areaImport.getScore();
            const color = gradient('#FFFFFF', '#02419f', score / AreaImport.maxScore());
            return {area: areaImport, color: color}
        })
    }
}


function createTagsTooltipDiv(dcExpectedTags, dcResultTags) {
    const divExpectedVsReceivedTags = document.createElement('div');

    const divTitleTags = document.createElement('div');
    divTitleTags.textContent = 'Oczekiwane, a otrzymane:';

    const divExpectedTags = document.createElement('div');
    divExpectedTags.className = 'tags';
    divExpectedTags.textContent = tagsObjectToString(dcExpectedTags);

    const divResultTags = document.createElement('div');
    divResultTags.className = 'tags';
    divResultTags.textContent = tagsObjectToString(dcResultTags);

    divExpectedVsReceivedTags.appendChild(divTitleTags);
    divExpectedVsReceivedTags.appendChild(divExpectedTags);
    divExpectedVsReceivedTags.appendChild(divResultTags);

    return divExpectedVsReceivedTags;
}

function createTooltipHTMLContent(areaImport) {
    const tooltipContentDiv = document.createElement('div');
    tooltipContentDiv.className = 'tooltip-content';

    const spanElement = document.createElement('span');
    spanElement.textContent = `${areaImport.teryt} – ${areaImport.name}`;
    tooltipContentDiv.appendChild(spanElement);
    tooltipContentDiv.appendChild(document.createElement('hr'));

    const ulElement = document.createElement('ul');

    const liStatus = document.createElement('li');
    liStatus.textContent = `Status: ${areaImport.getResultStatusDisplay()}`;

    ulElement.appendChild(liStatus);

    if ([AreaImport.ResultStatus.SUCCESS, AreaImport.ResultStatus.DATA_CHECK_ERROR].includes(areaImport.resultStatus)) {
        const liBuildingCount = document.createElement('li');
        liBuildingCount.textContent = `Liczba budynków: ${areaImport.buildingCount}`;

        const liHasBuildingType = document.createElement('li');
        liHasBuildingType.textContent = `Zawiera typ budynku: ${areaImport.hasBuildingType ? 'Tak' : 'Nie'}`;

        const liHasBuildingLevels = document.createElement('li');
        liHasBuildingLevels.textContent = `Zawiera piętra budynku: ${areaImport.hasBuildingLevels ? 'Tak' : 'Nie'}`;

        const liHasBuildingUndergroundLevels = document.createElement('li');
        liHasBuildingUndergroundLevels.textContent = `Zawiera piętra (podziemne) budynku: ${areaImport.hasBuildingLevelsUnderground ? 'Tak' : 'Nie'}`;

        ulElement.appendChild(liBuildingCount);
        ulElement.appendChild(document.createElement('hr'));
        ulElement.appendChild(liHasBuildingType);
        ulElement.appendChild(liHasBuildingLevels);
        ulElement.appendChild(liHasBuildingUndergroundLevels);

        if (!areaImport.dcHasExpectedtags) {
            ulElement.appendChild(document.createElement('hr'));
            ulElement.appendChild(createTagsTooltipDiv(areaImport.dcExpectedTags, areaImport.dcResultTags));
        }
    }
    tooltipContentDiv.appendChild(ulElement);

    return tooltipContentDiv;
}


function updateSvgMap(svgElement, areaImportDataWithColors) {
    const svgAreaMap = new SvgAreaMap(svgElement.contentDocument);
    areaImportDataWithColors.forEach(areaWithColor => {
        const countyPathElement = svgAreaMap.getPathElementById(areaWithColor.area.teryt);
        if (countyPathElement == null) {  // It may happen for areas inside a counties
            return;
        }
        svgAreaMap.fillAreaBackground(countyPathElement, areaWithColor.color);
        svgAreaMap.addTooltipToArea(countyPathElement, createTooltipHTMLContent(areaWithColor.area));
    });
}

function initReportVisualizationSelectOptions(reportType) {
    while (reportVisualizationSelectElem.options.length > 0) {
        // noinspection JSCheckFunctionSignatures
        reportVisualizationSelectElem.remove(0);
    }

    let options = [
        {
            value: VisualizationType.STATUS,
            label: 'Status',
        },
        {
            value: VisualizationType.SCORE,
            label: 'Ocena',
        },
    ];
    if (reportType === ReportType.STABLE) {
        options = [
            {
                value: VisualizationType.LAST_UPDATED_DT,
                label: 'Czas ostatniej aktualizacji',
            }
        ].concat(options);
    }
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.value;
        optionElement.text = option.label;
        reportVisualizationSelectElem.add(optionElement);
    })
}


function updateReportVisualization(visualizationType, areaImportData) {
    const areaImportDataWithColors = getBackgroundColorBy(visualizationType, areaImportData);
    updateSvgMap(document.getElementById('counties-svg'), areaImportDataWithColors);
}

async function updateReport() {
    const reportType = getReportType();
    initReportVisualizationSelectOptions(reportType);

    const areaImportData = await getAreaImportData(reportType);
    updateSummarySection(areaImportData);
    updateReportVisualization(getVisualizationType(), areaImportData);
}

// Initial SVG resize to fit the page
const svgMap = document.getElementById('counties-svg');
svgMap.style.height = `${window.innerHeight - svgMap.offsetTop}px`;

reportTypeSelectElem.addEventListener('change', updateReport);
reportVisualizationSelectElem.addEventListener('change', async () => {
    const areaImportData = await getAreaImportData(getReportType());
    updateReportVisualization(getVisualizationType(), areaImportData);
});
document.getElementById('counties-svg').addEventListener('load', async function () {
    await updateReport();
});