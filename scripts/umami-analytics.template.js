async function umamiAnalyticsTemplate(context, options) {
    return {
        name: 'umami-analytics',
        injectHtmlTags({content}) {
            return {
                headTags: [
                    {
                        tagName: 'script',
                        attributes: {
                            async: true,
                            defer: true,
                            'data-website-id': "UMAMI_TRACE_ID",
                            src: "UMAMI_TRACE_URL",
                        },
                    },
                ]
            };
        },
    };
}

module.exports = umamiAnalyticsTemplate;