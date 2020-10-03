function sleep(s) {
    // usage: await sleep(2)
    ms = s * 1000
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function updateStatusPeriodically() {
    if (window.location.pathname != '/lobby' && window.location.pathname != '/game') {
        return
    }
    while (true) {
        statusUpdates()
        await sleep(20)
    }
}
updateStatusPeriodically()


function statusUpdates() {
    $(function() {
        $.ajax({
            type: "GET",
            url: '/status',
            success: function(data)
            {
                console.log(data)
                gameStarted = data['game_started']
                roomUsers = data['room_users']
                adminUser = data['admin_user']
                userId = data['user_id']

                startEndGame(gameStarted)
                fillUsernames(roomUsers)
                enableDisableAdminOptions(adminUser, userId)
            }
        });
    })
}


function startEndGame(gameStarted) {
    if (window.location.pathname == '/game' && !gameStarted) {
        window.location.href = '/lobby'
        return 1
    }
    if (window.location.pathname == '/lobby' && gameStarted) {
        window.location.href = '/game'
        return 1
    }
}


function fillUsernames(users) {
    usersHtml = ''
    for (var i=0; i<users.length; i++) {
        usersHtml += `<p>${users[i]}</p>`
    }
    $('#players').html(usersHtml)
}


function enableDisableAdminOptions(adminUser, userId) {
    if (window.location.pathname == '/lobby' && adminUser == userId) {
        $('#start-game').css('display', '')
        return 1
    }
    if (window.location.pathname == '/lobby' && adminUser != userId) {
        $('#start-game').css('display', 'none')
        return 1
    }
    if (window.location.pathname == '/game' && adminUser == userId) {
        $('#end-game').css('display', '')
        return 1
    }
    if (window.location.pathname == '/game' && adminUser != userId) {
        $('#end-game').css('display', 'none')
        return 1
    }
}
