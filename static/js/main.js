document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const button = form.querySelector("button");

    const resultDiv = document.createElement("div");
    resultDiv.id = "result";
    form.appendChild(resultDiv);

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        // 🔹 Show loading
        button.disabled = true;
        button.innerText = "Verifying...";
        resultDiv.innerHTML = `
            <div class="loader"></div>
            <p>Analyzing signature...</p>
        `;

        fetch("/verify", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            button.disabled = false;
            button.innerText = "Verify Signature";

            let resultClass = data.prediction === "Genuine Signature"
                ? "success"
                : "fraud";

            resultDiv.innerHTML = `
                <div class="result-card ${resultClass}">
                    <h3>Result</h3>
                    <p><strong>Prediction:</strong> ${data.prediction}</p>
                    <p><strong>Confidence:</strong> ${data.confidence}</p>
                </div>
            `;

            if (data.prediction === "Genuine Signature") {
                launchConfetti();
            }

        })
        .catch(error => {
            button.disabled = false;
            button.innerText = "Verify Signature";

            resultDiv.innerHTML = `
                <div class="result-card fraud">
                    <p>Error verifying signature.</p>
                </div>
            `;
        });
    });

});
function launchConfetti() {
    for (let i = 0; i < 80; i++) {
        const confetti = document.createElement("div");
        confetti.classList.add("confetti");
        confetti.style.left = Math.random() * 100 + "vw";
        confetti.style.animationDuration = (Math.random() * 3 + 2) + "s";
        confetti.style.backgroundColor = 
        "hsl(" + Math.random() * 360 + ", 100%, 50%)";

        document.body.appendChild(confetti);

        setTimeout(() => {
            confetti.remove();
        }, 4000);
    }
}
