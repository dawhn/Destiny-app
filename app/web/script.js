async function searchPlayer(event) {
    // Check if the Enter key (keyCode 13) is pressed
    if (event.keyCode === 13) {
        event.preventDefault();
        // Prevent the default form submission behavior (if any)

        // Get the value of the search bar
        const query = document.getElementById('search-bar').value;

        await eel.search_player(query)
        // Perform your search logic here (e.g., redirect to a results page or display results)
        console.log('Search query:', query);

        await loadRaidCards(query);
    }
}


async function loadRaidCards(query) {
    let player= await eel.fetch_player(query)();
    let raids = await eel.fetch_player_raids(query)();

    let player_data = JSON.parse(player);
    localStorage.setItem("player", JSON.stringify(player_data))
    console.log(player_data)
    let raid_data = JSON.parse(raids);
    localStorage.setItem("raids", JSON.stringify(raid_data));
}