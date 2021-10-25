const resultBox = document.getElementById("results");

const renderAlert = ({ message, title, isPwned, sources = null }) => {
    let pnwedSources = sources &&
        sources
            .map(
                (source) => `<span class="badge badge-primary">${source}</span>`
            )
            .join(" ");

    resultBox.innerHTML = `
    <div class="alert alert-${isPwned ? "danger" : "success"}" role="alert">
        <h4 class="alert-heading">${title}</h4>
        <p class="mb-0"}>${message}</p>

        ${isPwned ? `
            ${pnwedSources ? pnwedSources : ""}
            <hr class="mb-0">
            <p class="mb-0">
                <small>The tags indicate the sources of accidents had been captured onto.</small>
            </p>`
            : ""
        }
    </div>`;
};

const informUser = ({ status, data = null }, hash) => {
    if (status == "SUCCESS") {
        let count;
        let sources;

        const filteredEntries = data.filter((item) => item.hash == hash);

        if (filteredEntries.length == 1) {
            sources = filteredEntries[0].sources;
            count = filteredEntries[0].count.toLocaleString();
            renderAlert({
                title: "Oh no — the attackers are already guessing it!",
                message: `Your password has been used <b>${count}</b> times with service(s):`,
                isPwned: true,
                sources,
            });
            return;
        }
    }

    renderAlert({
        title: "Good news — no records found!",
        message:
            "This password wasn't used against Turris routers yet. That is always a good sign, but no guarantee that your password is safe.",
        isPwned: false,
    });
    return;
};

const hashPassword = async (password) => {
    const msgUint8 = new TextEncoder().encode(password);
    const hashBuffer = await crypto.subtle.digest("SHA-1", msgUint8);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
        .map((b) => b.toString(16).padStart(2, "0"))
        .join("")
        .toString();
    const hashSlice = hashHex.slice(0, 6);

    return { hash: hashHex, hashSlice };
};

passwordForm.onsubmit = async (e) => {
    e.preventDefault();

    resultBox.innerHTML = "";

    const enteredPassword = document.getElementById("password");
    const { hash, hashSlice } = await hashPassword(enteredPassword.value);

    try {
        const response = await fetch("/passcheck/apiv1/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                msg_type: "request",
                hash: hashSlice,
            }),
        });
        const data = await response.json();

        informUser(data, hash);
    } catch (error) {
        console.error("Sending hash to server failed: ", error);
    }

    enteredPassword.value = "";
};
