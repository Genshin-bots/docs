async function umamiAnalyticsTemplate(context, options) {
    return {
        name: '51la-analytics',
        injectHtmlTags({content}) {
            return {
                headTags: [
                    {
                        tagName: 'script',
                        attributes: {
                            async: true,
                            defer: true,
                            id: "LA_COLLECT",
                            src: "//sdk.51.la/js-sdk-pro.min.js",
                        },
                    },
                    {
                        tagName: 'script',
                        attributes: {
                            async: true,
                            type: 'text/javascript'
                        },
                        innerHTML: "LA.init({id:\"LA51_TRACE_ID\",ck:\"LA51_TRACE_CK\",autoTrack:true,hashMode:true})"
                    },
                ]
            };
        },
    };
}

module.exports = umamiAnalyticsTemplate;