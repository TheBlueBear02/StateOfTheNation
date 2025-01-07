function displayTweets(tweets, divId) {
    const chatDiv = document.getElementById(divId);
    chatDiv.innerHTML = ''; // Clear existing tweets

    tweets.forEach(tweet => {
        const tweetHtml = `
            <div id="${tweet.is_coalition ? 'coalition_bubble' : 'oposition_bubble'}">
                <table id="${tweet.is_coalition ? 'coalition_table' : 'oposition_table'}">
                    <tr style="direction: rtl; padding: 0px; margin: 0;">
                        <th style="text-align: ${tweet.is_coalition ? 'right' : 'left'}; width: 100%;">
                            <table style="width: 100%; margin: 0; padding: 0;direction: ${tweet.is_coalition ? 'ltr' : 'rtl'}">
                                <tr>
                                    <th style="width: 20%; padding: 0; margin: 0;">
                                        <div style="text-align: center; box-shadow: 0 .1vw .3vw rgb(0 0 0 / 0.2); border-radius: 25px; display:flex; margin:0px; background-color:#C3FBC2; width:3.5vw;">
                                            <p style="font-size: .9vw; font-weight: 700; margin: auto; padding:0px;">${tweet.topic}</p>
                                        </div>
                                    </th>
                                    <th style="width: 50%; padding: 0; margin: 0; padding-left:.2vh;">
                                        <h3 style="margin: 0; padding: 0; font-size: 1.2vw; font-weight: bold;">${tweet.name}</h3>
                                    </th>
                                </tr>
                            </table>
                            <i style="float: ${tweet.is_coalition ? 'right' : 'left'}; margin:0px; padding:0px; font-size: 1vw; padding-left: .2vh;">${tweet.party}</i>
                        </th>
                        <th style="float: ${tweet.is_coalition ? 'right' : 'left'}; margin:0; padding: 0;">
                            <span class="img_span" style="background-image: url(${tweet.minister_image})"></span>
                        </th>
                    </tr>
                    <tr>
                        <table style="margin: 0; padding: 0;">
                            <p dir="rtl" style="margin-top:.3vw; width: 100%; line-height:120%;font-size:1vw;color: black; padding:0px; margin-right: 10px;">${tweet.text}</p>
                        </table>
                    </tr>
                    ${tweet.image ? `
                    <tr>
                        <span class="tweet_image" style="background-image: url(${tweet.image})"></span>
                    </tr>` : ''}
                    <tr style="float: ${tweet.is_coalition ? 'right' : 'left'};display: block;">
                        <td>
                            <img style="margin-bottom:5px;border-radius:25px; width:100%;" src="" />
                            <p style="margin: auto; color: black;  font-size: .8vw; margin-right:.2vw; padding:0px;">${tweet.time} | ${tweet.date}</p>
                        </td>
                    </tr>
                </table>
            </div>
        `;
        chatDiv.insertAdjacentHTML('beforeend', tweetHtml);
    });
}
