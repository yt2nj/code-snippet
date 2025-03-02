// ==UserScript==
// @name         arxiv.org -> papers.cool
// @namespace    nju.ai.lamda.wangyh
// @version      2024-11-26
// @description  arxiv.org -> papers.cool
// @author       nju.ai.lamda.wangyh
// @match        https://arxiv.org/pdf/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=arxiv.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 获取当前 URL
    const currentUrl = window.location.href;

    // 定义一个正则表达式来匹配 https://arxiv.org/pdf/{arxivId}
    const regex = /^https?:\/\/arxiv\.org\/pdf\/(\d+\.\d+)/;

    // 使用正则表达式测试当前 URL
    const match = currentUrl.match(regex);

    if (match) {
        // 提取匹配的部分
        const arxivId = match[1];

        // 构造新的 URL
        const newUrl = `https://papers.cool/arxiv/${arxivId}`;

        // 立即重定向到新的 URL
        window.location.href = newUrl;
    } else {
        console.log('Current URL does not match the pattern "https://arxiv.org/pdf/{arxivId}".');
    }

})();
