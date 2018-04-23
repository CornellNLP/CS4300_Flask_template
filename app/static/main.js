google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawCharts);
popup_ids = ["donations", "tweets", "votes"]

function showPopup(show_id) {
  for (id of popup_ids) {
    document.getElementById(id).style.display = "none";
  }
  document.getElementById(show_id).style.display = "block";
}

charts_to_make = [];
function prepChart(id, dem, rep) {
  charts_to_make.push([id, dem, rep]);
}

function drawCharts() {
  console.log(charts_to_make);
  for (l of charts_to_make) {
    console.log("making chart");
    var data = google.visualization.arrayToDataTable([
      ['Party', 'Amount'],
      ['Democrat', l[1]],
      ['Republican', l[2]]
    ]);

    var options = {
      legend: {
        position: 'none'
      },
      chartArea: {left:0,top:0,width:"100%",height:"100%"},
      height: 80,
      width: 80,
      pieSliceText: 'none',
    };

    var chart = new google.visualization.PieChart(document.getElementById(l[0]));

    chart.draw(data, options);
  }
}

politicians = ['Mike Crapo', 'David Scott', 'Rodney Frelinghuysen', 'Jason Lewis', 'Rosa DeLauro', 'Bob Gibbs', 'Mike Kelly', 'Brenda Lawrence', 'Ted Cruz', 'Kirsten Gillibrand', 'Michael Burgess', 'Tom MacArthur', 'Dennis Ross', 'Frank Lucas', 'Andy Biggs', 'Jimmy Panetta', 'Keith Rothfus', 'Pete King', 'Leonard Lance', 'Jackie Speier', 'Jeff Denham', 'Todd Young', 'Tony C\xc3\xa1rdenas', 'Michelle Grisham', 'Mike Quigley', 'Dan Newhouse', 'Tim Kaine', 'Bennie Thompson', 'Sanford Bishop', 'Mike Simpson', 'Dick Durbin', 'Bruce Westerman', 'Lisa Murkowski', 'David Rouzer', 'David Jolly', 'Gary Palmer', 'Alex Mooney', 'Cathy Rodgers', 'Andy Barr', 'Luis Gutierrez', 'Maria Cantwell', 'Pete Visclosky', 'Tammy Baldwin', 'Carolyn Maloney', 'Adrian Smith', 'Randy Neugebauer', 'Ron Kind', 'Yvette Clarke', 'Anna Eshoo', 'Grace Napolitano', 'Ron DeSantis', 'Ra\xc3\xbal Labrador', 'Chris Gibson', 'Gregory Meeks', 'Frank Pallone', 'Ed Markey', 'Rick Allen', 'Sam Johnson', 'Fred Upton', 'Ann Wagner', 'Lois Frankel', 'Alan Grayson', 'John Thune', 'John Katko', 'Kenny Marchant', 'Barbara Mikulski', 'Cory Booker', 'Brad Sherman', 'Tom Graves', 'Don Young', 'Barry Loudermilk', 'Mike Gallagher', 'Jody Hice', 'Cortez Masto', 'Mark Kirk', 'Joni Ernst', 'Joe Crowley', 'Kamala Harris', 'Darin LaHood', 'Bob Corker', 'Candice Miller', 'Claudia Tenney', 'Al Lawson', 'Mike Doyle', 'Rich Nugent', 'Steve Russell', 'Bobby Scott', 'Dianne Feinstein', 'John Lewis', 'Jim Inhofe', 'Ted Poe', 'Kamala Harris', 'Vicente Gonzalez', 'Bill Huizenga', 'Luis Gutierrez', 'James Clyburn', 'Jeff Sessions', 'Mo Brooks', 'Morgan Griffith', 'Paul Cook', 'Brendan Boyle', 'Kathy Castor', 'Stacey Plaskett', 'Stephen Lynch', 'Stephen Fincher', 'Keith Ellison', 'Tom Cotton', 'Reid Ribble', 'John Delaney', 'Mike Rounds', 'Frederica Wilson', 'Scott Taylor', 'Kevin Brady', 'Suzanne Bonamici', 'Garret Graves', 'Julia Brownley', 'Bobby Rush', 'Gerry Connolly', 'Frank LoBiondo', 'Bill Pascrell', 'Ed Perlmutter', 'Bill Keating', 'Paul Tonko', 'Tim Walz', 'John Kennedy', 'Peter Welch', 'Jaime Beutler', 'Emanuel Cleaver', 'Alan Lowenthal', 'Tom Reed', 'Lynn Jenkins', 'Dean Heller', 'Dave Reichert', 'David Perdue', 'James Lankford', 'Scott Tipton', 'Alcee Hastings', 'Ruben Gallego', 'Betty McCollum', 'Brett Guthrie', 'Cynthia Lummis', 'Francis Rooney', 'Kevin McCarthy', 'Heidi Heitkamp', 'Donald Payne', 'Jerry McNerney', 'Nanette Barrag\xc3\xa1n', 'Paul Mitchell', 'Louise Slaughter', 'Dan Sullivan', 'Kelly Ayotte', 'Carol Shea-Porter', 'John McCain', 'Eliot Engel', 'Roy Blunt', 'Jerry Nadler', 'Lindsey Graham', 'Tom Carper', 'Marlin Stutzman', 'Hakeem Jeffries', 'Brian Schatz', 'Chris Coons', 'Dan Coats', 'Bill Johnson', 'Vern Buchanan', "Tom O'Halleran", 'Mark DeSaulnier', 'Drew Ferguson', 'Doris Matsui', 'John Rutherford', 'Richard Burr', 'Michael McCaul', 'Steve Chabot', 'Shelley Moore', 'Donald Norcross', 'Juan Vargas', 'Jeff Merkley', 'Kevin Cramer', 'John Conyers', 'Ted Lieu', 'Aumua Amata', 'Thad Cochran', 'Steve King', 'Scott Perry', 'Tammy Duckworth', 'Sean Duffy', 'Bill Cassidy', 'Brad Wenstrup', 'Dutch Ruppersberger', 'Jared Huffman', 'Martha McSally', 'Patty Murray', 'Rob Portman', 'Jodey Arrington', 'Nancy Pelosi', 'Markwayne Mullin', 'Xavier Becerra', 'Gene Green', 'Bob Brady', 'Walter Jones', 'Steve Scalise', 'Trey Hollingsworth', 'Peter DeFazio', 'Jim McDermott', "Beto O'Rourke", 'Linda S\xc3\xa1nchez', 'Jim Cooper', 'Ander Crenshaw', 'Scott Garrett', 'Hank Johnson', 'Mike Bishop', 'Bruce Poliquin', 'Michael Bennet', 'Charles Rangel', 'Duncan Hunter', 'Janice Hahn', 'Rob Wittman', 'Scott Rigell', 'Tom Rice', 'Sam Graves', 'Peter Roskam', 'Rub\xc3\xa9n Hinojosa', 'Tim Huelskamp', 'Ben Ray', 'David Vitter', 'Joe Barton', 'Lois Capps', 'Cory Gardner', 'Jenniffer Gonz\xc3\xa1lez', 'Virginia Foxx', 'Jim Jordan', 'Lynn Westmoreland', 'Ted Budd', 'Hal Rogers', 'Ruben Kihuen', 'Renee Ellmers', 'Eddie Bernice', 'Glenn Grothman', 'Mario Diaz-Balart', 'Mike Conaway', 'Zoe Lofgren', 'Adam Smith', 'Brian Fitzpatrick', 'Austin Scott', 'John Shimkus', 'Mitch McConnell', 'Jason Smith', 'Elijah Cummings', 'Donald Norcross', 'Johnny Isakson', 'Chris Smith', 'Lloyd Doggett', 'Roger Wicker', 'Chuck Schumer', 'Val Demings', 'Chellie Pingree', 'Xavier Becerra', 'Bob Goodlatte', 'Adriano Espaillat', 'Ro Khanna', 'Dan Donovan', 'Billy Long', 'Mike Thompson', 'Colleen Hanabusa', 'Carlos Curbelo', 'Martin Heinrich', 'Darren Soto', 'Ralph Abraham', 'John Barrasso', 'Don Beyer', 'Kristi Noem', 'Dave Brat', 'Rodney Davis', 'Jeb Hensarling', 'Joe Courtney', 'Larry Bucshon', 'Henry Cuellar', 'Joe Donnelly', 'John Boehner', 'Charlie Dent', 'Tulsi Gabbard', 'David Schweikert', 'Marcia Fudge', 'Tom Udall', 'Tom Cole', 'Donald McEachin', 'Orrin Hatch', 'Bill Foster', 'Marc Veasey', 'Bob Menendez', 'Mazie Hirono', 'Tom Marino', 'Jeff Duncan', 'Lamar Alexander', 'Dan Benishek', 'Filemon Vela', 'Mark Amodei', 'Joe Wilson', 'Chris Collins', 'Rick Larsen', 'David Valadao', 'Ed Whitfield', 'Harry Reid', 'Rick Nolan', 'George Holding', 'Doug Collins', 'Steve Daines', 'Mike Bost', 'Richard Shelby', 'Barbara Boxer', 'Mike Enzi', 'Governor John', 'Jim Renacci', 'Jim Banks', 'Bernie Sanders', 'Gregg Harper', "Glenn 'GT'", 'Jim Costa', 'David Young', 'Trent Kelly', 'Karen Bass', 'Scott Peters', 'Jim Bridenstine', 'Sonya Leighton', 'Joe Kennedy', 'Pat Roberts', 'Rand Paul', 'Sandy Levin', 'Bonnie Watson', 'Marcy Kaptur', 'Ryan Costello', 'Lou Barletta', 'Lloyd Smucker', 'Dave Trott', 'Ben Sasse', 'Claire McCaskill', 'Martha Roby', 'Andy Harris', 'John Duncan', 'Cresent Hardy', 'Jim Risch', 'Joe Manchin', 'Eric Swalwell', 'Chuck Fleischmann', 'Luke Messer', 'Deb Fischer', 'Jeff Fortenberry', 'Jamie Raskin', 'Tom Suozzi', 'Marsha Blackburn', 'Sean Patrick', 'Frank Guinta', 'Gwen Moore', 'Elaine Lee', 'Marco Rubio', 'Scott DesJarlais', 'Jim Sensenbrenner', 'Jeff Miller', 'Randy Hultgren', 'Trey Gowdy', 'Dave Loebsack', 'Pedro Pierluisi', 'Niki Tsongas', 'Loretta Sanchez', 'Raja Krishnamoorthi', 'Mike Fitzpatrick', 'Paul Ryan', 'Vicky Hartzler', 'Mark Walker', 'Blunt Rochester', 'Will Hurd', 'Pete Sessions', 'Norma Torres', 'Jeanne Shaheen', 'Stephanie Murphy', 'Bob Latta', 'Dave Joyce', 'Adam Schiff', 'Derek Kilmer', 'Dan Kildee', 'Debbie Stabenow', 'Erik Paulsen', 'Ron Johnson', 'Chuck Grassley', 'Robin Kelly', 'David McKinley', 'Tom Price', 'Randy Weber', 'John Fleming', 'Pete Aguilar', 'John Garamendi', 'Kevin Yoder', 'Adam Kinzinger', 'Lamar Smith', 'Robert Aderholt', 'David Cicilline', 'Sherrod Brown', 'Joyce Beatty', 'Ami Bera', 'Aaron Schock', 'Jim McGovern', 'John Culberson', 'Ken Buck', 'John Boozman', 'Bill Nelson', 'Kathleen Rice', 'Mac Thornberry', 'Rob Woodall', 'Al Franken', 'Patrick McHenry', 'Jasmine Coleman', 'Nydia Velazquez', 'Steve Israel', 'Todd Rokita', 'Paul Gosar', 'Suzan DelBene', 'Chaka Fattah', 'Danny Davis', 'Donna Edwards', 'Mike Rogers', 'Roger Williams', 'John Ratcliffe', 'John Faso', 'Patrick Meehan', 'David Cicilline', 'Judge Carter', 'Richard Hanna', 'Richard Hudson', 'John Moolenaar', 'Brad Ashford', 'Lacy Clay', 'Rick Crawford', 'Barbara Comstock', 'Lucille Roybal-Allard', 'Ben Cardin', 'Bill Posey', 'Maxine Waters', 'Dana Rohrabacher', 'Doug Lamborn', 'Brad Schneider', 'Diane Black', 'Raul Grijalva', 'Katherine Clark', 'Warren Davidson', 'Ed Royce', 'Jason Chaffetz', 'Tim Walberg', 'Mark Takai', 'Neal Dunn', 'Robert Pittenger', 'Daniel Lipinski', 'Curt Clawson', 'Elizabeth Warren', 'Jon Tester', 'French Hill', 'Barbara Lee', 'Susan Davis', 'Elise Stefanik', 'Gary Peters', 'John Cornyn', 'Chris Murphy', 'Al Green', 'John Larson', 'Mia Love', 'Pramila Jayapal', 'Susan Collins', 'Steve Pearce', 'Tom McClintock', 'Tim Scott', 'Sheldon Whitehouse', 'Liz Cheney', 'Steve Knight', 'Blake Farenthold', 'Elizabeth Esty', 'Lee Zeldin', 'Steny Hoyer', 'David Kustoff', 'Judy Chu', 'Pete Aguilar', 'Brian Babin', 'Seth Moulton', 'Dina Titus', 'Mimi Walters', 'John Sarbanes', 'Debbie Dingell', 'Kurt Schrader', 'Raul Ruiz', 'Tulsi Gabbard', 'Mike Coffman', 'Jose Serrano', 'Louie Gohmert', 'Kyrsten Sinema', 'Mike Lee', 'Doug LaMalfa', 'Eleanor Holmes', 'Amy Klobuchar', 'Bob Casey', 'Thomas Massie', 'Josh Gottheimer', 'Salud Carbajal', 'Ted Yoho', 'Garret Graves', 'Grace Meng', 'Ken Calvert', 'David Price', 'Rod Blum', 'Jim Himes', 'Greg Walden', 'Bradley Byrne', 'Ted Deutch', 'Brian Higgins', 'Glenn Grothman', 'Ann McLane', 'Steve Cohen', 'Kay Granger', 'Bill Shuster', 'Tom Rooney', 'Steve Womack', 'John Hoeven', 'Gus Bilirakis', 'Joaquin Castro', 'Pete Olson', 'Sheila Jackson', 'Jeff Flake', 'Chris Stewart', 'George Butterfield', 'Terri Sewell', 'Susan Brooks', 'Bill Flores', 'Thom Tillis', 'Debbie Wasserman', 'Alma Adams', 'Tim Ryan', 'Nita Lowey', 'Phil Roe', 'Ileana Ros-Lehtinen', 'Darrell Issa', 'Cedric Richmond', 'Blaine Luetkemeyer', 'Jackie Walorski', 'Mark Meadows', 'Michael Capuano', 'Pat Toomey', 'Randy Forbes', 'Steven Palazzo', 'Mike Turner', 'Daniel Webster', 'Denny Heck', 'Evan Jenkins', 'Jack Bergman', 'Mike Honda', 'Jacky Rosen', 'Tom Emmer', 'Brian Mast', 'Jared Polis', 'Cheri Bustos', 'Buddy Carter', 'John Yarmuth', 'Jim Langevin', 'Richard Neal', 'Claire McCaskill', 'Mark Warner', 'Albio Sires', 'Mark Pocan', 'Angus King', 'Andr\xc3\xa9 Carson', 'Matt Cartwright', 'Steve Stivers', 'Robert Dold', 'Jerry Moran', 'Ryan Zinke', 'Patrick Leahy', 'John Kline', 'Diana DeGette', 'Richard Blumenthal', 'Mark Takano', 'Jan Schakowsky', 'Matt Salmon', 'Seth Moulton', 'Jack Reed', 'Ron Wyden', 'Donna Christensen', 'Mark Sanford', 'Robert Hurt', 'Chris Van', 'Charlie Crist']

$.getScript("/static/awesomplete.js", function() {
   // alert("Script loaded but not necessarily executed.");
   var input = document.getElementById("politician_input");
   new Awesomplete(input, {
     list: politicians
   });
});

function validateForm() {
    var politician = document.getElementById("politician_input").value;
    var issue = document.getElementById("free_form_input").value;
    if((!politician || !politicians.includes(politician)) && (!issue || issue.length < 1)) {
        alert("Please enter a valid politician and issue");
        return false;
    }
    else if(!politician || !politicians.includes(politician)){
      alert("Please enter a valid politician name");
      return false;
    }
    else if(!issue || issue.length < 1){
      alert("Please enter an issue");
      return false;
    }
}
