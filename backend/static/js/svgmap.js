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

            const currentTooltipRectHeight = tooltip.getBoundingClientRect().height;
            const maxTooltipRectHeight = 240; // It could be dynamic too, but hardcoding makes better UX.
            const cursorPadding = 10;

            const cursorX = svgRect.left + event.clientX + window.scrollX;
            const cursorY = svgRect.top + event.clientY + window.scrollY;

            const isTooltipFitsBelowCursor = cursorY + maxTooltipRectHeight + cursorPadding < window.scrollY + window.innerHeight;

            if (isTooltipFitsBelowCursor) {
                tooltip.style.top = cursorY + cursorPadding + 'px';
            } else {
                tooltip.style.top = cursorY - currentTooltipRectHeight - cursorPadding + 'px';
            }
            tooltip.style.left = svgRect.left + event.clientX + window.scrollX + cursorPadding + 'px';
        });

        pathElement.addEventListener('mouseout', () => {
            tooltip.style.visibility = 'hidden';
        });
    }

}