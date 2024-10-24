"use strict";

module.exports = {
    tabWidth: 4,
    bracketSpacing: false,
    trailingComma: "all",
    overrides: [
        {
            files: ["tsconfig.json"],
            options: {
                parser: "json5",
                quoteProps: "preserve",
            },
        },
        {
            files: ["*.md"],
            options: {
                embeddedLanguageFormatting: "off",
            },
        },
    ],
    plugins: ["prettier-plugin-tailwindcss"],
};
