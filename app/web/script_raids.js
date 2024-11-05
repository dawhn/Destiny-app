window.onload = function () {
    let raid_data = JSON.parse(localStorage.getItem("raids"));
    for (const raid of raid_data) {
        const card = document.getElementById(raid.name)
        const clears = card.querySelector(".clears")
        const fastest = card.querySelector(".fastest");
        const average = card.querySelector(".average");

        clears.innerHTML = raid.clears;
        fastest.innerHTML = raid.fastest;
        average.innerHTML = raid.avg;
    }

    let player_data = JSON.parse(localStorage.getItem("player"));
    const player_banner = document.getElementById("player_emblem_img");
    const player_logo = document.getElementById("player_logo_img");

    player_banner.src = player_data.banner;
    player_logo.src = player_data.logo;

    const player_clan = document.getElementById("clan_name");
    const player_name = document.getElementById("player_name")

    player_clan.innerHTML = player_data.clan_name + " [" + player_data.clan_tag + "]";
    player_name.innerHTML = player_data.name;

    let seal_data = JSON.parse(player_data.seals);
    for (const seal of seal_data){
        const card = document.getElementById(seal.name);
        const image_seal = card.querySelector(".image_seal");
        console.log(image_seal);
        image_seal.src = "https://bungie.net" + seal.image
        if (seal.completed === "no") {
            image_seal.style.filter = 'brightness(0.3) grayscale(1)'
        }
    }
    console.log(seal_data)
}