// ==UserScript==
// @name         更换抖音字体
// @namespace    nju.ai.lamda.wangyh
// @version      2025-02-28
// @description  更换抖音字体
// @author       nju.ai.lamda.wangyh
// @match        *://*.douyin.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=douyin.com
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    const styleContent = `
    /* douyin */
    @font-face{font-style:normal;font-family:"PingFang SC";src:local("Aptos Mono")}
    @font-face{font-style:normal;font-family:"DFPKingGothicGB-Regular";src:local("HarmonyOS Sans SC")}
    `

    // 插入样式

    const addStyle = (cssContent) => {
        const styleElement = document.createElement('style');
        styleElement.textContent = cssContent;
        document.head.appendChild(styleElement);
    };

    addStyle(styleContent);
})();

