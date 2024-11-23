const tooltip = document.getElementById('tooltip');

class AreaImport {
    static ResultStatus = {
        SUCCESS: 'success',
        DOWNLOADING_ERROR: 'downloading_error',
        PARSING_ERROR: 'parsing_error',
        EMPTY_DATA_ERROR: 'empty_data_error',
    }
    static translationResultStatusPl = {
        success: "Sukces",
        downloading_error: "Błąd pobierania",
        parsing_error: "Błąd przetwarzania",
        empty_data_error: "Brak danych"
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
                    hc_has_expected_tags,
                    hc_expected_tags,
                    hc_result_tags
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
        this.hcHasExpectedtags = hc_has_expected_tags;
        this.hcExpectedTags = hc_expected_tags;
        this.hcResultTags = hc_result_tags;

        if (Object.values(AreaImport.ResultStatus).includes(result_status)) {
            this.resultStatus = result_status;
        } else {
            throw new Error(`Invalid result status: ${result_status}`);
        }
    }

    getResultStatusDisplay() {
        return AreaImport.translationResultStatusPl[this.resultStatus];
    }
}

function tagsObjectToString(tags) {
    if (tags === null) {
        return '<brak danych>';
    }
    return Object.entries(tags).map(([k, v]) => `${k}=${v}`).join(',');
}

const areaImportCache = {};
async function fetchAreaImportData(type) {
    if (type in areaImportCache) {
        return areaImportCache[type];
    }
    try {
        const response = await fetch(`/api/v1/area_imports/${type}`);
        const data = await response.json();
        areaImportCache[type] = data.map(areaImportData => new AreaImport(areaImportData));
        return areaImportCache[type];
    } catch (e) {
        console.error(`Failed to fetch ${type} area import objects:`, e);
        return [];
    }
}

const fetchLatestAreaImport = () => fetchAreaImportData('latest');
const fetchStableAreaImport = () => fetchAreaImportData('stable');

function updateSummarySection(areaImportData) {
    let minStartTs = areaImportData[0].startTs;
    let maxEndTs = areaImportData[0].endTs;
    let successAreaNumber = 0;
    areaImportData.forEach(areaImport => {
        minStartTs = Math.min(minStartTs, areaImport.startTs);
        maxEndTs = Math.max(maxEndTs, areaImport.endTs);
        if (areaImport.resultStatus === AreaImport.ResultStatus.SUCCESS) {
            successAreaNumber++;
        }
    })
    const totalAreaNumber = areaImportData.length;
    const intervals = areaImportData.map(a => [a.startTs, a.endTs]);
    const durationSeconds = sumNonOverlappingDuration(intervals);

    document.getElementById('summary-start-dt').innerText = formatDateToISO(minStartTs);
    document.getElementById('summary-end-dt').innerText = formatDateToISO(maxEndTs);
    document.getElementById('summary-duration').innerText = formatDurationToMinutesHours(durationSeconds);
    document.getElementById('summary-areas-info').innerText = `${successAreaNumber}/${totalAreaNumber} (${successAreaNumber}/~380)`;
}


function getBackgroundColorByStatus(areaImport) {
    switch (areaImport.resultStatus) {
        case AreaImport.ResultStatus.SUCCESS:
            if (areaImport.hcHasExpectedtags) {
                return '#00FF00';
            } else {
                return '#FFD700';
            }
        case AreaImport.ResultStatus.DOWNLOADING_ERROR:
        case AreaImport.ResultStatus.PARSING_ERROR:
            return '#FF0000';
        case AreaImport.ResultStatus.EMPTY_DATA_ERROR:
            return '#89978A';
    }
}


function createTagsTooltipDiv(hcExpectedTags, hcResultTags) {
    const divExpectedVsReceivedTags = document.createElement('div');

    const divTitleTags = document.createElement('div');
    divTitleTags.textContent = 'Oczekiwane, a otrzymane:';

    const divExpectedTags = document.createElement('div');
    divExpectedTags.className = 'tags';
    divExpectedTags.textContent = tagsObjectToString(hcExpectedTags);

    const divResultTags = document.createElement('div');
    divResultTags.className = 'tags';
    divResultTags.textContent = tagsObjectToString(hcResultTags);

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

    if (areaImport.resultStatus === AreaImport.ResultStatus.SUCCESS) {
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

        if (!areaImport.hcHasExpectedtags) {
            ulElement.appendChild(document.createElement('hr'));
            ulElement.appendChild(createTagsTooltipDiv(areaImport.hcExpectedTags, areaImport.hcResultTags));
        }
    }
    tooltipContentDiv.appendChild(ulElement);

    return tooltipContentDiv;
}


function updateSvgMap(svgElement, latestAreaImport) {
    const svgAreaMap = new SvgAreaMap(svgElement.contentDocument);

    latestAreaImport.forEach(areaImport => {
        const countyPathElement = svgAreaMap.getPathElementById(areaImport.teryt);
        if (countyPathElement == null) {  // It may happen for areas inside a counties
            return;
        }
        svgAreaMap.fillAreaBackground(countyPathElement, getBackgroundColorByStatus(areaImport));
        svgAreaMap.addTooltipToArea(countyPathElement, createTooltipHTMLContent(areaImport));
    });
}

async function updateReport() {
    const reportType = document.getElementById('report-type').value;
    let areaImportData;
    if (reportType === 'latest') {
        areaImportData = await fetchLatestAreaImport();
    } else if (reportType === 'stable') {
        areaImportData = await fetchStableAreaImport();
    }
    updateSummarySection(areaImportData);
    updateSvgMap(document.getElementById('counties-svg'), areaImportData);
}

document.getElementById('report-type').addEventListener('change', updateReport);
document.getElementById('counties-svg').addEventListener('load', async function () {
    await updateReport();
});