/**
 * eg. gradient('#FF0000', '#0000FF', 0.5) => '#800080' 
 * https://stackoverflow.com/a/72703778
 * */
function gradient(color1, color2, ratio) {
    // Ensure color2 is "greater" than color1
    if (parseInt(color1.replace('#', ''), 16) > parseInt(color2.replace('#', ''), 16)) {
        [color1, color2] = [color2, color1];
    }

    const from = rgb(color1)
    const to = rgb(color2)

    const r = Math.ceil(from.r * ratio + to.r * (1 - ratio));
    const g = Math.ceil(from.g * ratio + to.g * (1 - ratio));
    const b = Math.ceil(from.b * ratio + to.b * (1 - ratio));

    return '#' + hex(r) + hex(g) + hex(b);
}

/** eg. rgb('#FF0080') => { r: 256, g: 0, b: 128 } */
function rgb(color) {
    const hex = color.replace('#', '')
    return {
        r: parseInt(hex.substring(0, 2), 16),
        g: parseInt(hex.substring(2, 4), 16),
        b: parseInt(hex.substring(4, 6), 16),
    }
}

/** eg. hex(123) => '7b' */
function hex(num) {
    // noinspection JSCheckFunctionSignatures
    num = num.toString(16);
    return (num.length === 1) ? '0' + num : num;
}