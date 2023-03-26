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
                            src: "//sdk.51.la/js-sdk-pro.min.js?id=LA51_TRACE_ID&ck=LA51_TRACE_CK",
                        },
                    },
                ]
            };
        },
    };
}

module.exports = umamiAnalyticsTemplate;