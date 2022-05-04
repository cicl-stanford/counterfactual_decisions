var height = 290;
var page_starter = '<div style="height:' + height + 'px; text-align: center;">';

var page1 = page_starter +
        '<img src="instructions/agent.png" style="width: 60px;' +
            'margin-top: 10em;"></img> </div>' +
        '<p> In this experiment, you will watch the player above moving' +
        ' around in different grids. </p>';

var page2 = page_starter + 
        '<img src="instructions/instructions_00.png" style="margin-top: 2em;">' +
        ' </img> </div>' +
        "<p> The player's goal is to reach the star in each grid. At the beginning" +
        ' of each round, the player can pick one of two paths to take:' +
        ' the red path (top) or the blue path (bottom). The player can see' +
        ' the whole grid and what each path looks like. </p>';

var page3 = page_starter + 
        '<img src="instructions/instructions_01.png" style="margin-top: 2em;">' +
        ' </img> </div>' +
        '<p> Once the player picks a path, they move to the designated shaded' +
        ' start square for that path. They cannot change paths after they make' +
        ' their choice. </p>' +
        '<p> Here, the player picked the red path. </p>';

var page4 = page_starter + 
        '<img src="instructions/instructions_full.gif" style="margin-top: 2em;">' +
        ' </img> </div>' +
        '<p> On each step, the player can move up, down, left, right, or' +
        ' stay in place. They cannot move through walls. If they' +
        ' reach the star before time runs out, then they win. </p>' +
        ' <p> Above, you can watch the player move and see that they won' +
        ' this time! </p>';

var page5 = page_starter +
        '<div style="width: 40%; margin: 6em 5% auto; float:left;"> <img src=' +
            '"instructions/door_closed.png" style="width: 100%; margin: auto;">' +
            '</img> <br> <br> closed door </div>' +
        '<div style="width: 40%; margin: 6em 5% auto; float:left;"> <img src=' +
            '"instructions/door_open.png" style="width: 100%; margin: auto;">' +
            '</img> <br> <br> open door </div> </div>' +
        '<p> Some of the paths contain doors, which are shown in gray.' +
        ' The player can pass through a door only if it is open' +
        ' (has a gap in the middle). </p>';

var page6 = page_starter +
        '<img src="instructions/instructions2.gif" style="height: 80px;' +
        ' width: auto; margin-top: 6em;"></img> </div>' +
        '<p> Doors can randomly open and close over time. Here, the door was closed' +
        ' at first, but then opened, allowing the player to pass through. </p>';

var page7 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/00.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> Here is an example grid. There is currently one closed' +
        ' door on each path, and the player can see this.' +
        ' The player has 8 timesteps to reach the star (the number of' +
        ' timesteps remaining is shown on the right). </p>';

var page8 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/01.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> The player picks the blue path this time. </p>';

var page9 = page_starter +
        '<h2> Example </h2> <img src="trials/example/02.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> The player takes a step right and now faces a closed' +
        ' door. </p>';

var page10 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/03.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> Both doors are still closed. Since the player cannot' +
        ' pass through, they just stay where they are. </p>';

var page11 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/04.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> The door on the blue path opens. </p>';

var page12 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/05.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> The player takes a step right, through the open door. </p>';

var page13 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/06.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> The player takes another step right. </p>';

var page14 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/07.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> The player takes a step up and reaches the star. </p>';

var page15 = page_starter + 
        '<h2> Example </h2> <img src="trials/example/08.png"' +
        ' style="max-height: 100%; width: auto;"> </img> </div>' +
        '<p> The player wins this time! And there are 2 timesteps remaining. </p>' +
        '<p> On the next page, we will ask you to make a judgment about the' +
        ' result. You will be able to watch a video replay of what happened. </p>';

var instructions_prompt = 'The player won because they took the blue path this time.';

var instruction_pages = [
    page1,
    page2,
    page3,
    page4,
    page5,
    page6,
    page7,
    page8,
    page9,
    page10,
    page11,
    page12,
    page13,
    page14,
    page15
];

for (var i = 0; i < instruction_pages.length; i++) {
    instruction_pages[i] = '<div style="width: 700px; min-width: 300px; margin:' +
        'auto 5em;">' + instruction_pages[i] + '</div>';
}

var instructions_last = '<p> In this experiment, we will show you scenarios' +
        ' like this where the player takes one of the two paths through the' +
        ' grid and either succeeds or fails to reach the star in time.' +
        ' We want to know to what extent you think the player won or lost because' +
        ' of the path they took. </p>';

var start_prompt1 = '<p> Correct! You will now watch the player for 18 rounds. </p>' +
        '<p> On each round, you will first get to walk through a step-by-step play' +
        ' of what happened. You can proceed by either clicking the buttons or' +
        ' pressing arrow keys. Then, you will see a video replay of everything' +
        ' happened while you answer the question, just like in the example. </p>';

var start_prompt2 = '<p> Remember, the player can only take one path each round' +
        ' but they can pick which path each time. They can see the whole' +
        ' grid at the beginning, including which doors are open and closed.' +
        ' They can only pass through a door if it is open (has a gap in the middle)' +
        ' and doors can randomly open or close at any time. </p>' +
        ' <p> Please do not refresh the page. Click the start button whenever' +
        ' you are ready. <p>';

var instruction_images = [
        'instructions/agent.png',
        'instructions/door_closed.png',
        'instructions/door_open.png',
        'instructions/instructions_00.png',
        'instructions/instructions_01.png',
        'instructions/instructions_full.gif',
        'instructions/instructions2.gif',
        'instructions/comprehension.png',
        'trials/example/00.png',
        'trials/example/01.png',
        'trials/example/02.png',
        'trials/example/03.png',
        'trials/example/04.png',
        'trials/example/05.png',
        'trials/example/06.png',
        'trials/example/07.png',
        'trials/example/08.png',
        'trials/example/full.gif'
];
