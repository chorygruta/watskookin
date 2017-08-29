$(function() {
    var submit_form = function(e) {
        $('#myIngredients').css('height', '0');
        var ingredientString = "";
        $('#myUL').find('li').each(function() {
            ingredientString += $(this).text().slice(0, -1) + ', ';
        });
        ingredientString = ingredientString.slice(0, -2);
        document.getElementById("ingredientList").value = ingredientString;

        $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
            a: $('input[name="a"]').val(),
        }, function(data) {
            var text = "";
            var i;
            for (i = 0; i < data.result.length; i++) {
                text += data.result[i] + ", ";
            }

            $('#result').text(text);
        });
        return false;
    };
    $('a#calculate').bind('click', submit_form);
    $('input[type=text]').bind('keydown', function(e) {
        if (e.keyCode == 13) {
            submit_form(e);
        }
    });
});

function openNav() {
    document.getElementById("ingredientCarousel").style.width = "100%";
}

function closeNav() {
    document.getElementById("ingredientCarousel").style.width = "0%";
}

// Create a "close" button and append it to each list item
var myNodelist = document.getElementsByTagName("LI");
var i;
for (i = 0; i < myNodelist.length; i++) {
    var span = document.createElement("SPAN");
    var txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("close");
var i;
for (i = 0; i < close.length; i++) {
    close[i].onclick = function() {
        var div = this.parentElement;
        //div.style.display = "none";
        var parent = document.getElementById("myUL");
        parent.removeChild(div);
    }
}

// Create a new list item when clicking on the "Add" button
function newElement() {
    if (document.getElementById("myInput").value === '') {
        var x = document.getElementById("snackbar")
        x.innerHTML = "Please enter an ingredient";
        x.className = "show";
        setTimeout(function() {
            x.className = x.className.replace("show", "");
        }, 3000);
    } else {

        var check = true;
        $('#myUL').find('li').each(function() {
            var innerDivId = $(this).text();
            innerDivId = innerDivId.slice(0, -1);

            if (innerDivId.toLowerCase() === document.getElementById("myInput").value.toLowerCase())
                check = false;
        });

        if (check) {

            var out = document.getElementById("ingredientBank");
            var li = document.createElement("li");
            var inputValue = document.getElementById("myInput").value;
            var isScrolledToBottom = out.scrollHeight - out.clientHeight <= out.scrollTop + 1;
            var t = document.createTextNode(inputValue);
            li.appendChild(t);
            document.getElementById("myUL").appendChild(li);

            document.getElementById("myInput").value = "";

            var span = document.createElement("SPAN");
            var txt = document.createTextNode("\u00D7");
            span.className = "close";
            span.appendChild(txt);
            li.appendChild(span);

            if (isScrolledToBottom)
                out.scrollTop = out.scrollHeight - out.clientHeight;

            for (i = 0; i < close.length; i++) {
                close[i].onclick = function() {
                    var div = this.parentElement;
                    var parent = document.getElementById("myUL");
                    parent.removeChild(div);

                }
            }
        } else {
            var x = document.getElementById("snackbar")
            x.innerHTML = "'" + document.getElementById("myInput").value + "' has already been added";
            x.className = "show";
            setTimeout(function() {
                x.className = x.className.replace("show", "");
            }, 3000);
        }
    }
}


function newElementFromPantry(name) {
    var out = document.getElementById("ingredientBank");
    var li = document.createElement("li");
    var inputValue = name;

    var check = true;
    $('#myUL').find('li').each(function() {
        var innerDivId = $(this).text();
        innerDivId = innerDivId.slice(0, -1);
        if (innerDivId.toLowerCase() === name.toLowerCase())
            check = false;
    });

    if (check) {

        var isScrolledToBottom = out.scrollHeight - out.clientHeight <= out.scrollTop + 1;

        var t = document.createTextNode(inputValue);
        li.appendChild(t);
        if (inputValue === '') {
            alert("No Ingredient Entered!");
        } else {
            document.getElementById("myUL").appendChild(li);
        }
        document.getElementById("myInput").value = "";

        var span = document.createElement("SPAN");
        var txt = document.createTextNode("\u00D7");
        span.className = "close";
        span.appendChild(txt);
        li.appendChild(span);

        if (isScrolledToBottom)
            out.scrollTop = out.scrollHeight - out.clientHeight;

        for (i = 0; i < close.length; i++) {
            close[i].onclick = function() {
                var div = this.parentElement;
                var parent = document.getElementById("myUL");
                parent.removeChild(div);
            }
        }
    } else {
        var x = document.getElementById("snackbar")
        x.innerHTML = "'" + name + "' has already been added";
        x.className = "show";
        setTimeout(function() {
            x.className = x.className.replace("show", "");
        }, 3000);
    }
}

function search() {
    var ingredientString = "";
    $('#myUL').find('li').each(function() {
        ingredientString += $(this).text().slice(0, -1) + ', ';
    });
    ingredientString = ingredientString.slice(0, -2);
    alert(ingredientString);
}
