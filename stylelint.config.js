"use strict";

module.exports = {
    extends: ["stylelint-config-standard"],
    rules: {
        // Add some exceptions for recommended rules
        "at-rule-no-unknown": [
            true,
            {
                ignoreAtRules: [
                    "tailwind",
                    "extend",
                    "define-mixin",
                    "mixin",
                    "theme",
                ],
            },
        ],
        "font-family-no-missing-generic-family-keyword": [
            true,
            {ignoreFontFamilies: ["FontAwesome"]},
        ],
        "function-no-unknown": [
            true,
            {
                ignoreFunctions: ["theme"],
            },
        ],
        "import-notation": null,

        // Disable recommended rules we don't comply with yet
        "no-descending-specificity": null,

        // Disable standard rules we don't comply with yet
        "comment-empty-line-before": null,
        "declaration-empty-line-before": null,
        "keyframes-name-pattern": null,
        "selector-class-pattern": null,
        "selector-id-pattern": null,

        // Compatibility with older browsers
        "alpha-value-notation": "number",
        "color-function-notation": "modern",
        "hue-degree-notation": "number",

        // Limit language features
        "declaration-property-value-disallowed-list": {
            // thin/medium/thick is under-specified, please use pixels
            "/^(border(-top|-right|-bottom|-left)?|outline)(-width)?$/": [
                /\b(thin|medium|thick)\b/,
            ],
        },
        "function-disallowed-list": [],

        // Zulip CSS should have no dependencies on external resources
        "function-url-no-scheme-relative": true,
        "function-url-scheme-allowed-list": [
            "data", // Allow data URIs
        ],
    },
};
