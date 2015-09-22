var rdfstore = N3.Store();


function do_parse(rdf_data, store) {
    var parser = N3.Parser();

    parser.parse(rdf_data, function (error, triple, prefixes) {
        if (triple) {
            rdfstore.addTriple(triple.subject, triple.predicate, triple.object);
        }
    });
};


function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    for (var i = 0, f; f = files[i]; i++) {

        var reader = new FileReader();
        reader.onload = (function(theFile) {
            return function(e) {

                /*
                var ul = document.getElementById("triples-list");
                var li = document.createElement("li");
                li.appendChild(document.createTextNode("Four"));
                li.setAttribute("class", "list-group-item");
                ul.appendChild(li);
                */

                do_parse(e.target.result, rdfstore);

                /*alert(e.target.result);
                var row = '<li class="list-group-item">' + escape(theFile.name) + '</li>';
                alert(row);
                $('#triples-list ul').append(row);
                */
            };
        })(f);

        reader.readAsText(f);
    }
}

document.getElementById('rdf_file').addEventListener('change', handleFileSelect, false);
