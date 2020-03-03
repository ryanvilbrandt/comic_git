import { find_get_parameter } from "./utils.js";

export async function load_page() {
    await fetch_all_json_data();
}

async function fetch_all_json_data() {
    let response = await fetch("./comic/page_info_list.json");
    console.log("Fetched page info list");
    let json = await response.json();
    let tag = find_get_parameter("tag");
    console.log(json);
    build_tagged_list(json["page_info_list"], tag);
    document.getElementById("page-title").innerText = 'Posts tagged with "' + tag + '"';
}

function build_tagged_list(json_list, tag) {
    console.log(json_list);
    let html = "<ul>\n";
    json_list.forEach(comic_json => {
        if (comic_json["Tags"].includes(tag)) {
            html += build_page_link(comic_json);
        }
    });
    html += "</ul>";
    if (html === "<ul>\n</ul>") {
        html = "No posts found.";
    }
    document.getElementById("tagged").innerHTML = html;
}

function build_page_link(comic_json) {
    console.log(comic_json);
    let html = "        <li><a href='./comic/" + comic_json["page_name"] + ".html'>" + comic_json["Title"] + "</a>";
    html += " -- " + comic_json["Post date"] +"</li>\n";
    return html;
}