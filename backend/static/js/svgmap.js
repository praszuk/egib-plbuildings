class SvgAreaMap{
    constructor(svgDocument) {
        this.svgDocument = svgDocument;
    }

    getPathElementById(areaId) {
        return this.svgDocument.getElementById(areaId);
    }

    fillAreaBackground(pathElement, color) {
        pathElement.style.fill = color;
    }

    addTooltipToArea(pathElement, tooltipContentDiv) {
        pathElement.addEventListener('mouseover', (_) => {
            tooltip.style.visibility = 'visible';
            tooltip.innerHTML = '';
            tooltip.appendChild(tooltipContentDiv);
        });

        pathElement.addEventListener('mousemove', (event) => {
            const svgRect = this.svgDocument.defaultView.frameElement.getBoundingClientRect();

            tooltip.style.top = svgRect.top + event.clientY + window.scrollY + 10 + 'px';
            tooltip.style.left = svgRect.left + event.clientX + window.scrollX + 10 + 'px';
        });

        pathElement.addEventListener('mouseout', () => {
            tooltip.style.visibility = 'hidden';
        });
    }

}