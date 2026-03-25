async function fetchSignals() {
    const res = await fetch("/signals");
    const data = await res.json();

    const container = document.getElementById("signals");
    container.innerHTML = "";

    data.forEach(signal => {
        const div = document.createElement("div");
        div.className = "card";

        div.innerHTML = `
            <h2>${signal.pair}</h2>
            <p class="${signal.signal === 'CALL' ? 'call' : 'put'}">
                ${signal.signal}
            </p>
            <p>Confidence: ${signal.confidence}%</p>
        `;

        container.appendChild(div);
    });
}

// Refresh every 10 seconds
setInterval(fetchSignals, 10000);
fetchSignals();