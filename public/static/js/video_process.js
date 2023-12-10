const process_btn = document.getElementById("process-btn");
const file_input = document.getElementById("file_input");
const video = document.getElementById('video');
const mp4_viewer = document.getElementById("mp4-viewer");
const spinner = document.getElementById("spinner")
const urlEndPoint = `${location.protocol}//${location.host}/process/`

process_btn.onclick = (event) => {
    event.preventDefault();

    process_btn.textContent = "Processing..."
    process_btn.disabled = true;
    spinner.style.display = "block"

    const formData = new FormData();
    const file = file_input.files[0];

    formData.append("videoFile", file);

    fetch(urlEndPoint, {
        method: "POST",
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        mp4_viewer.src = data['processed_url']
        video.load();
        video.play();
        process_btn.textContent = "Process"
        process_btn.disabled = false;
        spinner.style.display = "none"
        console.log(data)

        const statData = data['stat'];

        // Get the div element where you want to display the stat data
        const statDiv = document.getElementById('stat-data');

        // Create a string representation of the stat data (you can format this as needed)
        let statHtml = '';
        for (const key in statData) {
            statHtml += `
            <tr>
                <td>${key}</td>
                <td>${statData[key]}</td>
            </tr>
        `;
        }

        // Set the inner HTML of the div to the stat data
        statDiv.innerHTML = statHtml;
    })
    .catch((error) => {
        console.log(error);
    });
}