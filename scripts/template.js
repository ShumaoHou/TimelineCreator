function gup(name) {
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.href);
  if (results == null) return "";
  else return results[1];
}

// get selected item count from url parameter
var count = Number(gup("count")) || 1000;

// create groups
var groups = new vis.DataSet([
  { id: 1, content: "Truck&nbsp;1" },
  { id: 2, content: "Truck&nbsp;2" },
  { id: 3, content: "Truck&nbsp;3" },
  { id: 4, content: "Truck&nbsp;4" },
]);

// create items
var items = new vis.DataSet();

var order = 1;
var truck = 1;
for (var j = 0; j < 4; j++) {
  var date = new Date();
  for (var i = 0; i < count / 4; i++) {
    date.setHours(date.getHours() + 4 * (Math.random() < 0.2));
    var start = new Date(date);

    date.setHours(date.getHours() + 2 + Math.floor(Math.random() * 4));
    var end = new Date(date);

    items.add({
      id: order,
      group: truck,
      start: start,
      end: end,
      content: "Order " + order,
    });

    order++;
  }
  truck++;
}

// specify options
var options = {
  stack: false,
  start: new Date(),
  end: new Date(1000 * 60 * 60 * 24 + new Date().valueOf()),
  editable: false,
  margin: {
    item: 10, // minimal margin between items
    axis: 5, // minimal margin between items and the axis
  },
  orientation: "top",
};

// create a Timeline
var container = document.getElementById("visualization");
timeline = new vis.Timeline(container, null, options);
timeline.setGroups(groups);
timeline.setItems(items);

window.addEventListener("resize", () => {
  /*timeline.checkResize();*/
});