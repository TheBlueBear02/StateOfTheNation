function normalizePartyName(name) {
    return name.replace(/["'״׳]/g, '');
}

function getPartyColor(party) {
    let color;
    party = normalizePartyName(party);
    switch (party) {
        case 'הליכוד':
            color = 'rgba(65, 105, 225, 1)'; // RoyalBlue with 50% opacity
            break;
        case 'יש עתיד':
            color = 'rgba(255, 179, 38, 1)'; // Orange with 50% opacity
            break;
        case 'המחנה הממלכתי':
            color = 'rgba(128, 202, 255, 1)'; // LightBlue with 50% opacity
            break;
        case 'כחול לבן':
            color = 'rgba(128, 202, 255, 1)'; // LightBlue with 50% opacity
            break;
        case 'עבודה':
            color = 'rgba(106, 13, 173, 1)'; // Purple with 50% opacity
            break;
        case 'העבודה':
            color = 'rgba(106, 13, 173, 1)'; // Purple with 50% opacity
            break;
        case 'מרצ':
            color = 'rgb(28, 127, 8)'; // Purple with 50% opacity
            break;
        case 'עוצמה יהודית':
            color = 'rgba(255, 112, 46, 1)'; // OrangeRed with 50% opacity
            break;
        case 'הציונות הדתית':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen with 50% opacity
            break;
        case 'האיחוד הלאומי':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen with 50% opacity
            break;
        case 'ימינה':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen with 50% opacity
            break;
        case 'הבית היהודי':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen with 50% opacity
            break;
        case 'תקווה חדשה':
            color = 'rgba(0, 0, 139, 1)'; // DarkBlue with 50% opacity
            break;
        case 'שס':
            color = 'rgba(54, 54, 54, 1)'; // DarkGray with 50% opacity
            break;
        case 'יהדות התורה':
            color = 'rgba(26, 64, 130, 1)'; // DarkBlue with 50% opacity
            break;
        case 'רעמ':
            color = 'rgba(0, 128, 0, 1)'; // Green with 50% opacity
            break;
        case 'חדש-תעל':
            color = 'rgba(219, 33, 33, 1)'; // Red with 50% opacity
            break;
        case 'ישראל ביתנו':
            color = 'rgba(37, 26, 161, 1)'; // DarkBlue with 50% opacity
            break;
        case 'נעם':
            color = 'rgba(173, 216, 230, 1)'; // LightBlue with 50% opacity
            break;
        case 'כולנו':
            color = 'rgb(72, 139, 161)'; // LightBlue with 50% opacity
            break;
        case 'בלד':
            color = 'rgb(179, 57, 0)'; // Gray with 50% opacity
            break;
        default:
            color = 'rgba(128, 128, 128, 1)'; // Gray with 50% opacity
    }
    return color;
}