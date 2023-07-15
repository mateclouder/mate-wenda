// ==UserScript==
// @name         画图
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  调用sd api画图
// @author       You
// @match        http://127.0.0.1:17860/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=0.1
// @grant        none
// ==/UserScript==


func.push({
    name: "中文绘图",
    question: async () => {
        lsdh(false)
        zsk(false)

        add_conversation("user", app.question)
        Q = await send("使用英语简要描述以下场景：" + app.question, app.question, false)
        app.loading = true
        alert("提示词：" + Q)
        response = await fetch("/api/sd_agent", {
            // signal: signal,
            method: 'post',
            body: JSON.stringify({
                prompt: `((masterpiece, best quality)), photorealistic,` + Q,
                steps: 20,
                // "enable_hr": false,
                // "hr_scale": 1,
                // "hr_upscaler": "ESRGAN_4x",
                // "hr_second_pass_steps": 15,
                // "denoising_strength": 0.6,
                "sampler_name": "DPM++ SDE Karras",
                negative_prompt: `paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans`
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        try {
            let json = await response.json()
            add_conversation("AI", '![](data:image/png;base64,' + json.images[0] + ")", no_history = true)
        } catch (error) {
            alert("连接SD API失败，请确认已开启agents库，并将SD API地址设置为127.0.0.1:786")
        }
        app.loading = false
        save_history()
    },
})
func.push({
    name: "draw use SD",
    question: async () => {
        lsdh(false)
        zsk(false)

        add_conversation("user", app.question)
        Q = app.question
        app.loading = true
        response = await fetch("/api/sd_agent", {
            // signal: signal,
            method: 'post',
            body: JSON.stringify({
                prompt: `best quality, hyper realism, (ultra high resolution), masterpiece, 8K, RAW Photo, ` + Q,
                steps: 20,
                // sampler_name: "DPM++ SDE Karras",
                negative_prompt: `paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans`
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        try {
            let json = await response.json()
            add_conversation("AI", '![](data:image/png;base64,' + json.images[0] + ")")
        } catch (error) {
            alert("连接SD API失败，请确认已开启agents库，并将SD API地址设置为127.0.0.1:786")
        }
        app.loading = false
        save_history()
    },
})