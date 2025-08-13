function normalizePartyName(name) {
    return name.replace(/["'״׳\-\s]/g, '');
}

function getPartyColor(party) {
    let color;
    party = normalizePartyName(party);
    switch (party) {
        case 'הליכוד':
            color = 'rgba(65, 105, 225, 1)'; // RoyalBlue
            break;
        case 'ישעתיד':
            color = 'rgba(255, 179, 38, 1)'; // Orange
            break;
        case 'המחנההממלכתי':
            color = 'rgba(128, 202, 255, 1)'; // LightBlue
            break;
        case 'כחוללבן':
            color = 'rgba(128, 202, 255, 1)'; // LightBlue
            break;
        case 'עבודה':
            color = 'rgba(106, 13, 173, 1)'; // Purple
            break;
        case 'העבודה':
            color = 'rgba(106, 13, 173, 1)'; // Purple
            break;
        case 'מרצ':
            color = 'rgb(28, 127, 8)'; // Green
            break;
        case 'עוצמהיהודית':
            color = 'rgba(255, 112, 46, 1)'; // OrangeRed
            break;
        case 'הציונותהדתית':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen
            break;
        case 'האיחודהלאומי':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen
            break;
        case 'ימינה':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen
            break;
        case 'הביתהיהודי':
            color = 'rgba(141, 192, 53, 1)'; // YellowGreen
            break;
        case 'תקווהחדשה':
            color = 'rgba(0, 0, 139, 1)'; // DarkBlue
            break;
        case 'שס':
            color = 'rgba(54, 54, 54, 1)'; // DarkGray
            break;
        case 'יהדותהתורה':
            color = 'rgba(26, 64, 130, 1)'; // DarkBlue
            break;
        case 'רעמ':
            color = 'rgba(0, 128, 0, 1)'; // Green
            break;
        case 'חדשתעל':
            color = 'rgba(219, 33, 33, 1)'; // Red
            break;
        case 'ישראלביתנו':
            color = 'rgba(37, 26, 161, 1)'; // DarkBlue
            break;
        case 'נעם':
            color = 'rgba(173, 216, 230, 1)'; // LightBlue
            break;
        case 'כולנו':
            color = 'rgb(72, 139, 161)'; // LightBlue
            break;
        case 'בלד':
            color = 'rgb(179, 57, 0)'; // Brown
            break;
        default:
            color = 'rgba(128, 128, 128, 1)'; // Gray
    }
    return color;
}